import os
from typing import List, Optional
from fastapi import APIRouter, Depends
from openai import OpenAI
from pydantic import BaseModel
from db.database import SessionLocal
from models.gpt import Gpt
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from db import crud, schemas

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class GptRequest(BaseModel):
    user_id: str
    gpt: Gpt


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/gpt", response_model=Gpt)
def create_gpt(request: GptRequest, db: Session = Depends(get_db)):
    """
    Create a GPT instance and a corresponding staging GPT instance.

    Args:
    - creator_email (str): Email of the creator.

    Returns:
    - Gpt: The staging GPT instance.
    """

    # Create Main GPT Instance
    main_gpt_dict = dict(request.gpt)
    main_gpt_dict["metadata"] = {
        **dict(request.gpt.metadata),
        "is_staging": False,
    }
    del main_gpt_dict["id"]
    main_gpt = client.beta.assistants.create(**main_gpt_dict)

    # Create Staging GPT Instance
    staging_gpt_dict = dict(request.gpt)
    staging_gpt_dict["metadata"] = {
        **dict(request.gpt.metadata),
        "is_staging": True,
        "ref": main_gpt.id,
    }
    del staging_gpt_dict["id"]
    staging_gpt = client.beta.assistants.create(**staging_gpt_dict)

    crud.create_user_gpt(
        db=db,
        user_gpt=schemas.UserGpt(
            user_id=request.user_id, gpt_id=staging_gpt.id
        ),
    )

    return staging_gpt


@router.get("/gpt", response_model=List[Gpt])
def list_gpts(query: Optional[str] = None):
    """
    Get a list of all GPT assistants.

    Args:
    - query (str): The query to filter by.

    Returns:
    - List[Gpt]: The list of GPT instances.
    """
    assistants = client.beta.assistants.list()
    all_gpts = [Gpt(**dict(assistant)) for assistant in assistants.data]
    if query:
        filtered_gpts = [
            gpt
            for gpt in all_gpts
            if (gpt.description and query in gpt.description)
        ]
        return filtered_gpts
    return [Gpt(**dict(assistant)) for assistant in assistants.data]


@router.patch("/gpt/{assistant_id}", response_model=Gpt)
def update_gpt(assistant_id, request: GptRequest):
    """
    Update an existing GPT assistant.

    Args:
    - assistant_id (str): The ID of the assistant to update.
    - request (GptRequest): The updated GPT data.

    Returns:
    - Gpt: The updated GPT instance.
    """
    print("request", request)

    # Update the GPT Assistant
    updated_gpt_dict = dict(request.gpt)
    updated_gpt_dict["metadata"] = dict(request.gpt.metadata)
    del updated_gpt_dict["id"]
    updated_gpt = client.beta.assistants.update(
        assistant_id, **updated_gpt_dict
    )

    return updated_gpt
