from fastapi import APIRouter, Response, Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from datetime import timedelta

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from api.database import SessionDep
from api.auth import authenticate_user, create_access_token, get_token_from_cookie

router = APIRouter(tags=["auth"])

# ログインしてアクセストークンを取得するリクエスト
@router.post("/token/")
def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expires = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    print(expires)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        expires=expires,
    )

    print(response.headers)
    return {"ok": True}

@router.post("/logout/")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"ok": True}

@router.get("/status/")
def read_auth_status(token: Annotated[str | None, Cookie()] = None) -> bool:
    if not token:
        return {"is_authenticated": False}
    return {"is_authenticated": True}