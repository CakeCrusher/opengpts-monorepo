from typing import List
from sqlalchemy.orm import Session
from db.models import User

from . import models, schemas
import uuid, bcrypt


# THREAD

def create_thread(
    db: Session, user_gpt_thread: schemas.UserGptThread
) -> models.User_gpt_thread:
    """
    Create a new thread for a user GPT.

    Args:
        db (Session): The database session.
        user_gpt_thread (schemas.UserGptThread): The user GPT thread schema with user_id, gpt_id, and thread_id.

    Returns:
        models.User_gpt_thread: The created user GPT thread object.
    """
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
    """
    Retrieve all threads for a given user.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user.

    Returns:
        List[models.User_gpt_thread]: A list of user GPT threads.
    """





def get_user_gpt_thread(
    db: Session, user_id: str, gpt_id: str, thread_id: str
) -> models.User_gpt_thread:
    """
    Retrieve a specific thread for a user GPT.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user.
        gpt_id (str): The ID of the GPT.
        thread_id (str): The ID of the thread.

    Returns:
        models.User_gpt_thread: The user GPT thread object if found, otherwise None.
    """
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

def get_user(db: Session, user_id: str) -> models.User:
    """
    Retrieve a user by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to retrieve.

    Returns:
        models.User: The user object if found, otherwise None.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

def get_user_by_username(db: Session, username: str) -> models.User:
    """
    Retrieve a user by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        models.User: The user object if found, otherwise None.
    """

    

def verify_passsword(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


def get_users(db: Session) -> List[models.User]:
    """
    Retrieve all users.

    Args:
        db (Session): The database session.

    Returns:
        List[models.User]: A list of all user objects.
    """
    all_users = db.query(models.User).all()
    return all_users



def create_user(db: Session, user: schemas.UserCreate, password: str) -> models.User:
    """
    Create a new user with the given details and password.

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user details.
        password (str): The plain text password for the user.

    Returns:
        models.User: The created user object.
    """
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

def create_user_gpt(db: Session, user_gpt: schemas.UserGpt) -> models.User_gpt:
    """
    Create a new user GPT association.

    Args:
        db (Session): The database session.
        user_gpt (schemas.UserGpt): The user GPT schema with user_id and gpt_id.

    Returns:
        models.User_gpt: The created user GPT object.
    """
    db_user_gpt = models.User_gpt(
        user_id=user_gpt.user_id, gpt_id=user_gpt.gpt_id
    )
    db.add(db_user_gpt)
    db.commit()
    db.refresh(db_user_gpt)
    return db_user_gpt

def get_user_gpts(db: Session, user_id: str) -> list[models.User_gpt]:
    """
    Retrieve all GPT associations for a given user.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user.

    Returns:
        list[models.User_gpt]: A list of user GPT objects.
    """
    user_gpts = (
        db.query(models.User_gpt)
        .filter(models.User_gpt.user_id == user_id)
        .all()
    )
    return user_gpts



def get_user_gpt(db: Session, user_id: str, gpt_id: str) -> models.User_gpt:
    """
    Retrieve a specific GPT association for a user.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user.
        gpt_id (str): The ID of the GPT.

    Returns:
        models.User_gpt: The user GPT object if found, otherwise None.
    """
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
