import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database.db import Base


class Facility(Base):
    __tablename__ = "facilities"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    district: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=True)


class HealthWorker(Base):
    __tablename__ = "health_workers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    facility_id: Mapped[str] = mapped_column(String(36), ForeignKey("facilities.id"), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="worker")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    facility_id: Mapped[str] = mapped_column(String(36), ForeignKey("facilities.id"), nullable=False)
    age: Mapped[float] = mapped_column(Float, nullable=False)
    sex: Mapped[str] = mapped_column(String(1), nullable=False)
    pregnancy_status: Mapped[bool] = mapped_column(Boolean, default=False)
    gestational_weeks: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Assessment(Base):
    __tablename__ = "assessments"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False)
    facility_id: Mapped[str] = mapped_column(String(36), ForeignKey("facilities.id"), nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), nullable=True)
    vitals: Mapped[dict] = mapped_column(JSON, nullable=False)
    news2_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_band: Mapped[str] = mapped_column(String(10), nullable=False)
    condition_detected: Mapped[str] = mapped_column(String(50), nullable=False)
    action_card_id: Mapped[str] = mapped_column(String(20), nullable=True)
    gps_lat: Mapped[float] = mapped_column(Float, nullable=True)
    gps_lon: Mapped[float] = mapped_column(Float, nullable=True)
    score_type: Mapped[str] = mapped_column(String(10), nullable=False, default="NEWS2")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessments.id"), nullable=False)
    facility_id: Mapped[str] = mapped_column(String(36), ForeignKey("facilities.id"), nullable=False)
    risk_band: Mapped[str] = mapped_column(String(10), nullable=False)
    sent_via: Mapped[list] = mapped_column(JSON, default=list)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    acknowledged_by: Mapped[str] = mapped_column(String(255), nullable=True)
    acknowledged_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    escalation_level: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SyncLog(Base):
    __tablename__ = "sync_log"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id: Mapped[str] = mapped_column(String(255), nullable=False)
    records_synced: Mapped[int] = mapped_column(Integer, default=0)
    synced_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    errors: Mapped[dict] = mapped_column(JSON, default=dict)
