from typing import Optional
import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

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