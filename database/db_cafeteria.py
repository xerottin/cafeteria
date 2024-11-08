from datetime import timedelta
from database.base import get_pg_db
from models import Cafeteria
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

from models.cafeteria import Menu, Coffee
from schemas.cafeteria import CafeteriaCreate, CafeteriaUpdate, MenuCreate, CoffeeCreate
from auth.oauth2 import create_access_token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.generator import no_bcrypt


def get_client(db: Session, pk: int):
    return db.query(Cafeteria).filter_by(id=pk, is_active=True).first()


def create_cafeteria(db: Session, data: CafeteriaCreate):
    exist_cafeteria = db.query(Cafeteria).filter_by(username=data.username).first()
    if exist_cafeteria:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    new_cafeteria = Cafeteria(
        username=data.username,
        password=no_bcrypt(data.password),
        url=data.url,
        latitude=data.latitude,
        longitude=data.longitude,
        logo=data.logo,
        company_id=data.company_id,
    )
    db.add(new_cafeteria)
    db.commit()
    db.refresh(new_cafeteria)
    return new_cafeteria


def get_cafeteria(db: Session, pk: int):
    return db.query(Cafeteria).filter_by(id=pk, is_active=True).first()

def edit_cafeteria(db: Session, pk: int, data: CafeteriaUpdate ):
    cafeteria = db.query(Cafeteria).filter_by(id=pk).first()
    if cafeteria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    if data.username:  cafeteria.username = data.username
    if data.password:  cafeteria.password = data.password
    if data.phone:  cafeteria.phone = data.phone
    if data.url: cafeteria.url = data.url
    if data.latitude: cafeteria.latitude = data.latitude
    if data.longitude: cafeteria.longitude = data.longitude
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

def create_menu(data:MenuCreate, db: Session):
    exist_menu = db.query(Menu).filter_by(name=data.name).first()
    if exist_menu:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Name already exists")

    new_menu = Menu(name=data.name, cafeteria_id=data.cafeteria_id)
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

def get_menu(pk: int, db: Session):
    menu = db.query(Menu).filter_by(id=pk).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    return menu


def create_coffee(data: CoffeeCreate, db: Session):
    exist_coffee = db.query(Coffee).filter_by(name=data.name).first()
    if exist_coffee:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Coffee already exists")
    new_coffee = Coffee(name=data.name, origin=data.origin, flavor_profile=data.flavor_profile, bean_type=data.bean_type, weight=data.weight, stock=data.stock, price=data.price, is_available=data.is_available, menu_id=data.menu_id )
    db.add(new_coffee)
    db.commit()
    db.refresh(new_coffee)
    return new_coffee

