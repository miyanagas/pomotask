from typing import Optional, Any
import uuid
from datetime import datetime
import re
from sqlmodel import SQLModel, Field
from pydantic import validator, EmailStr

# ToDoItemテーブルの定義
class TodoBase(SQLModel):
    title: str = Field(max_length=50, index=True) # タイトル

class Todo(TodoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True) # ID
    is_done: bool = False # 完了フラグ
    time_to_complete: int = 0 # 完了予定時間（秒）
    created_at: datetime = Field(default_factory=datetime.now, index=True) # 作成日時
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}, index=True) # 更新日時

class TodoCreate(TodoBase):
    pass

class TodoPublic(TodoBase):
    id: uuid.UUID
    is_done: bool
    time_to_complete: int
    created_at: datetime
    updated_at: datetime

class TodoUpdate(TodoBase):
    title: Optional[str] = None
    is_done: Optional[bool] = None
    time_to_complete: Optional[int] = None

# Userテーブルの定義
class UserBase(SQLModel):
    username: str = Field(max_length=20, index=True) # ユーザ名
    email: EmailStr # メールアドレス

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True) # ID
    password: str # パスワード

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
    password: Optional[str] = None

    _check_password_pattern = validator("password", allow_reuse=True)(check_password_pattern)