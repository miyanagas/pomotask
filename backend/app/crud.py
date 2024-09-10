from sqlalchemy.orm import Session
from . import models, schemas


# toDoListを取得
def get_toDoList(db: Session, all: bool = False):
    if all:
        return db.query(models.ToDoItem).all()
    return db.query(models.ToDoItem).filter(models.ToDoItem.is_done == False).all()


# ToDoItemを新規作成
def create_toDoItem(db: Session, toDoItem: schemas.toDoItemCreate):
    db_toDoItem = models.ToDoItem(title=toDoItem.title, is_done=False)
    db.add(db_toDoItem)
    db.commit()
    db.refresh(db_toDoItem)
    return db_toDoItem


# 全てのstock、salesを削除
def delete_toDoItem(db: Session):
    db.query(models.ToDoItem).delete()
    db.commit()
