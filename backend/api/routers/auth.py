from fastapi import APIRouter, Response, Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from sqlmodel import select

from typing import Annotated
from datetime import datetime, timedelta, timezone

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from api.database import SessionDep
from api.auth import authenticate_user, create_token, get_refresh_token_from_cookie, validate_credentials
from api.models.token import Token, TokenCreate

router = APIRouter(tags=["auth"])

# Set-Cookie attribute
cookie_config = {"httponly": True, "secure": True, "samesite": "None"}
# cookie_config = {"httponly": True, "secure": False, "samesite": "Strict"}

# ログインしてアクセストークンを取得するリクエスト
@router.post("/token/")
def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):

    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expires = create_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        expires=expires,
        **cookie_config
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token, expires = create_token(
        data={"sub": str(user.id)}, expires_delta=refresh_token_expires
    )

    refresh_token_data = TokenCreate(token=refresh_token, expires=expires, user_id=user.id)
    db_refresh_token = Token.model_validate(refresh_token_data)
    session.add(db_refresh_token)
    session.commit()

    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        expires=expires,
        **cookie_config
    )

    return {"ok": True}

# リフレッシュトークンを使ってアクセストークンを更新するリクエスト
@router.get("/refresh/")
def refresh_tokens(response: Response, refresh_token: Annotated[str, Depends(get_refresh_token_from_cookie)], session: SessionDep):
    refresh_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
    )

    refresh_token_data = validate_credentials(refresh_token)
    db_refresh_token = session.exec(select(Token).where(Token.user_id == refresh_token_data.user_id, Token.expires == refresh_token_data.expires)).first()
    if not db_refresh_token:
        raise refresh_exception
    if db_refresh_token.expires < datetime.now(timezone.utc):
        session.delete(db_refresh_token)
        raise refresh_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expires = create_token(
        data={"sub": str(db_refresh_token.user_id)}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        expires=expires,
        **cookie_config
    )

    return {"ok": True}

@router.delete("/logout/")
def logout(response: Response, refresh_token: Annotated[str, Depends(get_refresh_token_from_cookie)], session: SessionDep):
    scheme, token = get_authorization_scheme_param(refresh_token)
    db_refresh_token = session.exec(select(Token).where(Token.token == token)).first()

    if db_refresh_token:
        session.delete(db_refresh_token)
        session.commit()

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"ok": True}

@router.get("/status/")
def read_auth_status(access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return {"is_authenticated": False}
    return {"is_authenticated": True}