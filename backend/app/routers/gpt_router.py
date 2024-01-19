from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from utils.parsers import get_user_id
from db.database import SessionLocal
from models.gpt import UpsertGpt, Gpt

from sqlalchemy.orm import Session
from db import crud, schemas
from openai.types import FileObject
from utils.api import openai_client

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
    main_gpt = openai_client.beta.assistants.create(**main_gpt_dict)

    # Create Staging GPT Instance
    staging_gpt_dict = dict(request)
    staging_gpt_dict["metadata"] = {
        **dict(request.metadata),
        "is_staging": True,
        "ref": main_gpt.id,
    }
    staging_gpt = openai_client.beta.assistants.create(**staging_gpt_dict)

    crud.create_user_gpt(
        db=db,
        user_gpt=schemas.UserGpt(user_id=user_id, gpt_id=staging_gpt.id),
    )

    return staging_gpt


@router.get("/gpt", response_model=List[Gpt])
def list_gpts(
    query: Optional[str] = None,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get a list of all GPT assistants.

    Args:
    - query (str): The query to filter by.
    - user_id (str): The user ID to filter by.

    Returns:
    - List[Gpt]: The list of GPTs.
    """
    assistants = openai_client.beta.assistants.list()
    # # USE FOR METADATA ERRORS: Useful for for whenever there are changes to
    # # Metadata structure
    # for assistant in assistants.data:
    #     print("deleting", assistant)
    #     client.beta.assistants.delete(assistant.id)
    all_gpts = [Gpt(**dict(assistant)) for assistant in assistants.data]
    if query:
        all_gpts = [
            gpt
            for gpt in all_gpts
            if (gpt.description and query in gpt.description)
        ]
    if user_id:
        all_user_gpts = crud.get_user_gpts(db=db, user_id=user_id)
        all_gpts = [
            gpt
            for gpt in all_gpts
            if any(user_gpt.gpt_id == gpt.id for user_gpt in all_user_gpts)
        ]
    return all_gpts


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
    updated_gpt = openai_client.beta.assistants.update(
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

    request_gpt = openai_client.beta.assistants.retrieve(assistant_id)

    # Update the staging GPT Assistant
    updated_staging_gpt_dict = dict(request)
    updated_staging_gpt_dict["metadata"] = {
        **dict(request.metadata),
        "is_staging": True,
        "ref": request_gpt.metadata["ref"],
    }

    updated_staging_gpt = openai_client.beta.assistants.update(
        assistant_id, **updated_staging_gpt_dict
    )

    # Update the main GPT Assistant
    updated_main_gpt_dict = updated_staging_gpt_dict
    updated_main_gpt_dict["metadata"]["is_staging"] = False
    del updated_main_gpt_dict["metadata"]["ref"]

    updated_main_gpt = openai_client.beta.assistants.update(
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


@router.post("/gpt/file", response_model=FileObject)
async def upload_file(file: UploadFile, user_id: str = Depends(get_user_id)):
    """
    Upload a file to Assistants API.

    Args:
    - file (UploadFile): The file to upload.

    Headers:
    - auth (str): Bearer <USER_ID>

    Returns:
    - FileObject: Object containing file id and other details.
    """
    content = await file.read()
    assistant_file = openai_client.files.create(
        file=(file.filename, content),
        purpose='assistants',
        # metadata={
        #     "user_id": user_id,
        # },
    )
    return assistant_file


@router.get("/gpt/file/{file_id}", response_model=FileObject)
async def get_uploaded_file(file_id: str, user_id: str = Depends(get_user_id)):
    assistant_file = openai_client.files.retrieve(
        file_id=file_id,
    )
    # if assistant_file.metadata["user_id"] != user_id:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="User does not have access to this file.",
    #     )
    return assistant_file
