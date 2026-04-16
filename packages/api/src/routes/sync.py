import uuid
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.db import get_db
from src.database.models import Patient, Assessment, SyncLog
from src.schemas import SyncBatchSchema
from src.scoring import calculate_news2
import structlog

router = APIRouter(prefix="/sync", tags=["sync"])
logger = structlog.get_logger()


@router.post("")
async def sync_records(body: SyncBatchSchema, db: AsyncSession = Depends(get_db)):
    results = []
    synced = 0
    errors = []

    for record in body.records:
        try:
            status = await _process_record(
                record.table, record.data, record.clientId, record.clientTimestamp, db
            )
            results.append({"clientId": record.clientId, "status": status})
            if status in ("created", "updated"):
                synced += 1
        except Exception as e:
            err = {"clientId": record.clientId, "status": "error", "reason": str(e)}
            results.append(err)
            errors.append(err)

    log = SyncLog(device_id=body.deviceId, records_synced=synced, errors={"items": errors})
    db.add(log)
    await db.commit()

    return {
        "processed": len(body.records),
        "synced": synced,
        "results": results,
        "serverTimestamp": datetime.utcnow().isoformat(),
    }


async def _process_record(table: str, data: dict, client_id: str, client_ts: str, db: AsyncSession) -> str:
    if table == "assessments":
        existing = await db.execute(select(Assessment).where(Assessment.id == client_id))
        ex = existing.scalar_one_or_none()
        if ex:
            try:
                client_dt = datetime.fromisoformat(client_ts.replace("Z", "+00:00"))
                if client_dt.replace(tzinfo=None) <= ex.created_at:
                    return "skipped"
            except Exception:
                return "skipped"

        patient_data = data.get("patient", {})
        if patient_data and patient_data.get("id"):
            p_result = await db.execute(select(Patient).where(Patient.id == patient_data["id"]))
            if not p_result.scalar_one_or_none():
                p = Patient(
                    id=patient_data["id"],
                    facility_id=patient_data.get("facilityId", ""),
                    age=patient_data.get("age", 0),
                    sex=patient_data.get("sex", "O"),
                    pregnancy_status=patient_data.get("pregnancyStatus", False),
                )
                db.add(p)

        vitals = data.get("vitals", {})
        server_score = calculate_news2(vitals) if vitals else {"totalScore": 0, "band": "LOW"}

        assessment = Assessment(
            id=client_id,
            patient_id=data.get("patientId", patient_data.get("id", "")),
            facility_id=data.get("facilityId", ""),
            worker_id=data.get("workerId"),
            vitals=vitals,
            news2_score=server_score["totalScore"],
            risk_band=server_score["band"],
            condition_detected=data.get("conditionDetected", "GENERAL"),
            action_card_id=data.get("actionCardId"),
            gps_lat=data.get("gpsLat"),
            gps_lon=data.get("gpsLon"),
        )
        if ex:
            for k, v in assessment.__dict__.items():
                if not k.startswith("_"):
                    setattr(ex, k, v)
            return "updated"
        else:
            db.add(assessment)
            await db.flush()
            return "created"

    return "skipped"
