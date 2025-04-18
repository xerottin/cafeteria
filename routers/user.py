from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from database import db_user
from database.base import get_pg_db
from schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_pg_db)):
    return db_user.create_user(db, user)


@router.get("/")
async def get_user(db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    pk = user_data.id
    return db_user.get_user_by_id(db, pk)


@router.put("/")
async def update_user(user_update: UserUpdate, db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    pk = user_data.id
    return db_user.update_user(db, pk, user_update)


@router.delete("/")
async def delete_user(db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    pk = user_data.id
    return db_user.delete_user(db, pk)
