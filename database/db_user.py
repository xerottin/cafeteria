from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

from auth.oauth2 import hash_password, create_access_token
from database.base import get_pg_db
from models import User
from models.cafeteria import Menu, Coffee
from schemas.user import UserInDB, UserCreate, UserUpdate
from settings import ACCESS_TOKEN_EXPIRE_MINUTES


def create_user(data:UserCreate, db: Session):
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = hash_password(data.password)
    new_user = User(username=data.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": data.username}, expires_delta=access_token_expires)

    return UserInDB(
        id=new_user.id,
        username=new_user.username,
        access_token=access_token,
        token_type="bearer"
    )
def get_user(db: Session, pk: int):
    user = db.query(User).filter_by(id=pk, is_active=True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def update_user(pk: int, db: Session, user_update: UserUpdate):
    user = db.query(User).filter(User.id == pk).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_update.username:
        if user_update.username != user.username:
            username_taken = db.query(User).filter(User.username == user_update.username).first()
            if username_taken:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
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

def delete_user(db: Session, pk: int):
    user = db.query(User).filter(User.id == pk).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def get_cafeteria_menu(pk:int, db: Session):
    menu = db.query(Menu).filter(Menu.id == pk).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    return menu

def get_menu_coffee(pk:int, db: Session):
    coffee = db.query(Coffee).filter(Coffee.menu_id == pk).all()
    if not coffee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coffee not found")
    return coffee