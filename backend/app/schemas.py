from pydantic import BaseModel


# ToDoItem schema
class toDoItemCreate(BaseModel):
    title: str


class toDoItem(toDoItemCreate):
    is_done: bool
