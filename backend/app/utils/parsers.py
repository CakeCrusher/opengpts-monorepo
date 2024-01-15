from fastapi import HTTPException, Header
from typing import Optional


def get_user_id(auth: Optional[str] = Header(None)):
    if auth:
        scheme, _, param = auth.partition(' ')
        if scheme.lower() == 'bearer' and param and len(param) > 0:
            return param
    raise HTTPException(status_code=400, detail='Invalid authorization header')


def get_optional_user_id(auth: Optional[str] = Header(None)):
    if auth:
        scheme, _, param = auth.partition(' ')
        if scheme.lower() == 'bearer':
            return param
    return None
