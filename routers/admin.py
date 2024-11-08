from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import db_admin
from schemas.admin import AdminCreate, AdminInDB, AdminResponse, AdminUpdate
from database.base import get_pg_db

router = APIRouter(prefix="", tags=["admin"])


@router.post("/", response_model=AdminResponse)
async def admin_create(admin: AdminCreate, db: Session = Depends(get_pg_db)):
    return db_admin.create_admin(db, admin)

@router.get("/", response_model=AdminInDB)
async def get_admin(pk:int, db: Session = Depends(get_pg_db)):
    return db_admin.get_admin(pk, db)

@router.put("/", response_model=AdminInDB)
async def put_admin(
    pk: int,
    admin_update: AdminUpdate,
    db: Session = Depends(get_pg_db)
):
    return db_admin.update_admin(db, pk, admin_update)

@router.delete("/", response_model=AdminInDB)
async def delete_admin(pk:int, db: Session = Depends(get_pg_db)):
    return db_admin.delete_admin(pk, db)