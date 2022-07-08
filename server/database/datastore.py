import datetime
import hashlib
import os
import sys

import google.cloud.datastore as datastore

from core import config as settings

sys.path.append(os.pardir)
os.environ.setdefault("GCLOUD_PROJECT", settings.GOOGLE_PROJECT_ID)

# dataStoreの初期化
datastore_client = datastore.Client.from_service_account_json("config/account_key.json")


class ClientManager:
    """Google CloudDatastoreクラス

    Google CloudDatastoreへアクセスするためのクライアント処理

    Attributes:
    """
    
    def __init__(self):
        self
    
    def create_auth_token(self, token: str, token_secret: str):
        """token情報作成
        TwitterAPIトークン情報を登録する。

        Args:
            token :クライアントトークン 
            token_secret:クライアントトークン
        """
        
        # saltの原文
        salt: str = token + settings.ENCRYPTION_KEY
        hash_str: str = hashlib.sha256(salt.encode()).hexdigest()
        
        key = datastore_client.key("user_token", hash_str)
        entity = datastore.Entity(key)
        entity['created_date'] = datetime.datetime.now()
        entity['token'] = hash_str
        entity['token_secret'] = token_secret
        
        # 登録実行
        datastore_client.put(entity)
    
    def get_auth_token(self, token):
        """token情報取得
        TwitterAPIトークン情報を取得する。

        Args:
            token :クライアントトークン
        """
        
        try:
            query = datastore_client.query(kind = "user_token")
            salt: str = token + settings.ENCRYPTION_KEY
            query.add_filter("__key__", "=", datastore_client.key("user_token", hashlib.sha256(salt.encode()).hexdigest()))
            
            ret = list(query.fetch())
            
            token_secret = ""
            if len(ret) > 0:
                token_secret: str = ret[0]["token_secret"]
            else:
                raise ("Not Login")
            
            return token_secret
        
        except Exception as e:
            raise Exception(e)
    
    # def create_key(self, kind_name, id):
    #     return self.client.key(kind_name, id)
    
    # def create_entity(self, key):
    #     return datastore.Entity(key)
    
    # def get(self, kind_name, id):
    #     try:
    #         key = self.client.key(kind_name, id)
    #         entity = self.client.get(key)
    #         return entity
    #     except Exception as e:
    #         raise Exception(e)
    
    # def get_list(self, kind_name):
    #     try:
    #         query = self.client.query(kind = kind_name)
    #         # fetches all the entities from the datastore
    #         all_keys = query.fetch()
    
    #         key = self.client.key(kind_name)
    #         entity = self.client.get(key)
    #         return entity
    #     except Exception as e:
    #         raise Exception(e)
    
    # def put(self, entity):
    #     try:
    #         self.client.put(entity)
    #     except Exception as e:
    #         raise Exception(e)
