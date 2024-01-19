import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, FastAPI, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN
from .config import settings
from .dependencies import get_db
from .security import get_current_active_user
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from .config import settings
from .security import create_access_token, 
from db.crud import get_user_by_username, verify_password
from db.schemas import UserInDB
from db.database import get_db

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return UserInDB(**user.__dict__)    

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Logs a user in and returns an access token.

    Parameters:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (Session): The database session.

    Returns:
        str: The access token.

    Raises:
        HTTPException: If the username or password is incorrect.
    """
    Session = Depends(get_db):
    user = get_user_by_username(db, username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Security(get_current_active_user)):
    """
    An asynchronous function that handles the GET request for the "/users/me" endpoint.
    The function expects a parameter called `current_user` of type `UserInDB`, which represents the currently authenticated user.
    The function returns an instance of `UserInDB`, which represents the details of the currently authenticated user.
    """
    return current_user





