import os
from typing import List
from fastapi import APIRouter, Depends
from openai import OpenAI
from db.database import SessionLocal
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from db import crud, schemas

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    (The user's ID will be tentatively used for authentication"""
    +"""by passing it to the headers of relevant endpoints.)

    Args:
    - user (schemas.UserCreate): The new user's details.

    Returns:
    - schemas.User: The created user.
    """
    db_user = crud.create_user(db=db, user=user)
    return db_user


@router.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.

    Returns:
    - List[schemas.User]: The list of users.
    """
    db_users = crud.get_users(db)
    return db_users
