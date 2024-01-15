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


class GptMetadata(BaseModel):
    user_name: str
    # TODO: add GPT image
    visibility: Visibility
    is_staging: bool
    ref: Optional[str] = None


class UpsertGptMetadata(BaseModel):
    user_name: str
    visibility: Visibility


class Gpt(BaseModel):
    id: Optional[str]
    description: Optional[str]
    file_ids: list
    instructions: Optional[str]
    metadata: GptMetadata
    name: str
    model: Model
    tools: List[Tool]


class UpsertGpt(BaseModel):
    description: Optional[str]
    file_ids: List[str]
    instructions: Optional[str]
    metadata: UpsertGptMetadata
    name: str
    model: Model
    tools: List[Tool]
