from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from db.database import engine, SessionLocal, Base
from db.schemas import UserBase

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
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[ExtendedUserBase, Depends(get_current_active_user)]
):
    return current_user