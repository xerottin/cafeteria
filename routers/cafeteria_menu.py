from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import db_cafeteria
from database.base import get_pg_db
from schemas.cafeteria import MenuCreate, CoffeeCreate

router = APIRouter(prefix="", tags=["xuy"])

@router.post("/menu")
async def menu_create(data:MenuCreate, db: Session = Depends(get_pg_db)):
    cafeteria = db_cafeteria.create_menu(data, db)
    return cafeteria

@router.get("/menu")
async def menu_get(pk: int, db: Session = Depends(get_pg_db)):
    return db_cafeteria.get_menu(pk, db)


#coffee
@router.post("/coffe")
async def coffee_create(data:CoffeeCreate, db: Session = Depends(get_pg_db)):
    coffee = db_cafeteria.create_coffee(data, db)
    return coffee
