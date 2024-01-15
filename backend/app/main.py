from fastapi import FastAPI
from routers import gpt_router, user_router
from db.database import engine
from db import models

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(gpt_router.router)
app.include_router(user_router.router)
