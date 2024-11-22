from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from database import db_user
from database.base import get_pg_db
from models import Cafeteria
from schemas.cafeteria import CafeteriaResponse
import math
from typing import List
from sqlalchemy import select

from schemas.user import OrderCreate

router = APIRouter(prefix="", tags=["user_cafeteria"])


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@router.get("/cafeterias/nearby", response_model=List[CafeteriaResponse])
async def nearby_cafeterias(
    latitude: float,
    longitude: float,
    radius: float = 5.0,
    session = Depends(get_pg_db),
    user_data=Security(get_current_user)
):
    result = session.execute(select(Cafeteria))
    cafeterias = result.scalars().all()

    nearby_cafeterias = [
        cafeteria for cafeteria in cafeterias
        if haversine_distance(latitude, longitude, cafeteria.latitude, cafeteria.longitude) <= radius
    ]

    if not nearby_cafeterias:
        return []

    return nearby_cafeterias

@router.get("/cafeteria")
async def get_cafeteria_menus(pk: int, db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    return db_user.get_cafeteria_menus(pk, db)

@router.get("/menu/coffee")
async def get_menu_coffee(pk: int, db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    return db_user.get_menu_coffee(pk, db)


@router.post("/order")
async def create_order(data: OrderCreate, db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    pk = user_data.id
    return db_user.create_order_user(data, db, pk)


@router.get("/archive/me")
async def my_archive(db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    user_id = user_data.id
    return db_user.get_user_archive(user_id, db)


@router.post("/favourite")
def favourite(coffee_id: int, db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    user_id = user_data.id
    return db_user.create_favourite(user_id, coffee_id, db)

@router.get("favourite")
async def my_favouirite(db: Session = Depends(get_pg_db), user_data=Security(get_current_user)):
    user_id = user_data.id
    return db_user.get_my_fav(user_id, db)



