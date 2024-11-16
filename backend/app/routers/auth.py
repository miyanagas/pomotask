from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from typing import Annotated
from datetime import timedelta

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User
from app.database import SessionDep
from app.auth import verify_password, create_access_token, Token

router = APIRouter(tags=["auth"])

@router.post("/token/", response_model=Token)
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