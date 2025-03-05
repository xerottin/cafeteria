from datetime import timedelta, datetime
from typing import Optional
import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from database import db_admin, db_cafeteria, db_user
from database.base import get_pg_db
from schemas.admin import AdminBase
from settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, USERNAME, PASSWORD
from utils.generator import extract_token

def create_access_token(data: dict, secret_key: str = SECRET_KEY, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="admin_token")

def get_current_admin(token: str = Depends(oauth2_scheme_admin), db: Session = Depends(get_pg_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = extract_token(token)
        username: str = payload.get("sub")
        exp = payload.get("exp")
        if not username:
            raise credentials_exception from None
    except (JWTError, ValidationError) as e:
        raise credentials_exception from e
    if exp < int(time.time()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired") from None
    if username == USERNAME:
        return AdminBase(username=USERNAME, password=PASSWORD)
    admin = db_admin.get_admin_by_username(db, username)
    if not admin:
        raise credentials_exception from None
    return admin


oauth2_scheme_cafeteria = OAuth2PasswordBearer(tokenUrl="cafeteria_token")

def get_current_cafeteria(token: str = Depends(oauth2_scheme_cafeteria), db: Session = Depends(get_pg_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = extract_token(token)
        username: str = payload.get("sub")
        exp = payload.get("exp")
        if not username:
            raise credentials_exception from None
    except (JWTError, ValidationError) as e:
        raise credentials_exception from e
    if exp < int(time.time()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired") from None
    cafeteria = db_cafeteria.get_client_username(db, username)
    if not cafeteria:
        raise credentials_exception from None
    return cafeteria


oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="user_token")

def get_current_user(token: str = Depends(oauth2_scheme_user), db: Session = Depends(get_pg_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp = payload.get("exp")
        if not username:
            raise credentials_exception from None
    except (JWTError, ValidationError) as e:
        raise credentials_exception from e
    if exp < int(time.time()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired") from None
    user = db_user.get_user_by_username(db, username)
    if not user:
        raise credentials_exception from None
    return user
