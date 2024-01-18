from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.schemas import UserBase, ExtendedUserBase
from db.crud import get_user_by_username, verify_password
from .security import create_access_token, get_current_user
import bcrypt
import jwt

db = SessionLocal()

from typing import Optional
from pydantic import BaseModel
from db.schemas import UserBase

class ExtendedUserBase(UserBase):
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    disabled: Optional[bool] = None
    
class UserInDB(ExtendedUserBase):
    hashed_password: str

fake_users_db = {
   "johndoe": { ExtendedUserBase(username="chad" ,
                                 email="john@doe.com", 
                                 name="John Doe", 
                                 profile_image=None,
                                 hashed_password="fakehashedsecret",
                                 disabled=False,)},
   "alice": { ExtendedUserBase(username="alice" ,
                               email="alice@alice.com", 
                               name="Alice", 
                               profile_image=None,
                               hashed_password="fakehashedsecret",
                               disabled=False,)},
        
}

app = FastAPI()

def fake_hash_password(password: str):
    return f"fakehashed{password}"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return ExtendedUserBase(**user_dict)
    
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if user := fake_decode_token(token):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
async def get_current_active_user(
    current_user: Annotated[ExtendedUserBase, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Authenticate  

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: ExtendedUserBase = Depends(get_current_user)):
    return current_user
