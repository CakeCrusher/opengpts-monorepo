from openai.types.beta.assistant import Tool
from pydantic import BaseModel
from typing import Optional, List


class GptMetadata(BaseModel):
    creator_email: str
    visibility: str
    is_staging: bool
    ref: Optional[str] = None


class Gpt(BaseModel):
    id: Optional[str]
    description: Optional[str]
    file_ids: list
    instructions: Optional[str]
    metadata: GptMetadata
    name: str
    model: str
    tools: List[Tool]
