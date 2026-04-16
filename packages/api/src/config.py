from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://golden:golden@localhost:5432/golden_hour"
    redis_url: str = "redis://localhost:6379"
    jwt_secret: str = "changeme-use-256-bit-secret-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    environment: str = "development"
    alert_phone_number: str = "+911234567890"
    sms_provider_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
