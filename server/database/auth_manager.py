# import os
import datetime
import logging

import sqlalchemy

from . import connection

logger = logging.getLogger()

# This global variable is declared with a value of `None`, instead of calling
# `init_connection_engine()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = None

db = connection.init_connection_engine()


class AuthManager:
    
    # コンストラクタ
    def __init__(self):
        self.db = db
    
    def get_twitter_token(self, hashed_uid: str):
        
        uid: str = ""
        s_token: str = ""
        created_at: datetime = None
        
        with self.db.connect() as conn:
            cur = conn.connection.cursor()
            
            stmt = "SELECT * FROM t_user_token WHERE uid =%s"
            
            cur.execute(stmt, hashed_uid)
            result = cur.fetchall()
            
            if len(result) > 0:
                for row in result:
                    uid = row[0]
                    s_token = row[1]
                    created_at = row[2]
            
            cur.close()
        
        return {
            "uid": uid,
            "s_token": s_token,
            "created_at": created_at,
        }
    
    def save_twitter_token(self, hash_uid: str, twitter_auth_token_secret: str):
        # Get the team and time the vote was cast.
        created_time = datetime.datetime.now(tz = datetime.timezone.utc)
        
        # Verify that the team is one of the allowed options
        
        # [START cloud_sql_mysql_sqlalchemy_connection]
        # Preparing a statement before hand can help protect against injections.
        stmt = sqlalchemy.text("INSERT INTO t_user_token (uid, s_tokne, created_at)"
                                " VALUES (:uid, :s_tokne, :created_at)")
        try:
            # Using a with statement ensures that the connection is always released
            # back into the pool at the end of statement (even if an error occurs)
            with self.db.connect() as conn:
                conn.execute(
                    stmt,
                    uid = hash_uid,
                    s_tokne = twitter_auth_token_secret,
                    created_at = created_time,
                )
        except Exception as e:
            # If something goes wrong, handle the error in this section. This might
            # involve retrying or adjusting parameters depending on the situation.
            # [START_EXCLUDE]
            logger.exception(e)
            raise Exception(e)
            # [END_EXCLUDE]
        # [END cloud_sql_mysql_sqlalchemy_connection]
