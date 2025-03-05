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


# utils.py
def update_model(data, model, fields_mapping):
    """
    Обновляет атрибуты модели на основе данных.

    :param data: объект с данными (например, Pydantic-модель или словарь)
    :param model: объект модели, который нужно обновить
    :param fields_mapping: словарь, где ключ — атрибут data, значение — атрибут модели
    """
    for data_field, model_field in fields_mapping.items():
        value = getattr(data, data_field, None)
        if value is not None:
            if data_field == "password":
                value = no_bcrypt(value)
            setattr(model, model_field, value)
