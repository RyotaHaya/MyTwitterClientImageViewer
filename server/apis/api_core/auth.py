from __future__ import annotations

from routes.model import AuthParam
from util import encryption


class ApiCoreAuth:
    """クラスの説明タイトル

    クラスについての説明文

    Attributes:
        属性の名前 (属性の型): 属性の説明
        属性の名前 (:obj:`属性の型`): 属性の説明.
        aaa:

    """
    
    def post_create_auth_token(self, auth, auth_param: AuthParam) -> dict[str, object]:
        """ツイッタートークン情報の生成
        twitterへのリクエストトークンを暗号化された情報を発行する

        Returns:
            t_token:トークン情報
            use_dec_key:共通鍵
        """
        
        try:
            decrypt_key = encryption.create_encryption_key()
            enc_char = encryption.create_auth_token_str(
                auth,
                auth_param.twitter_token,
                auth_param.twitter_token_secret,
                decrypt_key,
            )
            
            return {
                "t_token": enc_char,
                "use_dec_key": decrypt_key,
            }
        except Exception as e:
            raise Exception(e)


api_core_auth = ApiCoreAuth()
