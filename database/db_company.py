from datetime import timedelta

from models import Company
from schemas.company import CompanyCreate, CompanyUpdate, CompanyBase
from sqlalchemy.orm import Session
from auth.oauth2 import create_access_token
from fastapi import status, HTTPException

from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.generator import no_bcrypt


def create_company(db: Session, data:CompanyCreate):
    existing_company = db.query(Company).filter_by(username=data.username).first()
    if existing_company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    new_company = Company(
        username=data.username,
        password=no_bcrypt(data.password),
        phone=data.phone,
        email=data.email,
        logo=data.logo,
        owner=data.owner
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def get_company(pk: int, db: Session):
    return db.query(Company).filter_by(id=pk, is_active=True).first()


def update_company(db: Session, pk: int, data: CompanyUpdate):
    company = db.query(Company).filter_by(id=pk, is_active=True).first()
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    if data.username: company.username = data.username
    if data.password: company.password = no_bcrypt(data.password)
    if data.phone: company.phone = data.phone
    if data.email: company.email = data.email
    if data.owner: company.owner = data.owner
    if data.logo: company.logo = data.logo
    db.commit()
    db.refresh(company)
    return company


def delete_company(pk: int, db: Session):
    company = db.query(Company).filter_by(id=pk).first()
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    company.is_active = False
    db.commit()
    db.refresh(company)
    return company