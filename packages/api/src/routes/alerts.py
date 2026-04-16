from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.db import get_db
from src.database.models import Alert
from src.schemas import AlertAcknowledgeSchema
from src.auth.jwt import get_current_worker

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
async def list_alerts(
    facility_id: str | None = None,
    acknowledged: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Alert).order_by(Alert.created_at.desc())
    if facility_id:
        q = q.where(Alert.facility_id == facility_id)
    if acknowledged is not None:
        q = q.where(Alert.acknowledged == acknowledged)
    result = await db.execute(q)
    rows = result.scalars().all()
    return [
        {
            "id": r.id,
            "assessmentId": r.assessment_id,
            "facilityId": r.facility_id,
            "riskBand": r.risk_band,
            "acknowledged": r.acknowledged,
            "acknowledgedBy": r.acknowledged_by,
            "escalationLevel": r.escalation_level,
            "createdAt": r.created_at.isoformat(),
        }
        for r in rows
    ]


@router.get("/active")
async def list_active_alerts(db: AsyncSession = Depends(get_db)):
    q = (
        select(Alert)
        .where(Alert.acknowledged == False, Alert.risk_band.in_(["HIGH", "CRITICAL"]))
        .order_by(Alert.created_at.desc())
    )
    result = await db.execute(q)
    rows = result.scalars().all()
    return [
        {"id": r.id, "facilityId": r.facility_id, "riskBand": r.risk_band, "createdAt": r.created_at.isoformat()}
        for r in rows
    ]


@router.patch("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    body: AlertAcknowledgeSchema,
    db: AsyncSession = Depends(get_db),
    worker=Depends(get_current_worker),
):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(404, "Alert not found")
    if alert.acknowledged:
        return {"status": "already_acknowledged"}
    alert.acknowledged = True
    alert.acknowledged_by = body.acknowledgedBy
    alert.acknowledged_at = datetime.utcnow()
    await db.commit()
    return {"status": "acknowledged", "id": alert_id}
