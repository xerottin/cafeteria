from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import db_client
from database.base import get_pg_db
from schemas.client import ClientCreate

router = APIRouter(prefix="", tags=["client"])

@router.post("/")
async def create_client(data: ClientCreate, db: Session = Depends(get_pg_db)):
    client, access_token = db_client.create_client(data, db)
    return client, access_token
