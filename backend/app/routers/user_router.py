import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from openai import OpenAI
from utils.parsers import get_optional_user_id
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


@router.post("/users", response_model=schemas.SafeUser)
def create_user(
    response: Response,
    user: Optional[schemas.UserCreate] = None,
    user_id: str = Depends(get_optional_user_id),
    db: Session = Depends(get_db),
):
    """
    Create a new user.
    Args:
    - user (Optional[schemas.UserCreate]): The new user's details.
    Headers:
    - auth (Optional[str]): Bearer <USER_ID>
    Returns:
    - Response: A response with the 'auth' header set to 'Bearer {user_id}'
      and the created user in the body.
    """
    if user_id:
        db_user = crud.get_user(db=db, user_id=user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        db_user = crud.create_user(db=db, user=user)

    response.headers["auth"] = f"Bearer {db_user.id}"

    return schemas.SafeUser(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        profile_image=db_user.profile_image,
    )


@router.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.

    Returns:
    - List[schemas.User]: The list of users.
    """
    db_users = crud.get_users(db)
    return db_users
