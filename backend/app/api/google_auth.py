from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

from app.core.security import JWTAuth
from app.schemas.user import Token
from app.services.auth import AuthService
from app.core.config import settings


router = APIRouter()

class GoogleAuthRequest(BaseModel):
    id_token: str

@router.post("/google-login", response_model=Token)
def google_login(payload: GoogleAuthRequest, service: AuthService = Depends()):
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.id_token,
            grequests.Request(),
            audience = f"{settings.VITE_GOOGLE_CLIENT_ID}"

        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    email = idinfo["email"]
    name = idinfo.get("name", email)

    user = service.user_repo.get_by_email(email)
    if not user:
        user = service.user_repo.create_google_user(email=email, name=name)

    token = JWTAuth.create_token(subject=user.id, role=user.role.value)
    return Token(access_token=token)
