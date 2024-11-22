from sqlmodel import SQLModel, Field, Relationship

from typing import Optional
import uuid
from datetime import datetime

from api.models.user import User

# Tokenテーブルの定義
class TokenBase(SQLModel):
    token: str = Field(primary_key=True) # トークン
    expires: datetime # 有効期限

class Token(TokenBase, table=True):
    created_at: datetime = Field(default_factory=datetime.now, index=True) # 作成日時
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
        index=True
    ) # 更新日時

    user_id: uuid.UUID = Field(index=True, foreign_key="user.id", ondelete="CASCADE") # User削除時に削除
    user: User = Relationship(back_populates="token")

class TokenCreate(TokenBase):
    user_id: uuid.UUID