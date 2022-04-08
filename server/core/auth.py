"""firebase認証
    CookieによるFirebaseの認証関連処理を実行する

Todo:
    特になし

"""

import datetime
import os
from typing import Optional

import firebase_admin
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials, exceptions
from pydantic import BaseModel

# firebaseの設定ファイル読み込み
path = os.getcwd()
cred = credentials.Certificate("./config/account_key.json")
firebase_admin.initialize_app(cred)


def get_current_user(
        res: Response,
        # cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        session: Optional[str] = Cookie(None),
):
    """FireBase認証
        引数に渡されたトークン情報からログイン中のユーザに対応するトークン情報を取得する
    Args:
        res:Response
        cred:
        session:
    Returns:
        str: decoded_token

    Raises:

    """
    
    if cred is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Bearer authentication required",
            headers = {"WWW-Authenticate": 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_session_cookie(session)
    except Exception as err:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f"Invalid authentication credentials. {err}",
            headers = {"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )
    res.headers["WWW-Authenticate"] = 'Bearer realm="auth_required"'
    return decoded_token


def create_session_cookie(id_token: str, expires_in: datetime) -> object:
    """FireBaseセッション作成
        トークン情報からFireBaseのトークンセッションを作成
    Args:
        id_token:トークン
        expires_in:有効期限 Firebaseの仕様上、Cookieの保存期間は最長2週間
                    https://firebase.google.com/docs/auth/admin/manage-cookies?hl=ja
    Returns:
        str: decoded_token

    Raises:

    """
    
    try:
        session_cookie = auth.create_session_cookie(id_token, expires_in = expires_in)
        return session_cookie
    except exceptions.FirebaseError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Failed to create a session cookie'",
        )


def set_session_cookie(response: Response, key: str, value: str, expires_in: datetime):
    response.set_cookie(
        key = key,
        value = value,
        httponly = True,
        secure = True,
        expires = datetime.datetime.now() + expires_in,
    )


class Token(BaseModel):
    access_token: str
    token_type: str


router = APIRouter()
