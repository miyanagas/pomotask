from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from pydantic import BaseModel

from typing import Annotated
from datetime import datetime, timedelta
import uuid
import jwt
from jwt.exceptions import InvalidTokenError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.config import ALGORITHM, SECRET_KEY
from app.models.user import User
from app.database import SessionDep

ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

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

# アクセストークンの生成
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ユーザーの取得
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> User:
    credentials_exception = HTTPException(
        status_code=401,
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