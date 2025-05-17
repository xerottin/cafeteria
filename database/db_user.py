import json

from fastapi import HTTPException, status
from fastapi.openapi.models import Response
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.base import redis_client
from models import User
from models.cafeteria import Menu, Coffee
from models.user import Order, OrderItem, Favorite
from schemas.user import UserCreate, UserUpdate, OrderCreate
from utils.generator import generate_verification_code

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, data: UserCreate):
    exist_user = db.query(User).filter_by(username=data.username).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    verification_code = generate_verification_code()

    new_user = User(
        username=data.username,
        name=data.name,
        password=pwd_context.hash(data.password),
        email=data.email,
        phone=data.phone,
        image=data.image,
        is_verified=False,
        verification_code=verification_code
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"Код подтверждения для {new_user.username}: {verification_code}")

    return new_user

def verify_user(db: Session, username: str, code: str):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")

    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    user.is_verified = True
    user.verification_code = None

    db.commit()
    return {"message": "User successfully verified"}

def get_user_by_id(db: Session, pk: int):
    user = db.query(User).filter_by(id=pk, is_active=True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter_by(username=username, is_active=True).first()


def update_user(db: Session, pk: int, data: UserUpdate):
    if data.username == 'admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")

    user = db.query(User).filter(User.id == pk, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if data.username and data.username != user.username:
        exists = db.query(User).filter(User.username == data.username, User.is_active == True).first()
        if exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    update_data = data.dict(exclude_unset=True)  # Исключаем None
    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

    return user


def delete_user(db: Session, pk: int):
    user = db.query(User).filter(User.id == pk, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    db.commit()
    db.refresh(user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)



def get_cafeteria_menus(pk: int, db: Session):
    menu = db.query(Menu).filter(Menu.cafeteria_id == pk).all()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    return menu


def get_menu_coffee(pk: int, db: Session):
    coffee = db.query(Coffee).filter(Coffee.menu_id == pk).all()
    if not coffee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coffee not found")
    return coffee


def create_order_user(data: OrderCreate, db: Session, pk: int):
    new_order = Order(
        cafeteria_id=data.cafeteria_id,
        user_id=pk,
        status=data.status,
    )
    for item_data in data.order_items:
        order_item = OrderItem(
            coffee_id=item_data.coffee_id,
            quantity=item_data.quantity
        )
        new_order.order_items.append(order_item)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def get_user_archive(user_id: int, db: Session):
    archive = redis_client.lrange(f"user:{user_id}:archives", 0, -1)
    return [json.loads(order) for order in archive]


def create_favourite(user_id: int, coffee_id: int, db: Session):
    new_fav = Favorite(
        user_id=user_id,
        coffee_id=coffee_id
    )
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav

#to-do not working
def get_my_fav(user_id: int, db: Session):
    fav = db.query(Favorite).filter_by(user_id=user_id).all()
    if not fav:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favourite not found")
    return fav

