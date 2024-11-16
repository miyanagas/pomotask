from typing import Annotated
import uuid
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
import os
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, delete
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_session, create_db_and_tables, drop_db_and_tables
from app.todo_model import Todo, TodoCreate, TodoPublic, TodoUpdate
from app.user_model import User, UserCreate, UserPublic, UserUpdate, UserPasswordUpdate


app = FastAPI()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ph = PasswordHasher()

# CORSの設定
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

SessionDep = Annotated[Session, Depends(get_session)]

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/signup/", response_model=Token)
def signup(user: UserCreate, session: SessionDep):
    if session.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = hash_password(user.password)
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/token/", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

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
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    try:
        user_uuid = uuid.UUID(token_data.user_id)
    except ValueError:
        # uuid conversion failed
        raise HTTPException(status_code=401, detail="Invalid user ID in token")
    user = session.exec(select(User).where(User.id == user_uuid)).first()
    if not user:
        raise credentials_exception
    return user

UserDep = Annotated[User, Depends(get_current_user)]

@app.get("/users/me/", response_model=UserPublic)
def read_users_me(current_user: UserDep):
    return current_user

@app.put("/users/me/", response_model=UserPublic)
def update_user_me(user: UserUpdate, current_user: UserDep, session: SessionDep):
    user_data = user.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@app.put("/users/me/password/")
def update_user_password(user: UserPasswordUpdate, current_user: UserDep, session: SessionDep):
    if not verify_password(user.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    current_user.password = hash_password(user.new_password)
    session.add(current_user)
    session.commit()
    return {"ok": True}

@app.delete("/users/me/")
def delete_user_me(current_user: UserDep, session: SessionDep):
    session.delete(current_user)
    session.commit()
    return {"ok": True}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.on_event("shutdown")
def on_shutdown():
    drop_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# ToDoItemを新規作成するリクエスト
@app.post("/todo-list/", response_model=TodoPublic)
def create_todo(todo: TodoCreate, user: UserDep, session: SessionDep):
    todo_data = todo.model_dump()
    todo_data["user_id"] = user.id
    db_todo = Todo.model_validate(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


# ToDoItemを更新するリクエスト
@app.put("/todo-list/{id}", response_model=TodoPublic)
def update_todo(id: uuid.UUID, todo: TodoUpdate, user: UserDep, session: SessionDep):
    db_todo = session.exec(select(Todo).where(Todo.user_id == user.id).where(Todo.id == id)).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

# ToDoListを取得するリクエスト
@app.get("/todo-list/", response_model=list[TodoPublic])
def read_todo_list(user: UserDep, session: SessionDep, filter: bool = False):
    if filter:
        db_todo_list = session.exec(select(Todo).where(Todo.user_id == user.id).where(Todo.is_done == False)).all()
    else:
        db_todo_list = session.exec(select(Todo).where(Todo.user_id == user.id)).all()
    return db_todo_list

# ToDoItemを取得するリクエスト
@app.get("/todo-list/{id}", response_model=TodoPublic)
def read_todo(id: uuid.UUID, user: UserDep, session: SessionDep):
    db_todo = session.exec(select(Todo).where(Todo.user_id == user.id).where(Todo.id == id)).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# ToDoListを削除するリクエスト
@app.delete("/todo-list/")
def delete_todo_list(user: UserDep, session: SessionDep):
    session.exec(delete(Todo).where(Todo.user_id == user.id))
    session.commit()
    return {"ok": True}
