from fastapi import FastAPI
from routers import gpt_router, user_router, thread_router
from db.database import engine
from db import models

app = FastAPI()

# # TODO: Remove this in production
# models.Base.metadata.drop_all(bind=engine)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(gpt_router.router)
app.include_router(user_router.router)
app.include_router(thread_router.router)
