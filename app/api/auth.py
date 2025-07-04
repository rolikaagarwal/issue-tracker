from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserRead, Token

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(
    user_in: UserCreate,
    service: AuthService = Depends()
):
    """
    Register a new user. FastAPI will inject AuthService,
    which in turn gets a real DB session via get_db().
    """
    return service.register(user_in)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends()
):
    """
    Authenticate credentials via form-data (username/password)
    and return a JWT access token.
    """
    return service.authenticate(form_data.username, form_data.password)

@router.get("/me", response_model=UserRead)
def me(
    current_user=Depends()
):
    """
    Return details about the currently authenticated user.
    """
    return current_user
