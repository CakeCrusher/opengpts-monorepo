"""
TESTING
asst_H8r6928abxcTsq3XP5qRXCBD
thread_KFd3jsCK5LjSMVQfkrBQnQss
bearer 99d834cd-b052-4d56-9914-818aacca8533
{
  "content": "Please solve [1 2 3;4 5 6] x [7 8;9 10;11 12]"
}
"""

import json
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from utils.parsers import get_user_id
from db.database import SessionLocal
from sqlalchemy.orm import Session
from db import crud, schemas
from models.thread import (
    RunStepsResponse,
    CustomThread,
    CreateThreadMessage,
    ThreadMessage,
    ThreadMetadata,
)
from datetime import datetime
import time
from openai.pagination import SyncCursorPage
from utils.api import get_run_steps_and_messages, openai_client


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


# TODO: takes a while to retrieve, transform this to a stream
@router.get(
    "/gpt/{gpt_id}/thread/{thread_id}/run",
    response_model=RunStepsResponse,
)
def get_thread_runs(
    gpt_id: str,
    thread_id: str,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Get all run steps in a thread.

    Args:
    - gp_id (str): The ID of the GPT.
    - thread_id (str): The ID of the thread.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - RunStepsResponse: The run steps in the thread and a hash map of
      messages.
    """
    runs = openai_client.beta.threads.runs.list(
        thread_id=thread_id,
    )
    print("RUNS: ", json.dumps(runs.model_dump(), indent=2))
    messages: Dict[str, ThreadMessage] = {}
    aggregated_run_steps = []

    for run in runs:
        run_steps_response = get_run_steps_and_messages(
            openai_client, thread_id, run.id
        )

        aggregated_run_steps.extend(run_steps_response.run_steps)
        messages.update(run_steps_response.messages)

    return RunStepsResponse(
        messages=messages,
        run_steps=aggregated_run_steps,
    )


def check_step_status(step):
    if not (
        step.status == "in_progress"
        or step.status == "queued"
        or step.status == "completed"
    ):
        raise HTTPException(
            status_code=500,
            detail="GPT run failed. With status: " + step.status,
        )


@router.post(
    "/gpt/{gpt_id}/thread/{thread_id}/run",
    response_model=RunStepsResponse,
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
    - RunStepsResponse: The run steps in the run and a hash map of
      messages.
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

        run_steps_response = get_run_steps_and_messages(
            openai_client, thread_id, run.id, check_step_status
        )

        json_run_steps = [
            step.model_dump() for step in run_steps_response.run_steps
        ]
        if len(json_run_steps) and all(
            [step["status"] == "completed" for step in json_run_steps]
        ):
            break

        time.sleep(0.5)
    else:
        raise HTTPException(
            status_code=500,
            detail="GPT run timed out.",
        )

    return run_steps_response
