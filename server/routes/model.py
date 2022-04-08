from typing import Optional

from pydantic import BaseModel


class ListParam(BaseModel):
    id: Optional[str] = ("", )
    includeRTweets: Optional[bool] = (False, )
    filter: Optional[str] = ("", )
    maxCount: Optional[int] = (50, )
    maxTweetId: Optional[str] = ("", )
    sinceTweetId: Optional[str] = ("", )
    itemCount: Optional[int] = (100, )


class SessionParam(BaseModel):
    firebase_id_token: str
    token: str
    secret: str


class AuthParam(BaseModel):
    twitter_token: str
    twitter_token_secret: str
    user_id: str
