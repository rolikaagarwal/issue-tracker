from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

class PasswordHasher:
    """Encapsulates password hashing and verification."""
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        """Generate bcrypt hash for a password."""
        return cls._pwd_context.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify a plaintext password against its hash."""
        return cls._pwd_context.verify(plain_password, hashed_password)

class JWTAuth:
    """Encapsulates JWT token creation and decoding."""
    @staticmethod
    def create_token(subject: str | int, role: str, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT token embedding `sub` (subject) and `role`.
        Expires after settings.ACCESS_TOKEN_EXPIRE_MINUTES by default.
        """
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        payload = {"sub": str(subject), "role": role, "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode and verify a JWT token, raising JWTError on failure."""
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])