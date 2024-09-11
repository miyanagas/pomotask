from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

password = os.environ["MYSQL_ROOT_PASSWORD"]
dbname = os.environ["MYSQL_DATABASE"]

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{password}@db:3306/{dbname}"

# DBと接続するエンジンの作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# DBとの論理的な接続であるセッションを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # DBのテーブルに対応するクラスのベース
