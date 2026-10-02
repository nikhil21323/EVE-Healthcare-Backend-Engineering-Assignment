from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import SignupRequest, LoginRequest, TokenResponse
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email already registered")
    user = User(email=data.email, password_hash=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return TokenResponse(access_token=create_access_token(user.id))

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return TokenResponse(access_token=create_access_token(user.id))
