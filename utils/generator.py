from typing import Optional

from jose import jwt, JWTError
from pydantic import ValidationError

from database.hash import Hash
from settings import SECRET_KEY, ALGORITHM


def extract_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (JWTError, ValidationError) as e:
        raise e


def no_bcrypt(password: Optional[str] = None) -> str | None:
    if password:
        return Hash.bcrypt(password)
    return None