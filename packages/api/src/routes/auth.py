from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.db import get_db
from src.database.models import HealthWorker
from src.auth.jwt import verify_password, create_token
from src.schemas import LoginSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(body: LoginSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HealthWorker).where(HealthWorker.id == body.workerId))
    worker = result.scalar_one_or_none()
    if not worker or not verify_password(body.password, worker.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_token(worker.id, worker.facility_id, worker.role)
    return {"token": token, "workerId": worker.id, "facilityId": worker.facility_id, "role": worker.role}
