from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SQLALCHEMY_DATABASE_URL: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    VITE_GOOGLE_CLIENT_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()