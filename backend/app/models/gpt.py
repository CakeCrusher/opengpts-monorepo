from enum import Enum
from openai.types.beta.assistant import (
    ToolCodeInterpreter,
    ToolRetrieval,
)
from pydantic import BaseModel
from typing import Optional, List, Union

Tool = Union[ToolCodeInterpreter, ToolRetrieval]


class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class Model(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"


# TODO: align GPT with assistant
class GptMainMetadata(BaseModel):
    user_name: str
    # TODO: add GPT image
    visibility: Visibility


class GptStagingMetadata(GptMainMetadata):
    is_staging: str
    ref: str


class GptMain(BaseModel):
    id: Optional[str]
    description: Optional[str]
    file_ids: list[str]
    # TODO: need to fetch filenames
    instructions: Optional[str]
    metadata: GptMainMetadata
    name: str
    model: str  # TODO: make enum
    tools: List[Tool]


class GptStaging(BaseModel):
    id: Optional[str]
    description: Optional[str]
    file_ids: list[str]
    # TODO: need to fetch filenames
    instructions: Optional[str]
    metadata: GptStagingMetadata
    name: str
    model: str  # TODO: make enum
    tools: List[Tool]


class UpsertGpt(BaseModel):
    description: Optional[str]
    file_ids: List[str]
    instructions: Optional[str]
    metadata: GptMainMetadata
    name: str
    model: Model
    tools: List[Tool]
