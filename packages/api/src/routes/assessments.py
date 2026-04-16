import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.database.db import get_db
from src.database.models import Assessment, Patient, Alert
from src.schemas import AssessmentCreateSchema
from src.auth.jwt import get_current_worker
from src.scoring import calculate_news2
import structlog

router = APIRouter(prefix="/assessments", tags=["assessments"])
logger = structlog.get_logger()


@router.post("", status_code=201)
async def create_assessment(
    body: AssessmentCreateSchema,
    db: AsyncSession = Depends(get_db),
    worker=Depends(get_current_worker),
):
    server_score = calculate_news2(body.vitals.model_dump())
    if server_score["totalScore"] != body.clientScore:
        logger.warning(
            "score_mismatch",
            client_score=body.clientScore,
            server_score=server_score["totalScore"],
            device_id=body.deviceId,
        )

    patient_result = await db.execute(select(Patient).where(Patient.id == body.patient.id))
    patient = patient_result.scalar_one_or_none()
    if not patient:
        patient = Patient(
            id=body.patient.id,
            facility_id=body.patient.facilityId,
            age=body.patient.age,
            sex=body.patient.sex,
            pregnancy_status=body.patient.pregnancyStatus,
            gestational_weeks=body.patient.gestationalWeeks,
        )
        db.add(patient)

    assessment = Assessment(
        id=str(uuid.uuid4()),
        patient_id=body.patient.id,
        facility_id=body.patient.facilityId,
        worker_id=worker["sub"],
        vitals=body.vitals.model_dump(),
        news2_score=server_score["totalScore"],
        risk_band=server_score["band"],
        condition_detected=body.conditionDetected,
        action_card_id=body.actionCardId,
        gps_lat=body.gpsLat,
        gps_lon=body.gpsLon,
    )
    db.add(assessment)

    if server_score["band"] in ("HIGH", "CRITICAL"):
        alert = Alert(
            id=str(uuid.uuid4()),
            assessment_id=assessment.id,
            facility_id=body.patient.facilityId,
            risk_band=server_score["band"],
            sent_via=["DASHBOARD"],
        )
        db.add(alert)

    await db.commit()
    return {"id": assessment.id, "serverScore": server_score, "status": "created"}


@router.get("")
async def list_assessments(
    facility_id: str | None = None,
    risk_band: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    q = select(Assessment)
    if facility_id:
        q = q.where(Assessment.facility_id == facility_id)
    if risk_band:
        q = q.where(Assessment.risk_band == risk_band)
    q = q.order_by(Assessment.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    rows = result.scalars().all()
    return [
        {
            "id": r.id,
            "patientId": r.patient_id,
            "facilityId": r.facility_id,
            "riskBand": r.risk_band,
            "score": r.news2_score,
            "condition": r.condition_detected,
            "createdAt": r.created_at.isoformat(),
        }
        for r in rows
    ]


@router.get("/stats")
async def get_stats(facility_id: str | None = None, db: AsyncSession = Depends(get_db)):
    today = datetime.utcnow().date()
    q = select(Assessment.risk_band, func.count(Assessment.id)).group_by(Assessment.risk_band)
    if facility_id:
        q = q.where(Assessment.facility_id == facility_id)
    result = await db.execute(q)
    by_band = {row[0]: row[1] for row in result.all()}

    today_q = select(func.count(Assessment.id)).where(func.date(Assessment.created_at) == today)
    if facility_id:
        today_q = today_q.where(Assessment.facility_id == facility_id)
    today_count = (await db.execute(today_q)).scalar() or 0

    return {"totalToday": today_count, "byBand": by_band}


@router.get("/{assessment_id}")
async def get_assessment(assessment_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Assessment).where(Assessment.id == assessment_id))
    a = result.scalar_one_or_none()
    if not a:
        raise HTTPException(404, "Assessment not found")
    return {
        "id": a.id,
        "patientId": a.patient_id,
        "vitals": a.vitals,
        "riskBand": a.risk_band,
        "score": a.news2_score,
        "condition": a.condition_detected,
        "createdAt": a.created_at.isoformat(),
    }
