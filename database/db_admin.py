from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Admin
from schemas.admin import AdminCreate
from utils.generator import no_bcrypt


def create_admin(db: Session, data: AdminCreate):
    exist_admin = db.query(Admin).filter_by(username=data.username).first()
    if exist_admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    new_admin = Admin(username=data.username, password=no_bcrypt(data.password))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin