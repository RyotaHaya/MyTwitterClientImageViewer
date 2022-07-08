# -*- coding: utf-8 -*-
"""twitter API実行モジュール
    tweepyを利用してツイッターの情報を取得します
"""

from sqlalchemy import null
import tweepy

from core import config as settings
from util import timer


class TwitterAPI:
    """TwitterAPI呼び出しハンドラー

    twitterAPIを実行するモジュール呼び出しクラス

    Attributes:
        属性の名前 (属性の型): 属性の説明
        属性の名前 (:obj:`属性の型`): 属性の説明.
    """
    
    # コンストラクタ
    def __init__(self, token, token_secret):
        # twitter認証
        auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
        
        auth.set_access_token(token, token_secret)
        self.api = tweepy.API(auth)
    
    def home_timeline_tweets(
        self,
        req_filter,
        req_since_id,
        req_max_id,
        item_count,
        res_count,
    ):
        """タイムラインツイート取得メソッド
         ツイッターのホームタイムラインのツイート
         を取得します

        Args:
            req_filter:取得対象のツイートを指定します。未指定:全てのツイート images:画像付きツイート videos:動画付きツイート media:画像、動画付きツイート
            req_since_id:指定したツイートID以降に投稿されたツイートのみを取得します。
            req_max_id:指定したツイートID、指定したツイート以前のツイートのみを取得します。
            item_count:Cursorオブジェクト利用時のlimit数(max200)
            res_count:レスポンスするツイート数を指定します。
        Returns:
           list[]: 取得したツイートのJsonオブジェクト
        Raises:
            Exception: tweepy実行に失敗した場合

        Note:
            リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
        """
        
        ret_list = []
        
        try:
            # 検索条件の設定
            filter_args = {"include_entities": False, "exclude_replies": True}
            if req_since_id != "":
                filter_args["since_id"] = req_since_id
            
            if req_max_id != "":
                filter_args["max_id"] = req_max_id
            # リクエスト実行
            res = tweepy.Cursor(self.api.home_timeline, **filter_args).items(item_count)
            ret_list = []
            for time_line_tweet in res:
                # ツイート情報
                tweet = time_line_tweet
                
                # リツイート情報
                retweeted = False
                retweeted_id = ""
                if "retweeted_status" in dir(tweet):
                    retweet_status = tweet.retweeted_status
                    retweeted = True
                    # リツイートの場合、retweet_statuに元ツイートが格納されている
                    tweet = retweet_status
                    retweeted_id = tweet.id
                
                # メディア情報
                media_urls = []
                media_type = ""
                # textのみのツイートは処理されない
                if "extended_entities" in dir(time_line_tweet):
                    for media in tweet.extended_entities["media"]:
                        media_type = media["type"]
                        if media_type == "photo":
                            media_urls.append(media["media_url"])
                
                # filter指定時はテキストのみのツイートはレスポンスしない
                if req_filter != "" and len(media_urls) == 0:
                    continue
                
                tweet_status = {
                    "id": tweet.id,
                    "createdTime": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "text": tweet.text,
                    "retweetId": retweeted_id,
                    "retweeted": retweeted,
                    "media": {
                        "mediaType": media_type,
                        "url": media_urls
                    },
                    "user": {
                        "id": tweet.user.id,
                        "screenName": tweet.user.screen_name,
                        "name": tweet.user.name,
                        "profileImageUrl": tweet.user.profile_image_url,
                    },
                }
                ret_list.append(tweet_status)
                
                if len(ret_list) == res_count:
                    break
        except Exception as e:
            raise Exception(e)
        
        return ret_list
    
    def list_timeline_tweets(
        self,
        req_id,
        req_since_id,
        req_max_id,
        req_include_rts,
        req_filter,
        item_count,
        res_count,
    ):
        """リストタイムライン取得メソッド
         ツイッターのリストのツイートを取得します

        Args:
            req_id:取得対象のリストID
            req_since_id:指定したツイートID以降に投稿されたツイートのみを取得します。
            req_max_id:指定したツイートID、指定したツイート以前のツイートのみを取得します。
            req_include_rts:Trueの場合リツリートを含めて返却します。
            req_filter:取得対象のツイートを指定します。未指定:全てのツイート images:画像付きツイート videos:動画付きツイート media:画像、動画付きツイート
            item_count:Cursorオブジェクト利用時のlimit数(max200)
            res_count:レスポンスするツイート数を指定します。
        Returns:
           list[]: 取得したツイートのJsonオブジェクト
        Raises:
            Exception: twitterへのアクセスエラー時

        Note:
            リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
        """
        
        # 検索条件の設定
        filter_args = {
            "list_id": req_id,
            "include_rts": req_include_rts,
            "include_entities": False,
        }
        if req_since_id != "":
            filter_args["since_id"] = req_since_id
        
        if req_max_id != "":
            filter_args["max_id"] = req_max_id
        
        try:
            s = timer.timer_start()
            # リクエスト実行
            ret_list = []
            for time_line_tweet in tweepy.Cursor(self.api.list_timeline, **filter_args).items(item_count):
                # ツイート情報
                tweet: dict = time_line_tweet
                origin_tweet: dict = null
                origin_user: dict = null
                # リツイート情報
                retweeted: bool = False
                if "retweeted_status" in dir(tweet):
                    retweet_status = tweet.retweeted_status
                    retweeted = True
                    # リツイートの場合、retweet_statuに元ツイート情報が格納されている
                    origin_tweet = retweet_status
                    origin_user = origin_tweet.user
                
                # メディア情報
                media_urls = []
                media_type = ""
                # textのみのツイートは処理されない
                if "extended_entities" in dir(time_line_tweet):
                    for media in tweet.extended_entities["media"]:
                        media_type = str(media["type"])
                        if media_type == "photo":
                            media_urls.append(media["media_url"])
                
                # filter指定時はテキストのみのツイートはレスポンスしない
                if req_filter != "" and len(media_urls) == 0:
                    continue
                
                tweet_status = {
                    "id": str(origin_tweet.id) if retweeted else str(tweet.id),
                    "createdTime": origin_tweet.created_at.strftime("%Y-%m-%d %H:%M:%S") if retweeted else tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "text": str(origin_tweet.text) if retweeted else str(tweet.text),
                    "retweetId": str(tweet.id) if retweeted else '',
                    "retweeted": retweeted,
                    "retweetedUser": str(tweet.user.screen_name) if retweeted else '',
                    "favorited": tweet.favorited,
                    "media": {
                        "mediaType": media_type,
                        "url": media_urls
                    },
                    "user": {
                        "id": str(origin_user.id) if retweeted else str(tweet.user.id),
                        "screenName": str(origin_user.screen_name) if retweeted else tweet.user.screen_name,
                        "name": str(origin_user.name) if retweeted else tweet.user.name,
                        "profileImageUrl": str(origin_user.profile_image_url) if retweeted else tweet.user.profile_image_url,
                    },
                }
                ret_list.append(tweet_status)
                
                if len(ret_list) == res_count:
                    break
        except Exception as e:
            raise Exception(e)
        
        return ret_list
    
    def get_lists(self, screen_name):
        """リストオブジェクト取得メソッド
            引数に指定したユーザがアクセス可能なリストを取得します

        Args:

        Returns:
           list[]: 取得したツイートのJsonオブジェクト
        Raises:
            Exception: twitterへのアクセスエラー時

        Note:
            リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
        """
        
        ret_list = []
        try:
            res = self.api.get_lists(screen_name = screen_name)
            
            ret_list = []
            for res_list in res:
                list_data = {
                    "ID": str(res_list.id),
                    "Name": res_list.name,
                    "Member_count": res_list.member_count,
                }
                
                ret_list.append(list_data)
            
            return ret_list
        except Exception as e:
            raise Exception(e)
