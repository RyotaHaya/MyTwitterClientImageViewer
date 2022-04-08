# from __future__ import annotations
# import sys
# import os
# import cryptocode
# from core import config as settings
# import time

# sys.path.append(os.pardir)
# from routes.model import AuthParam
# from database.auth_manager import AuthManager
# from util import encryption

# class ApiCore:
#     """クラスの説明タイトル

#     クラスについての説明文

#     Attributes:
#         属性の名前 (属性の型): 属性の説明
#         属性の名前 (:obj:`属性の型`): 属性の説明.
#         aaa:

#     """

#     # コンストラクタ
#     def __init__(self):
#         self.db = AuthManager()

#     def get_auth_token(self, enc_hash_uid) -> dict[str, str]:
#         """トークンセッター
#             twitterログイン時にユーザ認証情報をDBに保存します

#         Args:
#             query:クエリパラメータ
#         Returns:
#             dict[str, object]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception:

#         Note:

#         """
#         try:
#             return self.db.get_twitter_token(enc_hash_uid)

#         except Exception as e:
#             raise Exception(e)

#     def post_create_auth_token(
#         self, query: dict[str, object], auth_param: AuthParam
#     ) -> dict[str, object]:

#         try:

#             decrypt_key = encryption.create_encryption_key()
#             enc_char = encryption.create_auth_token_str(
#                 auth_param.twitter_token, auth_param.twitter_token_secret, decrypt_key
#             )

#             return {
#                 "result": True,
#                 "t_token": enc_char,
#                 "use_dec_key": decrypt_key,
#             }

#             #    raise Exception("既に作成済みです")

#         except Exception as e:
#             raise Exception(e)

#     def post_set_auth_token(
#         self, query: dict[str, object], auth_param: AuthParam
#     ) -> dict[str, object]:
#         """トークンセッター
#             twitterログイン時にユーザ認証情報をDBに保存します

#         Args:
#             query:クエリパラメータ
#         Returns:
#             dict[str, object]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception:

#         Note:

#         """
#         try:

#             # encode_char = auth_param.firebaseUid + auth_param.twitter_token

#             # SHA256のハッシュ値
#             # https://en.wikipedia.org/wikienc_hash_uid = hashlib.sha256(encode_char.encode()).hexdigest()
#             # enc_hash_uid = cryptocode.encrypt(encode_char, settings.ENCRYPTION_KEY)
#             # current_user_token = self.get_auth_token(enc_hash_uid)

#             decrypt_key = encryption.create_encryption_key()
#             enc_char = encryption.create_auth_token_str(
#                 auth_param.twitter_token, auth_param.twitter_token_secret, decrypt_key
#             )

#             return {
#                 "result": True,
#                 "t_token": enc_char,
#                 "use_dec_key": decrypt_key,
#             }

#             # if current_user_token["uid"] == "":

#             # クライアント側の暗号化、復号化に必要なキー情報
#             # s_decrypt_key = encryption.create_encryption_key()
#             # encryption_s_token = cryptocode.encrypt(
#             #     cryptocode.encrypt(auth_param.twitter_token_secret, s_decrypt_key),
#             #     settings.ENCRYPTION_KEY,
#             # )

#             # encryption_s_token = cryptocode.encrypt(
#             #     encryption.encryption_auth_token_s(
#             #         auth_param.twitter_token_secret, s_decrypt_key
#             #     ),
#             #     settings.ENCRYPTION_KEY,
#             # )

#             # self.db.get_twitter_token(hash_uid)

#             # self.db.save_twitter_token(enc_hash_uid, encryption_s_token)

#             # return {
#             #     "result": True,
#             #     "t_token": enc_hash_uid,
#             #     "s_dec_key": s_decrypt_key,
#             # }
#             # else:
#             #    raise Exception("既に作成済みです")

#         except Exception as e:
#             raise Exception(e)

#     def decode_auth_token(
#         self, firebase_uid, enc_uid, enc_s_token, common_key
#     ) -> dict[str, object]:
#         """トークンセッター
#             twitterログイン時に必要なユーザ認証情報を返します。

#         Args:
#             enc_uid:クエリパラメータ
#             enc_uid:クエリパラメータ
#             enc_uid:common_key
#         Returns:
#             dict[str, object]: 取得したツイートのJsonオブジェクト
#         Raises:
#             Exception:

#         Note:

#         """
#         print("token decrypt")
#         start = time.time()

#         before_enc_char = cryptocode.decrypt(enc_uid, settings.ENCRYPTION_KEY)
#         # origin_twitter_outh_token_secret = encryption.decode_auth_token_s(
#         #     cryptocode.decrypt(enc_s_token, settings.ENCRYPTION_KEY), common_key
#         # )

#         elapsed_time = time.time() - start
#         print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
#         print("-----------------------------------------------")

#         origin_twitter_outh_token_secret = cryptocode.decrypt(
#             cryptocode.decrypt(enc_s_token, settings.ENCRYPTION_KEY), common_key
#         )

#         if not before_enc_char or not origin_twitter_outh_token_secret:
#             raise Exception("不正なリクエスト情報が送信されています")

#         return {
#             "twitter_token": before_enc_char.replace(firebase_uid, ""),
#             "twitter_token_secret": origin_twitter_outh_token_secret,
#         }

# api_core = ApiCore()
