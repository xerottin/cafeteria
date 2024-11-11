from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.oauth2 import create_access_token, get_current_cafeteria
from database.base import get_pg_db
from database.hash import Hash
from models import Admin, Cafeteria, User
from schemas.admin import AuthResponse
from schemas.cafeteria import CafeteriaInDB
from settings import USERNAME, PASSWORD

router = APIRouter(tags=["authentication"])


@router.post("/token", response_model=AuthResponse)
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_pg_db)):
    if request.username == USERNAME:
        if request.password != PASSWORD:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": request.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": request.username,
            "user_type": "admin"
        }
    admin = db.query(Admin).filter_by(username=request.username).first()
    cafeteria = db.query(Cafeteria).filter_by(username=request.username).first()
    user = db.query(User).filter_by(username=request.username).first()
    if admin:
        if not Hash.verify(admin.password, request.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        access_token = create_access_token(data={"sub": request.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": request.username,
            "user_type": "admin",
        }
    if cafeteria:
        if not Hash.verify(cafeteria.password, request.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        access_token = create_access_token(data={"cafeteria_id": cafeteria.id})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "cafeteria_id": cafeteria.id,
            "user_type": "cafeteria",
        }
    if user and Hash.verify(user.password, request.password):
        access_token = create_access_token(data={"username": user.username})
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            username=user.username,
            user_type="user"
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@router.post("/admin_token", response_model=AuthResponse)
def get_admin_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_pg_db)):
    if request.username == USERNAME:
        if request.password != PASSWORD:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": request.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": request.username,
            "user_type": "admin",
        }
    admin = db.query(Admin).filter_by(username=request.username).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not Hash.verify(admin.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    access_token = create_access_token(data={"sub": request.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": request.username,
        "user_type": "user",
    }

@router.post("/cafeteria_token", response_model=AuthResponse)
def get_cafeteria_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_pg_db)):
    cafeteria = db.query(Cafeteria).filter_by(username=request.username).first()
    if not cafeteria:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not Hash.verify(cafeteria.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    access_token = create_access_token(data={"sub": request.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": request.username,
        "user_type": "cafeteria",
    }

@router.post("/user_token", response_model=AuthResponse)
def get_user_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_pg_db)):
    user = db.query(User).filter_by(username=request.username).first()
    if user and Hash.verify(user.password, request.password):
        access_token = create_access_token(data={"sub": request.username})
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            username=request.username,
            user_type="user"
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@router.get("/cafeteria_me", response_model=CafeteriaInDB)
def get_cafeteria_me(cafeteria=Security(get_current_cafeteria)):
    return cafeteria
