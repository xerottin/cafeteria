from datetime import timedelta

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from database.db_user import hash_password, create_access_token
from models import Admin
from schemas.admin import AdminCreate, AdminUpdate
from database.base import get_pg_db
from settings import ACCESS_TOKEN_EXPIRE_MINUTES


def create_admin(data: AdminCreate, db: Session = Depends(get_pg_db)):
    existing_admin = db.query(Admin).filter(Admin.username == data.username).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = hash_password(data.password)
    new_admin = Admin(username=data.username, password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def get_admin(pk:int, db: Session = Depends(get_pg_db)):
    admin = db.query(Admin).filter(Admin.id == pk).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return admin

def update_admin(pk: int, db: Session, admin_update: AdminUpdate):
    db_admin = db.query(Admin).filter(Admin.id == pk).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )

    if admin_update.username:
        existing_admin = db.query(Admin).filter(Admin.username == admin_update.username).first()
        if existing_admin and existing_admin.id != pk:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя уже зарегистрировано"
            )
        db_admin.username = admin_update.username

    if admin_update.password:
        db_admin.password = hash_password(admin_update.password)

    db.commit()
    db.refresh(db_admin)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": db_admin.username}, expires_delta=access_token_expires)
    return {
        "id": db_admin.id,
        "username": db_admin.username,
        "created_at": db_admin.created_at,
        "updated_at": db_admin.updated_at,
        "access_token": access_token,
        "token_type": "bearer"
    }

def delete_admin(pk: int, db: Session = Depends(get_pg_db)):
    admin = db.query(Admin).filter(Admin.id == pk).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    admin.is_active = False
    db.commit()
    db.refresh(admin)
    return admin