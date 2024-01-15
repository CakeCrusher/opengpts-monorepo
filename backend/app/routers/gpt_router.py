import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from utils.parsers import get_user_id
from db.database import SessionLocal
from models.gpt import UpsertGpt, Gpt
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


@router.post("/gpt", response_model=Gpt)
def create_gpt(
    request: UpsertGpt,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Create a GPT instance and a corresponding staging GPT instance.

    Args:
    - request (UpsertGpt): The updated GPT data.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - Gpt: The staging GPT instance.
    """

    # Create Main GPT Instance
    main_gpt_dict = dict(request)
    main_gpt_dict["metadata"] = {
        **dict(request.metadata),
        "is_staging": False,
    }
    main_gpt = client.beta.assistants.create(**main_gpt_dict)

    # Create Staging GPT Instance
    staging_gpt_dict = dict(request)
    staging_gpt_dict["metadata"] = {
        **dict(request.metadata),
        "is_staging": True,
        "ref": main_gpt.id,
    }
    staging_gpt = client.beta.assistants.create(**staging_gpt_dict)

    staging_user_gpt = crud.create_user_gpt(
        db=db,
        user_gpt=schemas.UserGpt(user_id=user_id, gpt_id=staging_gpt.id),
    )

    print("staging_user_gpt", staging_user_gpt)

    return staging_gpt


@router.get("/gpt", response_model=List[Gpt])
def list_gpts(query: Optional[str] = None):
    """
    Get a list of all GPT assistants.

    Args:
    - query (str): The query to filter by.

    Returns:
    - List[Gpt]: The list of GPTs.
    """
    assistants = client.beta.assistants.list()
    # # USE FOR METADATA ERRORS: Useful for for whenever there are changes to
    # # Metadata structure
    # for assistant in assistants.data:
    #     print("deleting", assistant)
    #     client.beta.assistants.delete(assistant.id)
    all_gpts = [Gpt(**dict(assistant)) for assistant in assistants.data]
    if query:
        filtered_gpts = [
            gpt
            for gpt in all_gpts
            if (gpt.description and query in gpt.description)
        ]
        return filtered_gpts
    return [Gpt(**dict(assistant)) for assistant in assistants.data]


@router.patch("/gpt/{assistant_id}/update", response_model=Gpt)
def update_gpt(
    assistant_id,
    request: UpsertGpt,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Save your staging GPT.

    Args:
    - assistant_id (str): The ID of the assistant to update.
    - request (UpsertGpt): The updated GPT data.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - Gpt: The updated GPT instance.
    """

    user_gpt = crud.get_user_gpt(db=db, user_id=user_id, gpt_id=assistant_id)

    if not user_gpt:
        raise HTTPException(
            status_code=404,
            detail="User does not have access to this GPT instance.",
        )

    # Update the staging GPT Assistant
    updated_gpt_dict = dict(request)
    updated_gpt_dict["metadata"] = dict(request.metadata)
    updated_gpt = client.beta.assistants.update(
        assistant_id, **updated_gpt_dict
    )

    return updated_gpt


@router.patch("/gpt/{assistant_id}/publish", response_model=tuple[Gpt, Gpt])
def publish_gpt(
    assistant_id,
    request: UpsertGpt,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Save your staging GPT and publish to its corresponding main GPT.

    Args:
    - assistant_id (str): The ID of the assistant to update.
    - request (UpsertGpt): The updated GPT data.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - tuple[Gpt, Gpt]: The updated staging then main GPT instances.
    """

    user_gpt = crud.get_user_gpt(db=db, user_id=user_id, gpt_id=assistant_id)

    if not user_gpt:
        raise HTTPException(
            status_code=404,
            detail="User does not have access to this GPT instance.",
        )

    request_gpt = client.beta.assistants.retrieve(assistant_id)

    print("REQUEST GPT", dict(request_gpt))

    # Update the staging GPT Assistant
    updated_staging_gpt_dict = dict(request)
    updated_staging_gpt_dict["metadata"] = {
        **dict(request.metadata),
        "is_staging": True,
        "ref": request_gpt.metadata["ref"],
    }

    updated_staging_gpt = client.beta.assistants.update(
        assistant_id, **updated_staging_gpt_dict
    )

    # Update the main GPT Assistant
    updated_main_gpt_dict = updated_staging_gpt_dict
    updated_main_gpt_dict["metadata"]["is_staging"] = False
    del updated_main_gpt_dict["metadata"]["ref"]

    updated_main_gpt = client.beta.assistants.update(
        request_gpt.metadata["ref"], **updated_main_gpt_dict
    )

    # # OBSERVABILITY: find assistant with id ==
    # # updated_gpt_dict["metadata"]["ref"]
    # all_assistants = client.beta.assistants.list()
    # main_gpt = [
    #     assistant
    #     for assistant in all_assistants.data
    #     if assistant.id == request_gpt.metadata["ref"]
    # ][0]

    return (updated_staging_gpt, updated_main_gpt)
