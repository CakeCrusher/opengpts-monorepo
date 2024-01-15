from typing import List
from sqlalchemy.orm import Session

from models.thread import CustomThread
from . import models, schemas
import uuid


# THREAD
def create_thread(db: Session, user_id: str) -> CustomThread:
    pass
    # TODO: THREAD create a thread


def get_threads(db: Session, query: str, user_id: str) -> List[CustomThread]:
    pass
    # TODO: THREAD get all threads


# def create_thread_message(
#     db: Session, thread_message: schemas.ThreadMessageCreate
# ) -> models.ThreadMessage:
#     pass


# GPT
def get_users(db: Session):
    all_users = db.query(models.User).all()
    return all_users


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        id=str(uuid.uuid4()),
        email=user.email,
        name=user.name,
        profile_image=user.profile_image,
    )
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


def get_user_gpts(db: Session, user_id: str) -> list[models.User_gpt]:
    user_gpts = (
        db.query(models.User_gpt)
        .filter(models.User_gpt.user_id == user_id)
        .all()
    )
    return user_gpts


def get_user_gpt(db: Session, user_id: str, gpt_id: str) -> models.User_gpt:
    all_user_gpts = (
        db.query(models.User_gpt)
        .filter(models.User_gpt.user_id == user_id)
        .all()
    )
    print("all_user_gpts", [str(user_gpt) for user_gpt in all_user_gpts])
    user_gpt = (
        db.query(models.User_gpt)
        .filter(models.User_gpt.user_id == user_id)
        .filter(models.User_gpt.gpt_id == gpt_id)
        .first()
    )
    return user_gpt
