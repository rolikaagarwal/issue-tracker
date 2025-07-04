from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum
from app.schemas.user import UserCreate
from app.core.security import PasswordHasher

class UserRepository:
    """Handles DB operations for User model."""
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user_in: UserCreate, role: RoleEnum = RoleEnum.REPORTER) -> User:
        hashed = PasswordHasher.hash(user_in.password)
        user = User(email=user_in.email, hashed_password=hashed, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user