from fastapi import Cookie, Depends, HTTPException, status
from sqlmodel import select
from pydantic import BaseModel

from typing import Annotated
from datetime import datetime, timedelta, timezone
import uuid
import jwt
from jwt.exceptions import InvalidTokenError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from api.config import ALGORITHM, SECRET_KEY
from api.models.user import User
from api.database import SessionDep

ph = PasswordHasher()

class TokenData(BaseModel):
    user_id: uuid.UUID

# パスワードのハッシュ化
def hash_password(password: str) -> str:
    return ph.hash(password)

# パスワードの検証
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

# ユーザーの認証
def authenticate_user(username: str, password: str, session: SessionDep) -> User | bool:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user

# アクセストークンの生成
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire

# クッキーからトークンを取得
def get_token_from_cookie(token: Annotated[str | None, Cookie()] = None) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

# ユーザーの取得
def get_current_user(token: Annotated[str, Depends(get_token_from_cookie)], session: SessionDep) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            # uuid conversion failed
            raise credentials_exception
        token_data = TokenData(user_id=user_uuid)
    except InvalidTokenError:
        raise credentials_exception
    user = session.exec(select(User).where(User.id == token_data.user_id)).first()
    if not user:
        raise credentials_exception
    return user

UserDep = Annotated[User, Depends(get_current_user)]