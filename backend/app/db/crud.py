from sqlalchemy.orm import Session
from . import models, schemas
import uuid


# def get_user(db: Session):
#     return db.query(models.Item).all()


def get_users(db: Session):
    all_users = db.query(models.User).all()
    return all_users


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(id=str(uuid.uuid4()), email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_gpt(db: Session, user_gpt: models.User_gpt):
    db_user_gpt = models.User_gpt(
        user_id=user_gpt.user_id, gpt_id=user_gpt.gpt_id
    )
    db.add(db_user_gpt)
    db.commit()
    db.refresh(db_user_gpt)
    return db_user_gpt
