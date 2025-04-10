import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Backend API"
    PROJECT_DESCRIPTION: str = "FastAPI Backend with Enterprise Structure"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
   # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://myuser:mypassword@localhost:5432/mydb"
    )
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fgSr342sa#@$cvdfa#@")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

