from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_cafeteria
from database import db_cafeteria
from database.base import get_pg_db
from schemas.cafeteria import MenuCreate, CoffeeCreate

router = APIRouter(prefix="", tags=["xuy"])

@router.post("/menu")
async def create_menu(data:MenuCreate, db: Session = Depends(get_pg_db), cafeteria_data=Security(get_current_cafeteria)):
    cafeteria = db_cafeteria.create_menu(data, db)
    return cafeteria


@router.get("/menu/all")
async def get_menus(cafeteria_id: int, db: Session = Depends(get_pg_db), cafeteria_data=Security(get_current_cafeteria)):
    return db_cafeteria.get_menus(cafeteria_id, db)


@router.get("/menu")
async def get_menu(pk: int, db: Session = Depends(get_pg_db), cafeteria_data=Security(get_current_cafeteria)):
    return db_cafeteria.get_menu(pk, db)


@router.post("/coffe")
async def create_coffe(data:CoffeeCreate, db: Session = Depends(get_pg_db), cafeteria_data=Security(get_current_cafeteria)):
    coffee = db_cafeteria.create_coffee(data, db)
    return coffee
