from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str = "FastAPI Study"
    version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
