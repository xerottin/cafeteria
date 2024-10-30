from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import db_user
from database.base import get_pg_db
from database.db_user import hash_password, create_access_token
from models import User
from schemas.user import UserCreate, UserInDB, UserUpdate
from settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserInDB)
async def create_user(user: UserCreate, db: Session = Depends(get_pg_db)):
    return create_user(user, db)
@router.get("/")
async def get_user(pk:int, db:Session = Depends(get_pg_db)):
    return db_user.get_user(db, pk)

@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_pg_db)):
    return db_user.update_user(db, user_id, user_update)

@router.delete("/")
async def delete_user(user_id: int, db: Session = Depends(get_pg_db)):
    return db_user.delete_user(db, user_id)