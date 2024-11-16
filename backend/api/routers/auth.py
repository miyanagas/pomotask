from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from typing import Annotated
from datetime import timedelta

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from api.models.user import User
from api.database import SessionDep
from api.auth import verify_password, create_access_token, Token

router = APIRouter(tags=["auth"])

# ログインしてアクセストークンを取得するリクエスト
@router.post("/token/", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")