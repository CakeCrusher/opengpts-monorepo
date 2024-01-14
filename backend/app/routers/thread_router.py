import os

# from typing import List, Optional
# from fastapi import APIRouter
from openai import OpenAI

# from pydantic import BaseModel
# from models.gpt import Gpt
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
