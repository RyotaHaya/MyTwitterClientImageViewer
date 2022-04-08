# import os

# os.getcwd()
# from google.oauth2 import service_account
# import googleapiclient.discovery

# import json
# from pprint import pprint

# import sqlalchemy

# db_name = os.environ.get("DB_NAME")
# db_user = os.environ.get("DB_USER_NAME")
# db_pass = os.environ.get("DB_PASSWORD")
# instance_connection_name = "pictcaf-dev-5533548"

# SCOPES = ["https://www.googleapis.com/auth/sqlservice.admin"]
# SERVICE_ACCOUNT_FILE = "../db_credentials.json"

# print(os.path.exists(SERVICE_ACCOUNT_FILE))

# credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)

# service = googleapiclient.discovery.build("sqladmin", "v1beta4", credentials = credentials)

# request = service.databases().get(project = "twitter-illust-image-api", instance = instance, database = DB_NAME)
# response = request.execute()  # returns a dictionary with the data

# pprint(response)
