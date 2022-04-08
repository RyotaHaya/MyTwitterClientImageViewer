import os
import sys

from fastapi import HTTPException, status

sys.path.append(os.pardir)
from database.datastore import store_manager


def create_auth_token_str(token: str, token_secret: str) -> str:
    """認証用トークン登録
        トークン対してトークンシークレットを登録する
    Args:
        token:トークン
        token_secret:トークンシークレット
    Returns:
        str: 暗号化された値

    Raises:

    """
    
    client = store_manager.ClientManager()
    client.create_auth_token(token, token_secret)


def get_auth_token(auth_token: str):
    client = store_manager.ClientManager()
    ret = client.get_auth_token(auth_token)


def decode_auth_token_str(encryption_str) -> dict[str, str]:
    """認証用トークン復号
        一つ暗号化された値を復号する
    Args:
        encryption_str:暗号化された値
    Returns:
        dict: 復号したトークン情報

    Raises:
        復号に失敗した場合
    """
    try:
        result = encryption_str
        if not result:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "ツイッターのログイン情報が不正です。再ログインしてください。",
                headers = {"WWW-Authenticate": 'Bearer realm="auth_param invalid"'},
            )
        
        arr = result.split(":")
        
        return {"twitter_token": arr[0], "twitter_token_secret": arr[1]}
    
    except Exception as e:
        raise Exception(e)
