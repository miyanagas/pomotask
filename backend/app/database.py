from sqlmodel import SQLModel, Session, create_engine

import os
from dotenv import load_dotenv

load_dotenv()

password = os.environ["MYSQL_ROOT_PASSWORD"]
dbname = os.environ["MYSQL_DATABASE"]

SQL_DATABASE_URL = f"mysql+pymysql://root:{password}@db:3306/{dbname}"

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