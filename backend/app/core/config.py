from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Document Processor API"
    admin_email: str = "admin@documentprocessor.com"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    mongodb_url: str
    mongodb_name: str = "document_processor"
    
    class Config:
        env_file = ".env"

settings = Settings()