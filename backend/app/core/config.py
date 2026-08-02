import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "LeafSense AI API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Paths
    API_V1_STR: str = "/api"
    
    # CORS Origins (Handles string serialized lists or direct lists)
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # JWT Configs
    JWT_SECRET: str = "db5a9ef22e86bfd7b5bf3b8cd09641ab3e46c72e2d9cd7de28e67a7d42cf3891"

    @field_validator("JWT_SECRET", mode="after")
    @classmethod
    def check_jwt_secret_in_production(cls, v: str, info) -> str:
        env = info.data.get("ENVIRONMENT", "development")
        default_secret = "db5a9ef22e86bfd7b5bf3b8cd09641ab3e46c72e2d9cd7de28e67a7d42cf3891"
        if env == "production" and v == default_secret:
            raise ValueError(
                "Security Risk: Default JWT_SECRET cannot be used in production environment! "
                "Configure a secure random secret via the JWT_SECRET environment variable."
            )
        return v

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Database Settings
    DB_USER: str = "leafsense_admin"
    DB_PASSWORD: str = "leafsense_secure_pass_2026"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "leafsense_db"
    
    DATABASE_URL: str = ""

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str, info) -> str:
        if v:
            return v
        # Assemble Postgres connection string if fields exist
        data = info.data
        user = data.get("DB_USER")
        password = data.get("DB_PASSWORD")
        host = data.get("DB_HOST")
        port = data.get("DB_PORT")
        name = data.get("DB_NAME")
        
        # Enforce PostgreSQL configuration parameters are defined
        if user is None or password is None or host is None or name is None:
            raise ValueError(
                "Database credentials (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME) "
                "or DATABASE_URL must be provided."
            )
            
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

    # ML Model Configs
    MODEL_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "ml", "saved_model", "plant_disease_model.keras"
    )
    CLASS_INDICES_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "ml", "saved_model", "class_indices.json"
    )
    DISEASE_INFO_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "ml", "saved_model", "disease_info.json"
    )
    
    # Uploads Storage (inside backend directory)
    UPLOAD_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "uploads"
    )

    # AWS S3 Settings
    AWS_S3_BUCKET: str = ""
    AWS_REGION: str = "ap-south-1"
    USE_S3_STORAGE: bool = False


    # Config source file
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            ".env"
        ),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
