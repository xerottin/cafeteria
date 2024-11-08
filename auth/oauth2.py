from datetime import timedelta, datetime
from typing import Optional
import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, HTTPBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from database import db_admin, db_cafeteria, db_user
from database.base import get_pg_db
from schemas.admin import AdminBase
from schemas.user import CurrentUserScheme
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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


def get_current_cafeteria(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme_cafeteria), db: Session = Depends(get_pg_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = extract_token(token)
        exp = payload.get("exp")
        cafeteria_id: int = payload.get("cafeteria_id")
        if not cafeteria_id:
            raise credentials_exception from None
        token_scopes = payload.get("scopes", [])
    except (JWTError, ValidationError) as e:
        raise credentials_exception from e
    if exp < int(time.time()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired") from None
    cafeteria = db_cafeteria.get_client(db, cafeteria_id)
    if not cafeteria:
        raise credentials_exception from None
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions") from None
    return cafeteria


security_user = HTTPBearer()


def get_current_user(token: str = Depends(security_user), db: Session = Depends(get_pg_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        pk: str = payload.get("sub")
        # exp = payload.get("exp")

    except (JWTError, ValidationError) as e:
        raise credentials_exception from e
    # if exp < int(time.time()):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired") from None
    user = db_user.get_user_by_id(db, pk)
    if not user:
        raise credentials_exception from None
    user_full_scheme = CurrentUserScheme(
        id=user.id,
        username=user.username,
        image=user.image,
        email=user.email,
        phone=user.phone,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    return user_full_scheme