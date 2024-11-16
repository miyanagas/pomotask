import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password = os.environ["MYSQL_ROOT_PASSWORD"]
dbname = os.environ["MYSQL_DATABASE"]
SQL_DATABASE_URL = f"mysql+pymysql://root:{password}@db:3306/{dbname}"