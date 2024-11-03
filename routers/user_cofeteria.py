from fastapi import APIRouter, Depends

from database.base import get_pg_db
from models import Company, Cafeteria
from schemas.cafeteria import CafeteriaResponse
import math
from typing import List
from sqlalchemy import select

router = APIRouter(tags=["user-cofeteria"])

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@router.get("/cafeterias/nearby", response_model=List[CafeteriaResponse])
async def get_nearby_cafeterias(
        latitude: float,
        longitude: float,
        radius: float = 5.0,
        session = Depends(get_pg_db)
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
