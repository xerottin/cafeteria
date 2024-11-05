from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db_user
from database.base import get_pg_db
from schemas.user import UserCreate, UserInDB, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserInDB)
async def create_user(user: UserCreate, db: Session = Depends(get_pg_db)):
    return db_user.create_user(user, db)
@router.get("/")
async def get_user(pk:int, db:Session = Depends(get_pg_db)):
    return db_user.get_user(db, pk)

@router.put("/{pk}", response_model=UserInDB)
async def update_user(pk: int, user_update: UserUpdate, db: Session = Depends(get_pg_db)):
    return db_user.update_user(pk, db, user_update)

@router.delete("/")
async def delete_user(pk: int, db: Session = Depends(get_pg_db)):
    return db_user.delete_user(db, pk)

