from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

# データベースのテーブルの一括作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


# Dependency
# リクエストごとに独立してセッションを作成し、使用する
# リクエストが終了するとセッションを閉じる
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# ToDoItemを新規作成するリクエスト
@app.post("/todolist", response_model=schemas.toDoItem)
def add_toDo(toDoItem: schemas.toDoItemCreate, db: Session = Depends(get_db)):

    toDoItem = crud.create_toDoItem(db=db, toDoItem=toDoItem)
    return toDoItem


# ToDoListを取得するリクエスト
@app.get("/todolist", response_model=list[schemas.toDoItem])
def get_toDoList(db: Session = Depends(get_db)):
    toDoList = crud.get_toDoList(db, all=True)
    return toDoList


# ToDoListを削除するリクエスト
@app.delete("/todolist")
def delete_toDoList(db: Session = Depends(get_db)):
    crud.delete_toDoItem(db)
    return JSONResponse(content={"message": "Deleted all toDoList"})
