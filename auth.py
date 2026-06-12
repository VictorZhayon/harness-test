"""
api/routes/auth.py
──────────────────
POST /auth/register
POST /auth/login
GET  /auth/me
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from core.models import User
from db.database import get_db
from services.auth_service import AuthService
from api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------- Schemas ----------

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user_id: str
    email: str
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    user_id: str
    email: str
    is_active: bool


# ---------- Routes ----------

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user, token = AuthService(db).register(body.email, body.password)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc))
    return AuthResponse(user_id=user.id, email=user.email, access_token=token)


@router.post("/login", response_model=AuthResponse)
def login(body: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user, token = AuthService(db).login(body.email, body.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return AuthResponse(user_id=user.id, email=user.email, access_token=token)


@router.get("/me", response_model=MeResponse)
def me(current_user: User = Depends(get_current_user)):
    return MeResponse(
        user_id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
    )
