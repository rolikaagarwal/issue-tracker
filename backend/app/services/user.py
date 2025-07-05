from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.user import UserRepository
from app.schemas.user import UserRead
from app.models.user import RoleEnum
from app.dependencies.auth import get_db

class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = UserRepository(db)

    def change_role(self, user_id: int, new_role: RoleEnum) -> UserRead:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        updated = self.repo.update_role(user, new_role)
        return UserRead.from_orm(updated)
