from pydantic import BaseModel, field_validator
from typing import Optional, Literal


class VitalsSchema(BaseModel):
    heartRate: float
    systolicBP: float
    diastolicBP: float
    temperature: float
    respiratoryRate: float
    spO2: float
    consciousnessLevel: Literal["A", "V", "P", "U"]
    supplementalOxygen: bool
    timestamp: str
    recordedBy: str

    @field_validator("heartRate")
    @classmethod
    def check_hr(cls, v):
        if not (20 <= v <= 300):
            raise ValueError("Heart rate must be 20-300 bpm")
        return v

    @field_validator("systolicBP")
    @classmethod
    def check_sbp(cls, v):
        if not (40 <= v <= 300):
            raise ValueError("Systolic BP must be 40-300 mmHg")
        return v

    @field_validator("diastolicBP")
    @classmethod
    def check_dbp(cls, v):
        if not (20 <= v <= 200):
            raise ValueError("Diastolic BP must be 20-200 mmHg")
        return v

    @field_validator("temperature")
    @classmethod
    def check_temp(cls, v):
        if not (25 <= v <= 45):
            raise ValueError("Temperature must be 25-45 °C")
        return v

    @field_validator("respiratoryRate")
    @classmethod
    def check_rr(cls, v):
        if not (1 <= v <= 80):
            raise ValueError("Respiratory rate must be 1-80")
        return v

    @field_validator("spO2")
    @classmethod
    def check_spo2(cls, v):
        if not (0 <= v <= 100):
            raise ValueError("SpO2 must be 0-100%")
        return v


class PatientSchema(BaseModel):
    id: str
    age: float
    sex: Literal["M", "F", "O"]
    pregnancyStatus: bool
    gestationalWeeks: Optional[int] = None
    facilityId: str


class AssessmentCreateSchema(BaseModel):
    patient: PatientSchema
    vitals: VitalsSchema
    clientScore: int
    clientBand: str
    conditionDetected: str
    actionCardId: Optional[str] = None
    gpsLat: Optional[float] = None
    gpsLon: Optional[float] = None
    deviceId: str


class SyncRecordSchema(BaseModel):
    table: str
    data: dict
    clientTimestamp: str
    clientId: str


class SyncBatchSchema(BaseModel):
    deviceId: str
    records: list[SyncRecordSchema]


class AlertAcknowledgeSchema(BaseModel):
    acknowledgedBy: str


class LoginSchema(BaseModel):
    workerId: str
    password: str
