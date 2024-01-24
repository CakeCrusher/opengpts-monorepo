from fastapi import FastAPI
from routers import gpt_router, user_router, thread_router, auth_router
from db.database import engine
from db import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # TODO: Remove this in production
# models.Base.metadata.drop_all(bind=engine)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(gpt_router.router)
app.include_router(user_router.router)
app.include_router(thread_router.router)
