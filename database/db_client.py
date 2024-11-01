from datetime import timedelta
from database.base import get_pg_db
from models import Client
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from schemas.client import ClientCreate
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

