from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database.base import get_pg_db
from database.db_user import hash_password, create_access_token
from models import User
from schemas.user import UserCreate, UserInDB
from settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserInDB)
async def create_user(user: UserCreate, db: Session = Depends(get_pg_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": user.username}, expires_delta=access_token_expires)

    return UserInDB(
        username=new_user.username,
        access_token=access_token,
        token_type="bearer"
    )
