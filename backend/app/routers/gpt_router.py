import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from utils.parsers import get_user_id
from db.database import SessionLocal
from models.gpt import UpsertGpt, GptMain, GptStaging

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


@router.post("/gpt", response_model=GptMain)
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
    main_gpt_dict["metadata"] = dict(request.metadata)
    main_gpt = openai_client.beta.assistants.create(**main_gpt_dict)

    # Create Staging GPT Instance
    staging_gpt_dict = dict(request)
    staging_gpt_dict["metadata"] = {
        **dict(request.metadata),
        "is_staging": "true",
        "ref": main_gpt.id,
    }
    staging_gpt = openai_client.beta.assistants.create(**staging_gpt_dict)

    crud.create_user_gpt(
        db=db,
        user_gpt=schemas.UserGpt(user_id=user_id, gpt_id=staging_gpt.id),
    )

    return staging_gpt


# delete all gpts
@router.delete("/gpt")
def delete_all_gpts_and_threads(
    db: Session = Depends(get_db),
):
    assistants = openai_client.beta.assistants.list()
    for assistant in assistants.data:
        openai_client.beta.assistants.delete(assistant.id)
    crud.delete_all_gpts_and_threads(db=db)
    return {"message": "All GPTs deleted."}


@router.get("/gpt", response_model=List[GptMain | GptStaging])
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
    print(
        "assistants: ",
        json.dumps(
            [assistant.model_dump() for assistant in assistants.data], indent=2
        ),
    )
    # # USE FOR METADATA ERRORS: Useful for for whenever there are changes to
    # # Metadata structure
    # for assistant in assistants.data:
    #     print("deleting", assistant)
    #     client.beta.assistants.delete(assistant.id)
    all_gpts: List[GptMain | GptStaging] = []
    for assistant in assistants.data:
        if assistant.metadata and assistant.metadata.get("is_staging"):
            all_gpts.append(GptStaging(**assistant.model_dump()))
        else:
            all_gpts.append(GptMain(**assistant.model_dump()))
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


@router.patch("/gpt/{assistant_id}/update", response_model=GptStaging)
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
    updated_gpt = openai_client.beta.assistants.update(
        assistant_id, **request.model_dump()
    )

    return updated_gpt


@router.post(
    "/gpt/{assistant_id}/publish", response_model=tuple[GptStaging, GptMain]
)
def publish_gpt(
    assistant_id,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """
    Publish your staging GPT to its corresponding main GPT.

    Args:
    - assistant_id (str): The ID of the assistant to update.

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

    request_assistant = openai_client.beta.assistants.retrieve(assistant_id)

    json_request_assistant = request_assistant.model_dump()
    del json_request_assistant["object"]
    del json_request_assistant["created_at"]
    staging_assistant = json.loads(json.dumps(json_request_assistant))
    del json_request_assistant["id"]
    main_assistant_id = json_request_assistant["metadata"]["ref"]
    del json_request_assistant["metadata"]["is_staging"]
    del json_request_assistant["metadata"]["ref"]

    updated_main_gpt = openai_client.beta.assistants.update(
        main_assistant_id, **json_request_assistant
    )

    # # OBSERVABILITY: find assistant with id ==
    # # updated_gpt_dict["metadata"]["ref"]
    # all_assistants = client.beta.assistants.list()
    # main_gpt = [
    #     assistant
    #     for assistant in all_assistants.data
    #     if assistant.id == request_gpt.metadata["ref"]
    # ][0]

    return (staging_assistant, updated_main_gpt.model_dump())


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
