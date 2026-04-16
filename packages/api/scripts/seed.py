import asyncio
import uuid
from src.database.db import AsyncSessionLocal, engine
from src.database.models import Base, Facility, HealthWorker
from src.auth.jwt import hash_password

FACILITIES = [
    {"id": str(uuid.uuid4()), "name": "Chennai Government Hospital", "district": "Chennai",
     "state": "Tamil Nadu", "latitude": 13.0827, "longitude": 80.2707, "contact_phone": "+914422250000"},
    {"id": str(uuid.uuid4()), "name": "Coimbatore Medical College", "district": "Coimbatore",
     "state": "Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558, "contact_phone": "+914222301000"},
    {"id": str(uuid.uuid4()), "name": "Madurai Rajaji Hospital", "district": "Madurai",
     "state": "Tamil Nadu", "latitude": 9.9252, "longitude": 78.1198, "contact_phone": "+914522532535"},
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        for f_data in FACILITIES:
            db.add(Facility(**f_data))

        workers = [
            HealthWorker(id=str(uuid.uuid4()), name="Dr. Priya Rajan",
                         facility_id=FACILITIES[0]["id"], phone="+919876543210",
                         role="supervisor", hashed_password=hash_password("golden123")),
            HealthWorker(id=str(uuid.uuid4()), name="Nurse Kavitha",
                         facility_id=FACILITIES[0]["id"], phone="+919876543211",
                         role="worker", hashed_password=hash_password("golden123")),
            HealthWorker(id=str(uuid.uuid4()), name="Dr. Arjun Kumar",
                         facility_id=FACILITIES[1]["id"], phone="+919876543212",
                         role="supervisor", hashed_password=hash_password("golden123")),
            HealthWorker(id=str(uuid.uuid4()), name="Nurse Meena",
                         facility_id=FACILITIES[1]["id"], phone="+919876543213",
                         role="worker", hashed_password=hash_password("golden123")),
            HealthWorker(id=str(uuid.uuid4()), name="Dr. Sunitha",
                         facility_id=FACILITIES[2]["id"], phone="+919876543214",
                         role="supervisor", hashed_password=hash_password("golden123")),
        ]
        for w in workers:
            db.add(w)

        await db.commit()
        print(f"Seeded {len(FACILITIES)} facilities and {len(workers)} workers.")
        print("Default password for all accounts: golden123")
        for f in FACILITIES:
            print(f"  Facility: {f['name']} — ID: {f['id']}")


if __name__ == "__main__":
    asyncio.run(seed())
