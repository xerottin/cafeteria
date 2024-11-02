from datetime import timedelta

from database.base import get_pg_db
from models import Company
from schemas.company import CompanyCreate, CompanyUpdate
from sqlalchemy.orm import Session
from auth.oauth2 import hash_password, create_access_token
from fastapi import Depends, status, HTTPException

from settings import ACCESS_TOKEN_EXPIRE_MINUTES


def create_company(data:CompanyCreate, db: Session = Depends(get_pg_db)):
    exist_company = db.query(Company).filter_by(username=data.username).first()
    if exist_company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    hashed_password = hash_password(data.password)
    new_company = Company(username=data.username, password=hashed_password)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": data.username}, expires_delta=access_token_expires)

    return new_company, access_token


def get_company(pk: int, db: Session = Depends(get_pg_db)):
    company = db.query(Company).filter_by(id=pk).first()
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


def edit_company(pk: int, data: CompanyUpdate, db: Session = Depends(get_pg_db)):
    company = db.query(Company).filter_by(id=pk).first()
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    if data.username: company.username = data.username
    if data.password: company.password = data.password
    if data.phone: company.phone = data.phone
    if data.email: company.email = data.email
    if data.owner: company.owner = data.owner
    db.commit()
    db.refresh(company)
    return company

def delete_company(pk: int, db: Session = Depends(get_pg_db)):
    company = db.query(Company).filter_by(id=pk).first()
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    company.is_active = False
    db.commit()
    db.refresh(company)
    return company