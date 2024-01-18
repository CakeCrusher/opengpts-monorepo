from typing import List
from sqlalchemy.orm import Session
from db.models import User

from . import models, schemas
import uuid, bcrypt


# THREAD
def create_thread(
    db: Session, user_gpt_thread: schemas.UserGptThread
) -> models.User_gpt_thread:
    db_user_gpt_thread = models.User_gpt_thread(
        user_id=user_gpt_thread.user_id,
        gpt_id=user_gpt_thread.gpt_id,
        thread_id=user_gpt_thread.thread_id,
    )
    db.add(db_user_gpt_thread)
    db.commit()
    db.refresh(db_user_gpt_thread)
    return db_user_gpt_thread


def get_user_threads(
    db: Session, user_id: str
) -> List[models.User_gpt_thread]:
    user_gpt_threads = (
        db.query(models.User_gpt_thread)
        .filter(models.User_gpt_thread.user_id == user_id)
        .all()
    )
    return user_gpt_threads


def get_user_gpt_thread(
    db: Session, user_id: str, gpt_id: str, thread_id: str
) -> models.User_gpt_thread:
    user_gpt_thread = (
        db.query(models.User_gpt_thread)
        .filter(models.User_gpt_thread.user_id == user_id)
        .filter(models.User_gpt_thread.gpt_id == gpt_id)
        .filter(models.User_gpt_thread.thread_id == thread_id)
        .first()
    )
    return user_gpt_thread


# def create_thread_message(
#     db: Session, thread_message: schemas.ThreadMessageCreate
# ) -> models.ThreadMessage:
#     pass


# USER
def get_user(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
    
def verify_passsword(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_users(db: Session):
    all_users = db.query(models.User).all()
    return all_users


def create_user(db: Session, user: schemas.UserCreate, password: str) -> models.User:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(
        id=str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        profile_image=user.profile_image,
        # Add other fields as necessary
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# GPT
def create_user_gpt(db: Session, user_gpt: schemas.UserGpt):
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
