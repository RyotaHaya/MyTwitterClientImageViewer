# # -*- coding: utf-8 -*-
# """TwitterAPIversion2

# twitter api version2を実行します

# """

# import tweepy
# from core import config as settings

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

#     base_url = "https://api.twitter.com/"
#     request_token_url = base_url + "oauth/request_token"
#     authenticate_url = base_url + "oauth/authenticate"
#     access_token_url = base_url + "oauth/access_token"
#     base_json_url = "https://api.twitter.com/1.1/%s.json"
#     oauth_callback = "http://localhost:3000/"
#     authenticate_url = "https://api.twitter.com/oauth/authenticate"

#     # コンストラクタ
#     def __init__(self):
#         # フィールド

#         # OAuth2.0
#         bearer_token = "AAAAAAAAAAAAAAAAAAAAADqeIQEAAAAA8%2F5TEfTJWg54%2BYqXk0KJjGDTktk%3DPjg664rjysfEbHzw2YxPE1wXJfxzz5XquWuikR73aSr2kh5vfx"

#         self.client = tweepy.Client(
#             bearer_token=bearer_token,
#             consumer_key=settings.TWITTER_API_KEY,
#             consumer_secret=settings.TWITTER_API_SECRET_KEY,
#             access_token=settings.TWITTER_ACCESS_TOKEN,
#             access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
#         )

#     def get_home_timeline_tweets(self):
#         """タイムライン取得メソッド
#          ツイッターのホームタイムラインのツイート
#          を取得します

#         Args:

#         Returns:
#            list[]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception: tweepy実行に失敗した場合

#         Note:
#             リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
#         """

#         tweet_fields = [
#             "id",
#             "text",
#             "author_id",
#             "created_at",
#             "entities",
#             "referenced_tweets",
#             "public_metrics",
#         ]

#         user_fields = [
#             "id",
#             "name",
#             "username",
#             "created_at",
#         ]

#         media_fields = [
#             "preview_image_url",
#             "type",
#         ]

#         expansions = [
#             "author_id",
#             "referenced_tweets.id",
#             "in_reply_to_user_id",
#             "attachments.media_keys",
#             "attachments.poll_ids",
#             "geo.place_id",
#             "entities.mentions.username",
#             "referenced_tweets.id.author_id",
#         ]

#         try:
#             res1 = self.client.get_tweets(
#                 1304418413037498368,
#                 user_auth=True,
#                 user_fields=user_fields,
#                 expansions=expansions,
#                 tweet_fields=tweet_fields,
#             )

#         except Exception as e:
#             raise Exception(e)

#         return ""

#     def get_list_timeline_tweets_v2(
#         self, list_id, type="", page_count=1, pagination_token=""
#     ):
#         """リストタイムライン取得メソッド
#          ツイッターのリストのツイートを取得します(v2)

#         Args:
#             list_id:取得対象のリストID
#             type:取得対象のツイートを指定します。未指定:全てのツイート images:画像付きツイート videos:動画付きツイート media:画像、動画付きツイート
#             pagination_token:ページネーショントークン
#             page_count:指定したページ分の情報を取得します。
#         Returns:
#            list[]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception: twitterへのアクセスエラー時

#         Note:
#             リクエストしすぎるとtwitterのAPI制限に引っ掛かるため呼び出しは必要最小限とすること
#         """

#         tweet_fields = [
#             "id",
#             "text",
#             "author_id",
#             "created_at",
#             "entities",
#             "referenced_tweets",
#             "public_metrics",
#         ]

#         user_fields = [
#             "id",
#             "name",
#             "username",
#             "created_at",
#         ]

#         # media_fields = [
#         #     "preview_image_url",
#         #     "type",
#         # ]

#         expansions = [
#             "author_id",
#             "referenced_tweets.id",
#             "in_reply_to_user_id",
#             "attachments.media_keys",
#             "attachments.poll_ids",
#             "geo.place_id",
#             "entities.mentions.username",
#             "referenced_tweets.id.author_id",
#         ]

#         try:
#             res = tweepy.Paginator(
#                 self.client.get_list_tweets,
#                 list_id,
#                 user_auth=True,
#                 max_results=100,
#                 expansions=expansions,
#                 tweet_fields=tweet_fields,
#                 user_fields=user_fields,
#             ).flatten(limit=250)

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
#                 if "media" in tweet.entities:
#                     for media in tweet.extended_entities["media"]:
#                         media_type = media["type"]
#                         if media_type == "photo":
#                             media_urls.append(media["media_url"])

#                 # filter指定時はテキストのみのツイートはレスポンスしない
#                 if type != "" and len(media_urls) == 0:
#                     continue

#                 tweet_status = {
#                     "id": tweet.id,
#                     "createdTime": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#                     "text": tweet.text,
#                     "retweetId": retweeted_id,
#                     "retweeted": retweeted,
#                     "media": {"mediaType": media_type, "url": media_urls},
#                     "user_id": "",
#                     "user_name": "",
#                 }
#                 ret_list.append(tweet_status)

#                 # if len(ret_list) == res_count:
#                 #     break
#         except Exception as e:
#             raise Exception(e)

#             # res1 = self.client.get_list_tweets(
#             #     1304418413037498368,
#             #     user_auth=True,
#             #     user_fields=user_fields,
#             #     expansions=expansions,
#             #     tweet_fields=tweet_fields,
#             # )

#             # res2 = self.client.get_list_tweets(
#             #     1304418413037498368,
#             #     user_auth=True,
#             #     user_fields=user_fields,
#             #     # expansions=expansions,
#             #     tweet_fields=tweet_fields,
#             #     pagination_token=res1.meta["next_token"],
#             # )

#             # place_fields = (["full_name", "id"],)
#             # media_fields = (["type", "url", "alt_text", "public_metrics"],)

#             # res = tweepy.Paginator(
#             #     self.client.get_list_tweets,
#             #     list_id,
#             #     user_auth=user_auth,
#             #     expansions=expansions,
#             #     tweet_fields=tweet_fields,
#             #     user_fields=user_fields,
#             #     limit=250,
#             # )
