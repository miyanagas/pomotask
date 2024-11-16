from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.models.user import User, UserCreate, UserPublic, UserUpdate, UserPasswordUpdate
from app.auth import hash_password, verify_password, UserDep
from app.database import SessionDep

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup/", response_model=UserPublic)
def signup(user: UserCreate, session: SessionDep):
    if session.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user.password = hash_password(user.password)
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/me/", response_model=UserPublic)
def read_users_me(current_user: UserDep):
    return current_user

@router.put("/me/", response_model=UserPublic)
def update_user_me(user: UserUpdate, current_user: UserDep, session: SessionDep):
    user_data = user.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.put("/me/password/")
def update_user_password(user: UserPasswordUpdate, current_user: UserDep, session: SessionDep):
    if not verify_password(user.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect current password")
    current_user.password = hash_password(user.new_password)
    session.add(current_user)
    session.commit()
    return {"ok": True}

@router.delete("/me/")
def delete_user_me(current_user: UserDep, session: SessionDep):
    session.delete(current_user)
    session.commit()
    return {"ok": True}