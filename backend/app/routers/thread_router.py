"""
TESTING
asst_UOmnQLhM5Yf1jiZx56J7bleW
thread_6XCcv97SvXjmSqPXXdmXz1mf
6e9b3cb6-5ba5-4457-abcb-e0d08546c6ae
"""

from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from utils.parsers import get_user_id
from db.database import SessionLocal
from sqlalchemy.orm import Session
from db import crud, schemas
from models.thread import (
    CreateThreadMessageResponse,
    CustomThread,
    CreateThreadMessage,
    ThreadMessage,
    ThreadMetadata,
)
from datetime import datetime
import time
from openai.pagination import SyncCursorPage
from utils.api import openai_client


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


@router.post("/gpt/{gpt_id}/thread", response_model=CustomThread)
def create_thread(
    gpt_id: str,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Create a thread.

    Args:
    - gpt_id (str): The ID of the GPT.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - CustomThread: The created thread.
    """
    thread_metadata: ThreadMetadata = {
        "gpt_id": gpt_id,
        "user_id": user_id,
        "last_updated": int(datetime.now().timestamp()),
    }
    thread = openai_client.beta.threads.create(metadata=thread_metadata)
    user_gpt_thread = schemas.UserGptThread(
        user_id=user_id,
        gpt_id=gpt_id,
        thread_id=thread.id,
    )
    crud.create_thread(db=db, user_gpt_thread=user_gpt_thread)
    return thread


@router.get("/thread", response_model=List[CustomThread])
def get_threads(
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Get user threads.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - List[CustomThread]: The list of threads.
    """
    db_threads = crud.get_user_threads(db, user_id)
    threads = []
    for db_thread in db_threads:
        thread = openai_client.beta.threads.retrieve(db_thread.thread_id)
        threads.append(thread)
    return threads


@router.post(
    "/gpt/{gpt_id}/thread/{thread_id}/messages",
    response_model=SyncCursorPage[ThreadMessage],
)
def create_thread_message(
    gpt_id: str,
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
    - SyncCursorPage[ThreadMessage]: The message history including the
      assistant response.
    """
    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=request.content,
    )
    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=gpt_id,
    )

    max_wait_iterations = 20  # (max_wait_iterations / 2) = seconds to wait
    i = 0
    while i < max_wait_iterations:
        i += 1
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )

        if run.status == "completed":
            break
        elif not (run.status == "in_progress" or run.status == "queued"):
            raise HTTPException(
                status_code=500,
                detail="GPT run failed. With status: " + run.status,
            )

        time.sleep(0.5)
    else:
        raise HTTPException(
            status_code=500,
            detail="GPT run failed. With status: " + run.status,
        )

    messages = openai_client.beta.threads.messages.list(
        thread_id=thread_id,
    )

    return messages


@router.get(
    "/gpt/{gpt_id}/thread/{thread_id}/messages",
    response_model=SyncCursorPage[ThreadMessage],
)
def get_thread_messages(
    gpt_id: str,
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
    - SyncCursorPage[ThreadMessage]: All of the messages in a the thread.
    """
    if not crud.get_user_gpt_thread(db, user_id, gpt_id, thread_id):
        raise HTTPException(
            status_code=404,
            detail="User does not have access to this thread.",
        )

    messages = openai_client.beta.threads.messages.list(
        thread_id=thread_id,
    )
    return messages


@router.post(
    "/gpt/{gpt_id}/thread/{thread_id}/run",
    response_model=CreateThreadMessageResponse,
)
def create_thread_run(
    gpt_id: str,
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
    - SyncCursorPage[ThreadMessage]: The message history including the
      assistant response.
    """
    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=request.content,
    )
    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=gpt_id,
    )

    max_wait_iterations = 20  # (max_wait_iterations / 2) = seconds to wait
    i = 0
    while i < max_wait_iterations:
        i += 1
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )

        run_steps = openai_client.beta.threads.runs.steps.list(
            thread_id=thread_id,
            run_id=run.id,
        )
        messages: Dict[str, ThreadMessage] = {}

        # Iterate over the data in run_steps
        for step in run_steps:
            # Check if the step type is 'message_creation'
            if not (
                step.status == "in_progress"
                or step.status == "queued"
                or step.status == "completed"
            ):
                raise HTTPException(
                    status_code=500,
                    detail="GPT run failed. With status: " + run.status,
                )
            if step.type == 'message_creation':
                # Retrieve the message
                message = openai_client.beta.threads.messages.retrieve(
                    thread_id=step.thread_id,
                    message_id=step.step_details.message_creation.message_id,
                )
                # Map the message to the message_id in the hash map
                messages[
                    step.step_details.message_creation.message_id
                ] = message.model_dump()
                # Pydandtic does not recognize the ThreadMessage object,
                # so it must be serialized

        json_run_steps = run_steps.model_dump()
        if len(json_run_steps["data"]) and any(
            [
                step["type"] == "message_creation"
                and step["status"] == "completed"
                for step in json_run_steps["data"]
            ]
        ):
            break

        time.sleep(0.5)
    else:
        raise HTTPException(
            status_code=500,
            detail="GPT run failed. With status: " + run.status,
        )

    return CreateThreadMessageResponse(
        messages=messages,
        run_steps=run_steps,
    )
