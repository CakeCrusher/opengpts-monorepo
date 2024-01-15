from openai.types.beta.assistant import (
    ToolCodeInterpreter,
    ToolRetrieval,
)

# from openai.types.beta.thread import Thread
from openai.types.beta.threads import ThreadMessage as OpenaiThreadMessage
from pydantic import BaseModel
from typing import Union

Tool = Union[ToolCodeInterpreter, ToolRetrieval]


class ThreadMessage(OpenaiThreadMessage):
    pass


# Thread
class ThreadMetadata(BaseModel):
    gpt_id: str = None
    title: str = None
    last_updated: int = None


class CustomThread(BaseModel):
    id: str
    created_at: int
    metadata: ThreadMetadata


class UpsertCustomThread(BaseModel):
    pass


class CreateThreadMessage(BaseModel):
    content: str
