from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


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
