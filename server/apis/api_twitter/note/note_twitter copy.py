# # -*- coding: utf-8 -*-
# """twitter API実行モジュール

# * tweepyを利用してツイッターの情報を取得します
# * importより前に記載する

# Todo:
#     TODOリストを記載
#     コーディんぐスタイルの変更(googleStyle) https://qiita.com/11ohina017/items/118b3b42b612e527dc1d
#     * conf.pyの``sphinx.ext.todo`` を有効にしないと使用できない
#     * conf.pyの``todo_include_todos = True``にしないと表示されない

# """
# import json
# import time
# import datetime
# import tweepy
# from .sncrape import custom_scncraper as sntwitter

# import pandas as pd
# from core import config as settings
# from requests_oauthlib import OAuth1Session

# # import identifies_image as idf
# from urllib.parse import parse_qsl

# # 定数
# filter_options = ("", "images", "videos", "media")

# class TwiterGateway:
#     """クラスの説明タイトル

#     クラスについての説明文

#     Attributes:
#         属性の名前 (属性の型): 属性の説明
#         属性の名前 (:obj:`属性の型`): 属性の説明.
#         base_url:
#         request_token_url:
#         authenticate_url:
#         access_token_url:
#         base_json_url:
#         oauth_callback:認証成功時にcallbackするURL
#         authenticate_url:
#     """

#     # twitterの接続情報
#     base_url = "https://api.twitter.com/"
#     request_token_url = base_url + "oauth/request_token"
#     authenticate_url = base_url + "oauth/authenticate"
#     access_token_url = base_url + "oauth/access_token"
#     base_json_url = "https://api.twitter.com/1.1/%s.json"
#     oauth_callback = "http://localhost:3000/"
#     authenticate_url = "https://api.twitter.com/oauth/authenticate"

#     # コンストラクタ
#     def __init__(self, token, token_secret):
#         # twitter認証
#         auth = tweepy.OAuthHandler(
#             settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY
#         )

#         auth.set_access_token(token, token_secret)
#         # self.api = tweepy.API(auth)

#         # TODO 認証方式確立するまでは仮でaccesstokenを設定
#         self.twitter = OAuth1Session(
#             settings.TWITTER_API_KEY,
#             settings.TWITTER_API_SECRET_KEY,
#             settings.TWITTER_ACCESS_TOKEN,
#             settings.TWITTER_ACCESS_TOKEN_SECRET,
#         )

#     def get_twitter_request_token(self):
#         """リクエストトークン発行
#         twitterへのリクエストトークンを発行する

#         Returns:
#             authenticate_endpoint:アクセス許可のURL
#         """

#         try:
#             twitter = OAuth1Session(
#                 settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY
#             )

#             response = twitter.post(
#                 self.request_token_url, params={"oauth_callback": self.oauth_callback}
#             )

#             if response.status_code > 400:
#                 raise Exception("Twitterのリクエストトークンの発行に失敗しました。")

#             # responseからリクエストトークンを取り出す
#             request_token = dict(parse_qsl(response.content.decode("utf-8")))

#             # リクエストトークンから連携画面のURLを生成
#             authenticate_endpoint = "%s?oauth_token=%s" % (
#                 self.authenticate_url,
#                 request_token["oauth_token"],
#             )

#         except Exception as e:
#             raise Exception(e)

#         return authenticate_endpoint

#     def get_twitter_access_token(self, request):
#         """アクセストークン発行
#         twitterへのアクセストークンを発行する
#         Args:
#         Returns:
#             access_token:ユーザアクセストークン
#         Raises:
#         Yields:
#         Examples:
#         Note:
#             TODO: 仮実装のため呼び出しはまだ。アクセス管理の仕様が決まったら使う。
#         """
#         try:
#             oauth_token = request.params.get("oauth_token", "")
#             oauth_verifier = request.params.get("oauth_verifier", "")

#             twitter = OAuth1Session(
#                 settings.API_KEY,
#                 settings.API_SECRET_KEY,
#                 oauth_token,
#                 oauth_verifier,
#             )

#             response = twitter.post(
#                 self.access_token_url, params={"oauth_verifier": oauth_verifier}
#             )

#             access_token = dict(parse_qsl(response.content.decode("utf-8")))

#             return access_token
#         except Exception as e:
#             raise Exception(e)

#     def home_timeline_tweets(
#         self,
#         req_include_rts,
#         req_filter,
#         req_since_id,
#         req_max_id,
#         item_count,
#         res_count,
#     ):
#         """タイムラインツイート取得メソッド
#          ツイッターのホームタイムラインのツイート
#          を取得します

#         Args:
#             req_include_rts:Trueの場合リツリートを含めて返却します。
#             req_filter:取得対象のツイートを指定します。未指定:全てのツイート images:画像付きツイート videos:動画付きツイート media:画像、動画付きツイート
#             req_since_id:指定したツイートID以降に投稿されたツイートのみを取得します。
#             req_max_id:指定したツイートID、指定したツイート以前のツイートのみを取得します。
#             item_count:Cursorオブジェクト利用時のlimit数(max200)
#             res_count:レスポンスするツイート数を指定します。
#         Returns:
#            list[]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception: tweepy実行に失敗した場合

#         Note:
#             リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
#         """

#         ret_list = []

#         try:
#             rate = self.api.rate_limit_status()
#             resources = rate["resources"]
#             statuses = resources["statuses"]

#             # 検索条件の設定
#             filter_args = {"include_entities": False, "exclude_replies": True}
#             if req_since_id != "":
#                 filter_args["since_id"] = req_since_id

#             if req_max_id != "":
#                 filter_args["max_id"] = req_max_id
#             # リクエスト実行
#             res = tweepy.Cursor(self.api.home_timeline, **filter_args).items(item_count)
#             ret_list = []
#             for time_line_tweet in res:
#                 # ツイート情報
#                 tweet = time_line_tweet

#                 # リツイート情報
#                 retweeted = False
#                 retweeted_id = ""
#                 if "retweeted_status" in dir(tweet):
#                     retweet_status = tweet.retweeted_status
#                     retweeted = True
#                     # リツイートの場合、retweet_statuに元ツイートが格納されている
#                     tweet = retweet_status
#                     retweeted_id = tweet.id

#                 # メディア情報
#                 media_urls = []
#                 media_type = ""
#                 # textのみのツイートは処理されない
#                 if "extended_entities" in dir(time_line_tweet):
#                     for media in tweet.extended_entities["media"]:
#                         media_type = media["type"]
#                         if media_type == "photo":
#                             media_urls.append(media["media_url"])

#                 # filter指定時はテキストのみのツイートはレスポンスしない
#                 if req_filter != "" and len(media_urls) == 0:
#                     continue

#                 tweet_status = {
#                     "id": tweet.id,
#                     "createdTime": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#                     "text": tweet.text,
#                     "retweetId": retweeted_id,
#                     "retweeted": retweeted,
#                     "media": {"mediaType": media_type, "url": media_urls},
#                     "user": {
#                         "id": tweet.user.id,
#                         "screenName": tweet.user.screen_name,
#                         "name": tweet.user.name,
#                         "profileImageUrl": tweet.user.profile_image_url,
#                     },
#                 }
#                 ret_list.append(tweet_status)

#                 if len(ret_list) == res_count:
#                     break
#         except Exception as e:
#             raise Exception(e)

#         return ret_list

#     def list_timeline_tweets(
#         self,
#         req_id,
#         req_since_id,
#         req_max_id,
#         req_include_rts,
#         req_filter,
#         item_count,
#         res_count,
#     ):
#         """リストタイムライン取得メソッド
#          ツイッターのリストのツイートを取得します

#         Args:
#             req_id:取得対象のリストID
#             req_since_id:指定したツイートID以降に投稿されたツイートのみを取得します。
#             req_max_id:指定したツイートID、指定したツイート以前のツイートのみを取得します。
#             req_include_rts:Trueの場合リツリートを含めて返却します。
#             req_filter:取得対象のツイートを指定します。未指定:全てのツイート images:画像付きツイート videos:動画付きツイート media:画像、動画付きツイート
#             item_count:Cursorオブジェクト利用時のlimit数(max200)
#             res_count:レスポンスするツイート数を指定します。
#         Returns:
#            list[]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception: twitterへのアクセスエラー時

#         Note:
#             リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
#         """

#         # 検索条件の設定
#         filter_args = {
#             "list_id": req_id,
#             "include_rts": req_include_rts,
#             "include_entities": False,
#         }
#         if req_since_id != "":
#             filter_args["since_id"] = req_since_id

#         if req_max_id != "":
#             filter_args["max_id"] = req_max_id

#         start = time.time()
#         try:
#             # リクエスト実行
#             res = tweepy.Cursor(self.api.list_timeline, **filter_args).items(item_count)

#             ret_list = []
#             for time_line_tweet in res:
#                 # ツイート情報
#                 tweet = time_line_tweet

#                 # リツイート情報
#                 retweeted = False
#                 retweeted_id = ""
#                 if "retweeted_status" in dir(tweet):
#                     retweet_status = tweet.retweeted_status
#                     retweeted = True
#                     # リツイートの場合、retweet_statuに元ツイートが格納されている
#                     tweet = retweet_status
#                     retweeted_id = tweet.id

#                 # メディア情報
#                 media_urls = []
#                 media_type = ""
#                 # textのみのツイートは処理されない
#                 if "extended_entities" in dir(time_line_tweet):
#                     for media in tweet.extended_entities["media"]:
#                         media_type = media["type"]
#                         if media_type == "photo":
#                             media_urls.append(media["media_url"])

#                 # filter指定時はテキストのみのツイートはレスポンスしない
#                 if req_filter != "" and len(media_urls) == 0:
#                     continue

#                 tweet_status = {
#                     "id": tweet.id,
#                     "createdTime": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#                     "text": tweet.text,
#                     "retweetId": retweeted_id,
#                     "retweeted": retweeted,
#                     "media": {"mediaType": media_type, "url": media_urls},
#                     "user": {
#                         "id": tweet.user.id,
#                         "screenName": tweet.user.screen_name,
#                         "name": tweet.user.name,
#                         "profileImageUrl": tweet.user.profile_image_url,
#                     },
#                 }
#                 ret_list.append(tweet_status)

#                 if len(ret_list) == res_count:
#                     break
#         except Exception as e:
#             raise Exception(e)

#         elapsed_time = time.time() - start
#         print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

#         return ret_list

#     def get_user_timeline_media_tweets(
#         self, req_user_id, req_since_id, req_max_id, range_count
#     ):
#         """ユーザタイムライン画像取得メソッド
#         指定したユーザーのタイムラインのメディアのみツイート
#          を取得します

#         Args:
#             user_id:取得対象のユーザID
#             since_id:
#             max_id:
#         Returns:
#            list[]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception: tweepy実行に失敗した場合

#         Note:
#             リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
#         """

#         ret_list = []

#         try:
#             if req_since_id != "" and req_max_id != "":
#                 res = tweepy.Cursor(
#                     self.api.user_timeline,
#                     id=req_user_id,
#                     since_id=req_since_id,
#                     max_id=req_max_id,
#                     include_rts=False,
#                 ).items(range_count)
#             elif req_since_id != "":
#                 res = tweepy.Cursor(
#                     self.api.user_timeline,
#                     id=req_user_id,
#                     since_id=req_since_id,
#                     include_rts=False,
#                 ).items(range_count)
#             elif req_max_id != "":
#                 res = tweepy.Cursor(
#                     self.api.user_timeline,
#                     id=req_user_id,
#                     max_id=req_max_id,
#                     include_rts=False,
#                 ).items(range_count)
#             else:
#                 res = self.api.user_timeline(include_rts=False).items(range_count)

#             for tweet in res:
#                 if "media" in tweet.entities:
#                     for media in tweet.extended_entities["media"]:
#                         if media["type"] == "photo":
#                             media_url = media["media_url"]

#                             tweetData = {
#                                 "ID": tweet.id,
#                                 "UseID": tweet.user.screen_name,
#                                 "DateTime": tweet.created_at.strftime(
#                                     "%Y-%m-%d %H:%M:%S"
#                                 ),
#                                 "Url": media_url,
#                             }
#                             ret_list.append(tweetData)
#         except Exception as e:
#             raise Exception(e)

#         return ret_list

#     def get_user_favlist(self, user_id, max_count):
#         ret_list = []
#         try:
#             url = "https://api.twitter.com/1.1/favorites/list.json?"
#             params = {"screen_name": user_id, "count": 5000}

#             res = self.twitter.get(url, params=params)

#             break_roop = False
#             if res.status_code == 200:
#                 tweets = json.loads(res.text)
#                 for tweet in tweets:
#                     # メディアなしツイートの場合
#                     if "extended_entities" not in tweet:
#                         continue

#                     # ファボ数フィルタ
#                     if tweet["favorite_count"] < 5:
#                         continue

#                     entities = tweet["extended_entities"]
#                     if "media" in entities:
#                         url_list = []

#                         user_info = tweet["user"]
#                         datetime_obj_utc = datetime.datetime.strptime(
#                             tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"
#                         )

#                         for media in entities["media"]:
#                             if media["type"] == "photo":
#                                 media_url = media["media_url"]
#                                 url_list.append(media_url)

#                         ret_data = {
#                             "ID": tweet["id"],
#                             "UseID": user_info["screen_name"],
#                             "DateTime": datetime_obj_utc.strftime("%Y-%m-%d %H:%M:%S"),
#                             "Url": url_list,
#                         }
#                         ret_list.append(ret_data)

#                         if len(ret_list) == max_count:
#                             break_roop = True
#                             break

#                     if break_roop:
#                         break

#             else:
#                 raise Exception("failed to access twitter.com")

#         except Exception as e:
#             raise Exception(e)

#         return ret_list

#     def get_identified_user_favlist(self, user_id, max_count, identifies_image_size):
#         ret_list = []
#         try:
#             url = "https://api.twitter.com/1.1/favorites/list.json?"
#             params = {"screen_name": user_id, "count": 5000}

#             res = self.twitter.get(url, params=params)

#             break_roop = False
#             if res.status_code == 200:
#                 tweets = json.loads(res.text)
#                 for tweet in tweets:
#                     # メディアなしツイートの場合
#                     if "extended_entities" not in tweet:
#                         continue

#                     # ファボ数フィルタ
#                     if tweet["favorite_count"] < 5:
#                         continue

#                     entities = tweet["extended_entities"]
#                     if "media" in entities:
#                         illust_url_list = []
#                         photo_url_list = []
#                         is_photo_media = False

#                         user_info = tweet["user"]
#                         datetime_obj_utc = datetime.datetime.strptime(
#                             tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"
#                         )

#                         for media in entities["media"]:
#                             if media["type"] == "photo":
#                                 is_photo_media = True
#                                 media_url = media["media_url"]

#                                 if idf.do_identifiesImage(
#                                     media_url
#                                     + "?format=jpg&name="
#                                     + identifies_image_size
#                                 ):
#                                     illust_url_list.append(media_url)
#                                 else:
#                                     photo_url_list.append(media_url)

#                         # 画像ツイート以外はレスポンスしない
#                         if is_photo_media:
#                             ret_data = {
#                                 "ID": tweet["id"],
#                                 "UseID": user_info["screen_name"],
#                                 "DateTime": datetime_obj_utc.strftime(
#                                     "%Y-%m-%d %H:%M:%S"
#                                 ),
#                                 "illustUrlList": illust_url_list,
#                                 "PhotoUrlList": photo_url_list,
#                             }
#                             ret_list.append(ret_data)

#                         if len(ret_list) == max_count:
#                             break_roop = True
#                             break

#                     if break_roop:
#                         break

#             else:
#                 raise Exception("failed to access twitter.com")

#         except Exception as e:
#             raise Exception(e)

#         return ret_list

#     def get_user_image_tweets(self, user_id, opt_since, opt_until, max_count):

#         tweets_list = []

#         # 取得上限件数
#         if max_count == 0:
#             max_count = 1000

#         search_option_list = []

#         # ユーザ指定
#         search_option_list.append("from:" + user_id)

#         # 期間の指定
#         if opt_since == "" and opt_until == "":
#             d_today = datetime.date.today()

#             td = datetime.timedelta(weeks=4)
#             # 未指定の場合、検索範囲を1ヶ月以内に設定
#             opt_since = (d_today - td).strftime("%Y-%m-%d")
#             opt_until = d_today.strftime("%Y-%m-%d")

#         search_option_list.append("since:" + opt_since)
#         search_option_list.append("until:" + opt_until)

#         # 取得メディアの指定
#         search_option_list.append("filter:media")

#         # 除外するツイート設定
#         search_option_list.append("exclude:retweets")

#         query = " ".join(search_option_list)

#         image_tweet_list = []
#         id_list = set([])
#         # liveモードとimageで検索結果が異なるため両方で検索する
#         for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
#             if i >= max_count:
#                 break

#             if not tweet.id in id_list:
#                 id_list.add(str(tweet.id))

#                 image_tweet_list.append(
#                     [
#                         tweet.date,
#                         tweet.id,
#                         tweet.content,
#                         tweet.media,
#                         tweet.user.username,
#                     ]
#                 )

#         for i, tweet in enumerate(
#             sntwitter.TwitterSearchScraper(query).get_items("live")
#         ):
#             if i >= max_count:
#                 break

#             if not tweet.id in id_list:
#                 id_list.add(tweet.id)

#                 image_tweet_list.append(
#                     [
#                         tweet.date,
#                         tweet.id,
#                         tweet.content,
#                         tweet.media,
#                         tweet.user.username,
#                     ]
#                 )

#         tweets_df = pd.DataFrame(
#             image_tweet_list,
#             columns=["Datetime", "Tweet Id", "Text", "Media", "Username"],
#         )

#         return self.conv_tweets_df_to_jsonList(tweets_df)

#     def get_all_user_media_tweet(self, user_id):
#         try:
#             max_cnt = 1000

#             req_list = []
#             req_until = datetime.datetime.now() + datetime.timedelta(days=2)
#             req_since = req_until - datetime.timedelta(weeks=12)

#             # 3か月単位で検索する
#             for cnt in range(50):
#                 # 特定ユーザの画像ツイートIDを取得
#                 tweets_df = self.get_user_image_tweets(
#                     user_id,
#                     req_since.strftime("%Y-%m-%d"),
#                     req_until.strftime("%Y-%m-%d"),
#                     max_cnt,
#                 )

#                 json = self.conv_tweets_df_to_jsonList(tweets_df)
#                 if len(json) > 0:
#                     req_list.append(self.conv_tweets_df_to_jsonList(tweets_df))
#                 else:
#                     break
#                 req_until = req_since + datetime.timedelta(days=2)
#                 req_since = req_until - datetime.timedelta(weeks=12)

#             ret_list = []
#             id_set = set([])
#             for list in req_list:

#                 for tweet in list:
#                     id_set.add(tweet["id"])
#                     if not tweet["id"] in id_set:
#                         ret_list.append(tweet)
#             # 呼び出しもとでソートする
#             # sorted_list = sorted(list, reverse=True, key=lambda s: s["dateTime"])
#             return ret_list

#         except Exception as e:
#             raise Exception(e)

#     def get_user_profile(self, user_screen_name):

#         try:
#             res = self.api.get_user(user_screen_name)
#             return res
#         except Exception as e:
#             raise Exception(e)

#     def conv_tweets_df_to_jsonList(self, tweets_df, media_type=""):
#         # 検索対象のツイートを取得
#         ret_list = []

#         for datetime, tweetId, userName, media in zip(
#             tweets_df["Datetime"],
#             tweets_df["Tweet Id"],
#             tweets_df["Username"],
#             tweets_df["Media"],
#         ):
#             if media is not None:
#                 media_urls = []
#                 media_type = ""
#                 for mediaData in media:
#                     if len(media) > 0:
#                         if isinstance(mediaData, sntwitter.Photo):
#                             media_urls.append(mediaData.fullUrl)
#                             media_type = "photo"
#                         elif isinstance(mediaData, sntwitter.Video):
#                             media_urls.append(mediaData.thumbnailUrl)
#                             media_type = "video"

#                 tweetData = {
#                     "id": tweetId,
#                     "useID": userName,
#                     "dateTime": datetime._repr_base,
#                     "url": media_urls,
#                     "mediaType": media_type,
#                 }
#                 ret_list.append(tweetData)
#         return ret_list

#     def get_lists(self, user_id):
#         """リストオブジェクト取得メソッド
#          ツイッターの利用ユーザのリストを取得します

#         Args:

#         Returns:
#            list[]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception: twitterへのアクセスエラー時

#         Note:
#             リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
#         """

#         ret_list = []
#         try:
#             res = self.api.get_lists(user_id=user_id)

#             ret_list = []
#             for res_list in res:
#                 list_data = {
#                     "ID": res_list.id,
#                     "Name": res_list.name,
#                     "Member_count": res_list.member_count,
#                 }

#                 ret_list.append(list_data)

#             return ret_list
#         except Exception as e:
#             raise Exception(e)
