from __future__ import annotations

import datetime
import os
import sys
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from apis.api_core.auth import api_core_auth
from apis.api_twitter.twitter_dao import TwiterDAO
from core.auth import (create_session_cookie, get_current_user, set_session_cookie)

from .model import SessionParam

sys.path.append(os.pardir)

from util import encryption

router = APIRouter()


@router.post("/api/sessionLogin", tags = ["firebase"])
async def session_login(session_param: SessionParam, response: Response) -> dict[str, object]:
    """ログイン情報設定
        API実行時に必要なログイン情報をクライアント端末に設定する
    Args:
        session_param:
        response:
    Returns:
        dict: result

    Raises:

    """
    
    expires_in = datetime.timedelta(days = 14)
    session_cookie = create_session_cookie(session_param.firebase_id_token, expires_in)
    encryption.create_auth_token_str(session_param.token, session_param.secret)
    set_session_cookie(response, "session", session_cookie, expires_in)
    set_session_cookie(response, "tw_auth_token", session_param.token, expires_in)
    
    return {}


@router.get("/api/login", tags = ["firebase"])
async def view_firebaselogin(
        auth_token: Optional[str] = Cookie(None),
        auth: Depends = Depends(get_current_user),
) -> dict[str, object]:
    """FireBaseログイン
        FireBaseのログイン状態を確認する
    Args:
        session_param:
        response:
    Returns:
        dict: result

    Raises:

    """
    auth = Depends(get_current_user)
    return {"loginResult": "success"}


@router.get("/api/twitter/timeline/home", tags = ["api_twitter"])
async def view_timeline_home(
        includeRTweets: Optional[bool] = True,
        filter: Optional[str] = "",
        maxCount: Optional[int] = 50,
        maxTweetId: Optional[str] = "",
        sinceTweetId: Optional[str] = "",
        itemCount: Optional[int] = 100,
        auth: Depends = Depends(get_current_user),
) -> dict[str, object]:
    """Twitterホームタイムライン取得
        認証済みユーザのホームタイムラインを取得する
    Args:

    Returns:
        dict: result

    Raises:

    """
    
    q = {
        "include_rtweets": includeRTweets,
        "filter": filter,
        "max_count": maxCount,
        "max_tweet_id": maxTweetId,
        "since_tweet_id": sinceTweetId,
        "item_count": itemCount,
    }
    
    try:
        api = TwiterDAO()
        return api.get_home_timeline(q)
    
    except Exception as e:
        # Twitterアクセスエラーの場合
        if hasattr(e, "args"):
            e_args = e.args[0].args[0]
            
            # Twitterアクセスエラーの場合
            if hasattr(e_args, "args"):
                error_res = e.args.args[0]
                raise HTTPException(
                    status_code = error_res.response.status_code,
                    detail = error_res.api_errors[0],
                )
        else:
            raise HTTPException(status_code = 500, detail = str(e))


@router.get("/api/twitter/timeline/lists/{id}", tags = ["api_twitter"])
async def view_timeline_list(id: Optional[str] = "",
                                includeRTweets: Optional[bool] = True,
                                filter: Optional[str] = "",
                                maxCount: Optional[int] = 50,
                                maxTweetId: Optional[str] = "",
                                sinceTweetId: Optional[str] = "",
                                itemCount: Optional[int] = 100,
                                auth: Depends = Depends(get_current_user),
                                tw_auth_token: Optional[str] = Cookie(None)) -> dict[str, object]:
    """Twitterリストタイムライン取得
        認証済みユーザのリストタイムラインを取得する
    Args:

    Returns:
        dict: result

    Raises:

    """
    
    q = {
        "id": id,
        "include_rtweets": includeRTweets,
        "filter": filter,
        "max_count": maxCount,
        "max_tweet_id": maxTweetId,
        "since_tweet_id": sinceTweetId,
        "item_count": itemCount,
    }
    
    try:
        api = TwiterDAO(auth, tw_auth_token)
        return api.get_list_timeline(q)
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


@router.get("/api/twitter/lists", tags = ["api_twitter"])
async def view_user_list(user_name: Optional[str] = "", auth: Depends = Depends(get_current_user), tw_auth_token: Optional[str] = Cookie(None)) -> dict[str, object]:
    """Twitterリスト取得
        ユーザのリストを取得する
    Args:

    Returns:
        dict: result

    Raises:

    """
    
    q = {"user_name": user_name}
    
    try:
        api = TwiterDAO(auth, tw_auth_token)
        return api.get_user_list(q)
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
