from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db_cafeteria
from database.base import get_pg_db
from schemas.cafeteria import CafeteriaCreate, CafeteriaUpdate, CafeteriaInDB

router = APIRouter(prefix="", tags=["cafeteria"])

@router.post("/")
async def create_cafeteria(data: CafeteriaCreate, db: Session = Depends(get_pg_db)):
    cafeteria, access_token = db_cafeteria.create_cafeteria(data, db)
    return cafeteria, access_token

@router.get("/")
async def get_cafeteria(pk: int, db: Session = Depends(get_pg_db)):
    return db_cafeteria.get_cafeteria(pk, db)

@router.put("/")
async def put_cafeteria(pk: int, data: CafeteriaUpdate, db: Session = Depends(get_pg_db)):
    return db_cafeteria.edit_cafeteria(db, pk, data)


@router.delete("/", response_model=CafeteriaInDB)
def delete_cafeteria(pk: int, db: Session = Depends(get_pg_db)):
    return db_cafeteria.delete_cafeteria(db, pk)