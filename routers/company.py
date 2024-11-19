from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import db_company
from database.base import get_pg_db
from schemas.company import CompanyCreate, CompanyUpdate

router = APIRouter(prefix="/company", tags=["company"])


@router.post("/")
async def create_company(
    data: CompanyCreate,
    db: Session = Depends(get_pg_db),
    # sysadmin=Security(get_current_admin)
):
    company = db_company.create_company(db, data)
    return company

@router.get("/")
async def read_company(pk: int, db: Session = Depends(get_pg_db)):
    return db_company.get_company(pk, db)

@router.put("/")
async def update_company(pk: int, data: CompanyUpdate, db: Session = Depends(get_pg_db)):
    return db_company.update_company(db, pk, data)

@router.delete("/")
def delete_company(pk: int, db: Session = Depends(get_pg_db)):
    return db_company.delete_company(pk, db)