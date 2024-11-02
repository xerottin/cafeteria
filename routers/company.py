from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import db_company
from database.base import get_pg_db
from schemas.company import CompanyCreate, CompanyUpdate

router = APIRouter(prefix="/company", tags=["company"])


@router.post("/")
async def create_company(data: CompanyCreate, db: Session = Depends(get_pg_db)):
    client, access_token = db_company.create_company(data, db)
    return client, access_token

@router.get("/")
async def read_company(pk: int, db: Session = Depends(get_pg_db)):
    return db_company.get_company(pk, db)

@router.put("/")
async def update_company(pk: int, data: CompanyUpdate, db: Session = Depends(get_pg_db)):
    return db_company.edit_company(pk, data, db)

@router.delete("/")
def delete_company(pk: int, db: Session = Depends(get_pg_db)):
    return db_company.delete_company(pk, db)