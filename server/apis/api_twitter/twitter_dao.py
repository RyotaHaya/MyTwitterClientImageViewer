# -*- coding: utf-8 -*-
"""twitter データアクセスモジュール
    twitterへアクセスするためのインタフェースモジュール
"""

from __future__ import annotations

import os
import sys

from core import config as settings
from util import timer

from .twitter_api import TwitterAPI

sys.path.append(os.pardir)

from util import encryption


class TwiterDAO:
    """TwitterData Access Object（DAO）クラス
        Twitterの情報操作インターフェース

    Attributes:
        属性の名前 (属性の型): 属性の説明
        属性の名前 (:obj:`属性の型`): 属性の説明.
    """
    
    # コンストラクタ
    def __init__(self, auth, auth_token):
        
        token_secret = encryption.get_auth_token(auth_token)
        
        self.gate = TwitterAPI(
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET,
        )
    
    def get_home_timeline(self, query: dict[str, object]) -> dict[str, object]:
        """ホームタイムラインメソッド
            ログインユーザのホームタイムラインツイートを取得します
            を取得します
        Args:
            query:クエリパラメータ
        Returns:
            dict[str, object]: 取得したツイートのJsonオブジェクト
        Raises:
            Exception:

        Note:

        """
        try:
            tweets = self.gate.home_timeline_tweets(
                query["include_rtweets"],
                query["filter"],
                query["since_tweet_id"],
                query["max_tweet_id"],
                query["item_count"],
                query["max_count"],
            )
            
            return {"totalCount": len(tweets), "timeLineTweets": tweets}
        
        except Exception as e:
            raise Exception(e)
    
    def get_list_timeline(self, query: dict[str, object]) -> dict[str, object]:
        """リストタイムラインメソッド
            指定したリストのタイムラインツイートを取得します
            を取得します
        Args:
            query:クエリパラメータ
        Returns:
            dict[str, object]: 取得したツイートのJsonオブジェクト
        Raises:
            Exception:

        Note:

        """
        try:
            s = timer.timer_start()
            tweets = self.gate.list_timeline_tweets(
                query["id"],
                query["max_tweet_id"],
                query["since_tweet_id"],
                query["include_rtweets"],
                query["filter"],
                query["item_count"],
                query["max_count"],
            )
            timer.timer_end(s)
            
            return {"totalCount": len(tweets), "timeLineTweets": tweets}
        
        except Exception as e:
            raise Exception(e)
    
    def get_user_list(self, query: dict[str, object]) -> dict[str, object]:
        """ユーザリストメソッド
            指定したユーザのリストを取得します
        Args:
            query:クエリパラメータ
        Returns:
            dict[str, object]: 取得したリストのJsonオブジェクト
        Raises:
            Exception:

        Note:

        """
        try:
            lists = self.gate.get_lists(query["user_name"])
            
            return {"totalCount": len(lists), "list": lists}
        
        except Exception as e:
            raise Exception(e)
