from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    profile_image: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserGpt(BaseModel):
    user_id: str
    gpt_id: str


class User(UserBase):
    id: str
    email: str
    user_gpts: list[UserGpt] = []

    class Config:
        orm_mode = True


class UserGptThread(BaseModel):
    user_id: str
    gpt_id: str
    thread_id: str

    class Config:
        orm_mode = True
