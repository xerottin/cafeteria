from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.base import get_pg_db
from schemas.admin import AdminInDB, AdminCreate
from database import db_admin
router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/", response_model=AdminInDB)
def create_admin(data: AdminCreate, db: Session = Depends(get_pg_db), sysadmin=Security(get_current_admin)):
    if data.username == 'admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must not be admin")
    return db_admin.create_admin(db, data)
