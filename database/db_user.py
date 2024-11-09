from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import User
from models.cafeteria import Menu, Coffee
from schemas.user import UserCreate, UserUpdate
from utils.generator import no_bcrypt


def create_user(db: Session, data: UserCreate) -> User:
    exist_user = db.query(User).filter_by(username=data.username, is_active=True).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    new_user = User(
        username=data.username,
        password=data.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
def get_user_by_id(db: Session, pk: int):
    user = db.query(User).filter_by(id=pk, is_active=True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter_by(username=username, is_active=True).first()

def update_user(db: Session, pk: int, data: UserUpdate):
    if data.username == 'admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong username or password')
    same_user = db.query(User).filter_by(username=data.username, is_active=True).first()
    if same_user and same_user.id != pk:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already exists")
    user = db.query(User).filter_by(id=pk, is_active=True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if data.email: user.email = data.email
    if data.phone: user.phone = data.phone
    if data.image: user.image = data.image
    if data.password: user.password = no_bcrypt(data.password)
    db.commit()
    db.refresh(user)
    return user

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
