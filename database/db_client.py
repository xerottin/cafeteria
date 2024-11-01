from datetime import timedelta
from database.base import get_pg_db
from models import Client
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from schemas.client import ClientCreate, ClientUpdate
from auth.oauth2 import hash_password, create_access_token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES


def create_client(data: ClientCreate, db: Session = Depends(get_pg_db)):
    exist_client = db.query(Client).filter_by(username=data.username).first()
    if exist_client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    hashed_password = hash_password(data.password)
    new_client = Client(username=data.username, password=hashed_password)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": data.username}, expires_delta=access_token_expires)

    return new_client, access_token


def get_client(pk: int, db: Session):
    client = db.query(Client).filter_by(id=pk).first()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client

def edit_client(db: Session, pk: int, data: ClientUpdate ):
    client = db.query(Client).filter_by(id=pk).first()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    if data.username:  client.username = data.username
    if data.password:  client.password = data.password
    if data.phone:  client.phone = data.phone
    if data.url: client.url = data.url
    if data.logo: client.logo = data.logo
    if data.company_id: client.company_id = data.company_id
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, pk: int):
    client = db.query(Client).filter_by(id=pk).first()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    client.is_active = False
    db.commit()
    db.refresh(client)
    return client