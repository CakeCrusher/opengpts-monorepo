import os
from typing import List, Optional
from fastapi import APIRouter, Depends
from openai import OpenAI
from utils.parsers import get_user_id
from db.database import SessionLocal
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from db import crud
from models.thread import CustomThread, CreateThreadMessage, ThreadMessage

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# th = client.beta.threads.retrieve("th-1Y2J5Z5QX1QJ5")
# msgs = client.beta.threads.messages.list(th.id)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/thread", response_model=CustomThread)
def create_thread(
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Create a thread.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - CustomThread: The created thread.
    """
    db_thread = crud.create_thread(db=db, user_id=user_id)
    return db_thread


@router.get("/thread", response_model=List[CustomThread])
def get_threads(
    query: Optional[str] = None,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Get all threads.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - List[CustomThread]: The list of threads.
    """
    db_threads = crud.get_threads(db, query, user_id)
    return db_threads


@router.get("/thread/{thread_id}/messages", response_model=List[ThreadMessage])
def get_thread_messages(
    thread_id: str,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Get all messages in a thread.

    Args:
    - thread_id (str): The ID of the thread.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - Gpt: The thread.
    """
    db_thread = crud.get_thread(db, thread_id)
    return db_thread


@router.post("/thread/{thread_id}/messages", response_model=ThreadMessage)
def create_thread_message(
    thread_id: str,
    request: CreateThreadMessage,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Create a message in a thread.

    Args:
    - request (CreateThreadMessage): The message to create.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - ThreadMessage: The created message.
    """
    db_thread = crud.create_thread_message(db, thread_id, request)
    return db_thread
