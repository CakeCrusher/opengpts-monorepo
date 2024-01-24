from jose import jwt
import os


def get_token(token: str):
    """
    Function to get the token.
    Parameters:
    - token: str, the token
    Returns:
    - str: the token
    """

    return jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
