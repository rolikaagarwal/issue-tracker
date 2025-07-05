from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from datetime import timedelta

from app.crud.user import UserRepository
from app.schemas.user import UserCreate, Token, TokenData, UserRead
from app.core.security import JWTAuth, PasswordHasher
from app.database.session import SessionLocal
from app.models.user import RoleEnum
from app.core.config import settings
from app.dependencies.auth import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, user_in: UserCreate) -> UserRead:
        if self.user_repo.get_by_email(user_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        user = self.user_repo.create(user_in)
        return UserRead.from_orm(user)

    def authenticate(self, username: str, password: str) -> Token:
        user = self.user_repo.get_by_email(username)
        if not user or not PasswordHasher.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = JWTAuth.create_token(subject=user.id, role=user.role.value, expires_delta=expires)
        return Token(access_token=token)

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> UserRead:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = JWTAuth.decode_token(token)
            user_id = int(payload.get("sub"))
            role = payload.get("role")
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=user_id, role=role)
        except JWTError:
            raise credentials_exception

        user = self.user_repo.get(token_data.user_id)
        if not user:
            raise credentials_exception
        return UserRead.from_orm(user)

    def require_role(self, required_role: RoleEnum):
        def role_checker(current_user: UserRead = Depends(self.get_current_user)):
            if current_user.role != required_role.value:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
            return current_user
        return role_checker