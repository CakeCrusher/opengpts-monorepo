from jose import jwt
from datetime import datetime, timedelta
from datetime import timezone
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
from app.db import crud, models, schemas
from app.db.database import SessionLocal
import requests
import os
import dotenv
dotenv.load_dotenv()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")


# This is the URL of your domain name plus /login/google

app.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/login/google")
async def login_google():
    """
Handles the Google login process.

Returns:
    dict: A dictionary containing the login URL.

Examples:
    >>> login_google()
    {'url': 'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline'}
"""    
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/auth/google")
async def auth_google(code: str, db: Session = Depends(get_db)):
    """
        Async function for authenticating with Google using the provided code.
    Parameters:
    - code: str, the authentication code
    - db: Session, the database session
    Returns:
    - dict: containing the access token, token type, and user information
           or containing an error message if an authentication error occurs.
    Raises:
    - requests.exceptions.RequestException: if an error occurs during the authentication process.
    """
    try:
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        access_token = response.json().get("access_token")
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info.raise_for_status()
        user_info = user_info.json()

        user = get_or_create_user(db, user_info)
        access_token = generate_access_token(user)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user,
        }
    except requests.exceptions.RequestException:
        return {
            "error": "An error occurred during the authentication process."
        }


def get_or_create_user(db: Session, user_info: dict) -> models.User:
    """
    Function to get or create a user in the database.
    Parameters:
    - db: Session, the database session
    - user_info: dict, the user information
    Returns:
    - models.User: the user object
    """
    user = crud.find_user(db, email=user_info["email"])
    if not user:
        user_create = schemas.UserCreate(
            email=user_info["email"],
            name=user_info["name"],
            picture=user_info["picture"],
        )
        user = crud.create_user(db, user_create)
    return user

def generate_access_token(user: models.User) -> str:
    """
    Function to generate an access token for the user.
    Parameters:
    - user: models.User, the user object
    Returns:
    - str: the access token
    """
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Function to create an access token for the user.
    Parameters:
    - data: dict, the data to be encoded in the token
    - expires_delta: timedelta, the expiration time of the token
    Returns:
    - str: the access token
    """
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

@app.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    """
    Function to get the token.
    Parameters:
    - token: str, the token
    Returns:
    - str: the token
    """
    
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)