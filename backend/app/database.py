from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

from typing import Annotated

from app.config import SQL_DATABASE_URL

# DBと接続するエンジンの作成
engine = create_engine(SQL_DATABASE_URL)

# データベースのテーブルの一括作成
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)

# DBとの論理的な接続であるセッションを作成
# リクエストごとに独立してセッションを提供
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]