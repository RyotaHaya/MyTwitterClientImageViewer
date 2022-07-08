"""設定ファイル読込み
* .envファイルから設定ファイルから読み込みする。

"""

import os

from dotenv import load_dotenv

load_dotenv("./.env")

API_USERNAME = os.environ.get("API_USERNAME")
API_PASSWORD = os.environ.get("API_PASSWORD")

ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")

# Auth configs.
API_SECRET_KEY = os.environ.get("API_SECRET_KEY")
API_ALGORITHM = os.environ.get("API_ALGORITHM")

GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
# infinity
# API_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["API_ACCESS_TOKEN_EXPIRE_MINUTES"])
# twitte api config
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.environ.get("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
