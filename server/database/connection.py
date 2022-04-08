import datetime
import logging
import os

import sqlalchemy

logger = logging.getLogger()


def init_connection_engine():
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]
        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]
        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]
        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]
    }
    
    if os.environ.get("DB_HOST"):
        if os.environ.get("DB_ROOT_CERT"):
            return init_tcp_sslcerts_connection_engine(db_config)
        return init_tcp_connection_engine(db_config)
    return init_unix_connection_engine(db_config)


def init_tcp_sslcerts_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_tcp_sslcerts]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]
    db_root_cert = os.environ["DB_ROOT_CERT"]
    db_cert = os.environ["DB_CERT"]
    db_key = os.environ["DB_KEY"]
    
    # Extract port from db_host if present,
    # otherwise use DB_PORT environment variable.
    host_args = db_host.split(":")
    if len(host_args) == 1:
        db_hostname = host_args[0]
        db_port = int(os.environ["DB_PORT"])
    elif len(host_args) == 2:
        db_hostname, db_port = host_args[0], int(host_args[1])
    
    ssl_args = {"ssl_ca": db_root_cert, "ssl_cert": db_cert, "ssl_key": db_key}
    
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername = "mysql+pymysql",
            username = db_user,  # e.g. "my-database-user"
            password = db_pass,  # e.g. "my-database-password"
            host = db_hostname,  # e.g. "127.0.0.1"
            port = db_port,  # e.g. 3306
            database = db_name,  # e.g. "my-database-name"
        ),
        connect_args = ssl_args,
        **db_config)
    # [END cloud_sql_mysql_sqlalchemy_create_tcp_sslcerts]
    
    return pool


def init_tcp_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_tcp]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]
    
    # Extract port from db_host if present,
    # otherwise use DB_PORT environment variable.
    host_args = db_host.split(":")
    if len(host_args) == 1:
        db_hostname = db_host
        db_port = os.environ["DB_PORT"]
    elif len(host_args) == 2:
        db_hostname, db_port = host_args[0], int(host_args[1])
    
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername = "mysql+pymysql",
            username = db_user,  # e.g. "my-database-user"
            password = db_pass,  # e.g. "my-database-password"
            host = db_hostname,  # e.g. "127.0.0.1"
            port = db_port,  # e.g. 3306
            database = db_name,  # e.g. "my-database-name"
        ),
        **db_config)
    # [END cloud_sql_mysql_sqlalchemy_create_tcp]
    
    return pool


def init_unix_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_socket]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
    
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername = "mysql+pymysql",
            username = db_user,  # e.g. "my-database-user"
            password = db_pass,  # e.g. "my-database-password"
            database = db_name,  # e.g. "my-database-name"
            query = {
                "unix_socket":
                    "{}/{}".format(
                        db_socket_dir,
                        instance_connection_name  # e.g. "/cloudsql"
                    )  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            },
        ),
        **db_config)
    # [END cloud_sql_mysql_sqlalchemy_create_socket]
    
    return pool


# This global variable is declared with a value of `None`, instead of calling
# `init_connection_engine()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = None


def create_tables():
    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS votes "
                        "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
                        "candidate CHAR(6) NOT NULL, PRIMARY KEY (vote_id) );")


def get_index_context():
    votes = []
    with db.connect() as conn:
        # Execute the query and fetch all results
        recent_votes = conn.execute("SELECT candidate, time_cast FROM votes "
                                    "ORDER BY time_cast DESC LIMIT 5").fetchall()
        # Convert the results into a list of dicts representing votes
        for row in recent_votes:
            votes.append({"candidate": row[0], "time_cast": row[1]})
        
        stmt = sqlalchemy.text("SELECT COUNT(vote_id) FROM votes WHERE candidate=:candidate")
        # Count number of votes for tabs
        tab_result = conn.execute(stmt, candidate = "TABS").fetchone()
        tab_count = tab_result[0]
        # Count number of votes for spaces
        space_result = conn.execute(stmt, candidate = "SPACES").fetchone()
        space_count = space_result[0]
    return {
        "recent_votes": votes,
        "space_count": space_count,
        "tab_count": tab_count,
    }


def save_vote():
    # Get the team and time the vote was cast.
    team = "TABS"
    time_cast = datetime.datetime.now(tz = datetime.timezone.utc)
    # Verify that the team is one of the allowed options
    
    # [START cloud_sql_mysql_sqlalchemy_connection]
    # Preparing a statement before hand can help protect against injections.
    stmt = sqlalchemy.text("INSERT INTO votes (time_cast, candidate)"
                            " VALUES (:time_cast, :candidate)")
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            conn.execute(stmt, time_cast = time_cast, candidate = team)
    except Exception as e:
        # If something goes wrong, handle the error in this section. This might
        # involve retrying or adjusting parameters depending on the situation.
        # [START_EXCLUDE]
        logger.exception(e)
        # [END_EXCLUDE]
    # [END cloud_sql_mysql_sqlalchemy_connection]


if __name__ == "__main__":
    # global db
    db = db or init_connection_engine()
    
    # app.run(host="127.0.0.1", port=8080, debug=True)
    # create_tables()
    # save_vote()
    get_index_context()
    get_index_context()
    get_index_context()
    get_index_context()
    get_index_context()