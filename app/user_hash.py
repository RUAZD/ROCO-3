import os
from passlib.context import CryptContext
from typing import Union, Any
from datetime import timedelta, datetime
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.queries import q_users as database

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password, hashed_password) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(subject: Union[str, Any], expires_delta: Union[timedelta, None] = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/login')


def get_user_id_from_token(token: str, credentials_exception):
    """
    Извлекает ID пользователя из токена.

    :param token: Токен пользователя.
    :param credentials_exception: Ошибка токена!
    :return: user_id; credentials_exception or JWTError in case of exceptions!
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    return user_id


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Возвращает данные о пользователе, используя токен.

    :param token: Токен пользователя.
    :return: user; credentials_exception or JWTError in case of exceptions!
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить учетные данные!',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    user_id = get_user_id_from_token(token, credentials_exception)
    user = await database.user_get(user_id)
    if user is None:
        raise credentials_exception
    return user
