from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db_cafeteria, db_company
from database.base import get_pg_db
from schemas.cafeteria import CafeteriaCreate, CafeteriaUpdate, CafeteriaInDB
from schemas.company import CompanyUpdate

router = APIRouter(prefix="", tags=["cafeteria"])

@router.post("/")
async def create_cafeteria(data: CafeteriaCreate, db: Session = Depends(get_pg_db)):
    return db_cafeteria.create_cafeteria(db, data)

@router.get("/")
async def get_cafeteria(pk: int, db: Session = Depends(get_pg_db)):
    return db_cafeteria.get_cafeteria(db, pk)

@router.put("/")
async def put_cafeteria(pk: int, data: CafeteriaUpdate, db: Session = Depends(get_pg_db)):
    return db_cafeteria.edit_cafeteria(db, pk, data)


@router.delete("/", response_model=CafeteriaInDB)
def delete_cafeteria(pk: int, db: Session = Depends(get_pg_db)):
    return db_cafeteria.delete_cafeteria(db, pk)

@router.put("/company")
async def update_company(pk: int, data: CompanyUpdate, db: Session = Depends(get_pg_db)):
    return db_company.update_company(db, pk, data)