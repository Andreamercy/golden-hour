import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.db import get_db
from src.database.models import Facility

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get("")
async def list_facilities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Facility))
    rows = result.scalars().all()
    return [
        {"id": r.id, "name": r.name, "district": r.district, "state": r.state,
         "latitude": r.latitude, "longitude": r.longitude, "contactPhone": r.contact_phone}
        for r in rows
    ]


@router.post("", status_code=201)
async def create_facility(body: dict, db: AsyncSession = Depends(get_db)):
    f = Facility(
        id=str(uuid.uuid4()),
        name=body["name"],
        district=body.get("district", ""),
        state=body.get("state", ""),
        latitude=body["latitude"],
        longitude=body["longitude"],
        contact_phone=body.get("contactPhone"),
    )
    db.add(f)
    await db.commit()
    return {"id": f.id, "name": f.name}


@router.get("/{facility_id}")
async def get_facility(facility_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Facility).where(Facility.id == facility_id))
    f = result.scalar_one_or_none()
    if not f:
        raise HTTPException(404, "Facility not found")
    return {"id": f.id, "name": f.name, "district": f.district,
            "latitude": f.latitude, "longitude": f.longitude, "contactPhone": f.contact_phone}
