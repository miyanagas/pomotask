from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
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
    expires: datetime

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

# トークンの生成
def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc).replace(microsecond=0) + expires_delta
    else:
        expire = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire

# クッキーからアクセストークンを取得
def get_access_token_from_cookie(access_token: Annotated[str | None, Cookie()] = None) -> str:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_token

# クッキーからリフレッシュトークンを取得
def get_refresh_token_from_cookie(refresh_token: Annotated[str | None, Cookie()] = None) -> str:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is missing",
        )
    return refresh_token

# トークンの検証
def validate_credentials(credential: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    authorization_scheme, token = get_authorization_scheme_param(credential)
    if authorization_scheme.lower() != "bearer":
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        expires = payload.get("exp")
        if not user_id or not expires:
            raise credentials_exception

        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            # uuid conversion failed
            raise credentials_exception

        token_data = TokenData(user_id=user_uuid, expires=expires)
    except InvalidTokenError:
        raise credentials_exception

    return token_data

# ユーザーの取得
def get_current_user(access_token: Annotated[str, Depends(get_access_token_from_cookie)], session: SessionDep) -> User:
    token_data = validate_credentials(access_token)
    user = session.exec(select(User).where(User.id == token_data.user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

UserDep = Annotated[User, Depends(get_current_user)]