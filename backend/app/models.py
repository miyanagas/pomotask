from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


# ToDoItemテーブルの定義
class ToDoItem(Base):
    __tablename__ = "todo_list"

    id = Column(Integer, primary_key=True, index=True)  # ID
    title = Column(String(50), index=True)  # タイトル
    is_done = Column(Boolean, default=False)  # 完了フラグ
    time_to_complete = Column(Integer, default=0)  # 完了予定時間（秒）
