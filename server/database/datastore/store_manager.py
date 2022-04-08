import datetime
import hashlib
import os
import random
import string
import sys

from gcloud import datastore

from core import config as settings

sys.path.append(os.pardir)

os.environ.setdefault("GCLOUD_PROJECT", settings.GOOGLE_PROJECT_ID)


def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)


#datastore_client = datastore.Client()
datastore_client = datastore.Client.from_service_account_json("account_key.json")


class ClientManager:
    
    # コンストラクタ
    def __init__(self):
        self
    
    def create_auth_token(self, token: str, token_secret: str):
        # ソルト
        dat: str = token + settings.ENCRYPTION_KEY
        hash_str = hashlib.sha256(dat.encode()).hexdigest()
        
        key = datastore_client.key("user_token", hash_str)
        entity = datastore.Entity(key)
        
        entity['created_date'] = datetime.datetime.now()
        # 原文が分からないようハッシュ化
        entity['token'] = hash_str
        entity['token_secret'] = token_secret
        # 登録実行
        datastore_client.put(entity)
    
    def get_auth_token(self, token):
        
        try:
            query = datastore_client.query(kind = "user_token")
            dat: str = token + settings.ENCRYPTION_KEY
            #query.add_filter("token", "=", hashlib.sha256(dat.encode()).hexdigest())
            query.add_filter("__key__", "=", datastore_client.key("user_token", hashlib.sha256(dat.encode()).hexdigest()))
            
            ret = list(query.fetch())
            
            token_secret = ""
            if len(ret) > 0:
                token_secret = ret[0]["token_secret"]
            else:
                raise ("No Login")
            
            return token_secret
        
        except Exception as e:
            raise Exception(e)
    
    def create_key(self, kind_name, id):
        return self.client.key(kind_name, id)
    
    def create_entity(self, key):
        return datastore.Entity(key)
    
    def get(self, kind_name, id):
        try:
            key = self.client.key(kind_name, id)
            entity = self.client.get(key)
            return entity
        except Exception as e:
            raise Exception(e)
    
    def get_list(self, kind_name):
        try:
            query = self.client.query(kind = kind_name)
            
            all_keys = query.fetch()  # fetches all the entities from the datastore
            
            key = self.client.key(kind_name)
            entity = self.client.get(key)
            return entity
        except Exception as e:
            raise Exception(e)
    
    def put(self, entity):
        try:
            self.client.put(entity)
        except Exception as e:
            raise Exception(e)
