from datetime import timedelta
from database.base import get_pg_db
from models import Cafeteria
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from schemas.cafeteria import CafeteriaCreate, CafeteriaUpdate
from auth.oauth2 import hash_password, create_access_token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES


def create_cafeteria(data: CafeteriaCreate, db: Session = Depends(get_pg_db)):
    exist_cafeteria = db.query(Cafeteria).filter_by(username=data.username).first()
    if exist_cafeteria:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    hashed_password = hash_password(data.password)
    new_cafeteria = Cafeteria(username=data.username, password=hashed_password)
    db.add(new_cafeteria)
    db.commit()
    db.refresh(new_cafeteria)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": data.username}, expires_delta=access_token_expires)

    return new_cafeteria, access_token


def get_cafeteria(pk: int, db: Session):
    cafeteria = db.query(Cafeteria).filter_by(id=pk).first()
    if cafeteria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return cafeteria

def edit_cafeteria(db: Session, pk: int, data: CafeteriaUpdate ):
    cafeteria = db.query(Cafeteria).filter_by(id=pk).first()
    if cafeteria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    if data.username:  cafeteria.username = data.username
    if data.password:  cafeteria.password = data.password
    if data.phone:  cafeteria.phone = data.phone
    if data.url: cafeteria.url = data.url
    if data.logo: cafeteria.logo = data.logo
    if data.company_id: cafeteria.company_id = data.company_id
    db.commit()
    db.refresh(cafeteria)
    return cafeteria

def delete_cafeteria(db: Session, pk: int):
    cafeteria = db.query(Cafeteria).filter_by(id=pk).first()
    if cafeteria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cafeteria not found")
    cafeteria.is_active = False
    db.commit()
    db.refresh(cafeteria)
    return cafeteria