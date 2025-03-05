from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import Admin
from schemas.admin import AdminCreate, AdminUpdate
from database.base import get_pg_db
from utils.generator import no_bcrypt


def create_admin(db: Session, data: AdminCreate):
    exist_admin = db.query(Admin).filter_by(username=data.username).first()
    if exist_admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    new_admin = Admin(username=data.username, password=no_bcrypt(data.password))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


def get_admin(pk: int, db: Session = Depends(get_pg_db)):
    admin = db.query(Admin).filter(Admin.id == pk).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return admin


def update_admin(db: Session, pk: int, data: AdminUpdate):
    same_admin = db.query(Admin).filter_by(username=data.username).first()
    if same_admin and same_admin.id != pk:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    admin = db.query(Admin).filter_by(id=pk, is_active=True).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    admin.username = data.username
    admin.password = no_bcrypt(data.password)
    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(pk: int, db: Session = Depends(get_pg_db)):
    admin = db.query(Admin).filter(Admin.id == pk).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    admin.is_active = False
    db.commit()
    db.refresh(admin)
    return admin


def get_admin_by_username(db: Session, username: str):
    return db.query(Admin).filter_by(username=username, is_active=True).first()
