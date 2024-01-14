# import os
# from openai import OpenAI
from fastapi import FastAPI
from routers.gpt_router import (
    router as gpt_router,
)


app = FastAPI()

app.include_router(gpt_router)
