from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db_client
from database.base import get_pg_db
from schemas.client import ClientCreate, ClientUpdate, ClientInDB

router = APIRouter(prefix="", tags=["client"])

@router.post("/")
async def create_client(data: ClientCreate, db: Session = Depends(get_pg_db)):
    client, access_token = db_client.create_client(data, db)
    return client, access_token

@router.get("/")
async def get_client(pk: int, db: Session = Depends(get_pg_db)):
    return db_client.get_client(pk, db)

@router.put("/")
async def put_client(pk: int, data: ClientUpdate, db: Session = Depends(get_pg_db)):
    return db_client.edit_client(db, pk, data)


@router.delete("/", response_model=ClientInDB)
def delete_client(pk: int, db: Session = Depends(get_pg_db)):
    return db_client.delete_client(db, pk)