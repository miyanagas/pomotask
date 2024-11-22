from sqlmodel import SQLModel, Field, Relationship
from pydantic import validator, EmailStr, BaseModel

from typing import TYPE_CHECKING, Optional
from datetime import datetime
import uuid
import re

if TYPE_CHECKING:
    from api.models.todo import Todo
    from api.models.token import Token

# Userテーブルの定義
class UserBase(SQLModel):
    username: str = Field(max_length=20, index=True) # ユーザ名
    email: EmailStr # メールアドレス

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True) # ID
    password: str # パスワード
    created_at: datetime = Field(default_factory=datetime.now) # 作成日時
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now}
    ) # 更新日時

    todo_list: list["Todo"] = Relationship(back_populates="user", cascade_delete=True) # User削除時にTodoも削除
    token: Token | None = Relationship(back_populates="user", cascade_delete=True) # User削除時にTokenも削除

# パスワードのパターンを検証する関数
def check_password_pattern(password: str):
    # パスワードの長さを検証（8文字以上）
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    # パスワードの長さを検証（20文字以下）
    if len(password) > 20:
        raise ValueError("Password must be at most 20 characters long")

    # 英字が含まれているか
    if not re.search(r'[a-zA-Z]', password):
        raise ValueError("Password must contain at least one letter")

    # 数字が含まれているか
    if not re.search(r'[\d]', password):
        raise ValueError("Password must contain at least one digit")

    # 記号が含まれているか
    if not re.search(r'[!-\/:-@[-`{-~]', password):
        raise ValueError("Password must contain at least one special character")

    return password

class UserCreate(UserBase):
    password: str

    _check_password_pattern = validator("password", allow_reuse=True)(check_password_pattern)

class UserPublic(UserBase):
    id: uuid.UUID

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str

    _check_password_pattern = validator("new_password", allow_reuse=True)(check_password_pattern)
