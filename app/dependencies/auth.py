from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.database.session import SessionLocal         
from app.core.security import JWTAuth            
from app.crud.user import UserRepository        
from app.schemas.user import TokenData            
from app.models.user import RoleEnum, User        

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    """
    Yield a database session, closing it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decode the JWT, load the user, and return the User model.
    Raises 401 if invalid or not found.
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = JWTAuth.decode_token(token)
        user_id = int(payload.get("sub") or 0)
        role = payload.get("role")
        if not user_id or not role:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, role=role)
    except JWTError:
        raise credentials_exception

    user = UserRepository(db).get(token_data.user_id)
    if not user:
        raise credentials_exception
    return user

def require_role(required_role: RoleEnum):
    """
    Dependency factory to enforce that current_user.role == required_role.
    Usage:
        @router.post(..., dependencies=[Depends(require_role(RoleEnum.ADMIN))])
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker
