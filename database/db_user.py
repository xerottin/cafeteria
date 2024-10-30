from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from jose import jwt
from passlib.context import CryptContext

from models import User
from schemas.user import UserUpdate, UserInDB
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(db: Session, pk: int):
    user = db.query(User).filter_by(id=pk, is_active=True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def update_user(db: Session, user_id: int, user_update):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_update.username and user_update.username != user.username:
        username_taken = db.query(User).filter(User.username == user_update.username).first()
        if username_taken:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    if user_update.username:
        user.username = user_update.username
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": user.username}, expires_delta=access_token_expires)

    return UserInDB(
        username=user.username,
        access_token=access_token,
        token_type="bearer"
    )

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user