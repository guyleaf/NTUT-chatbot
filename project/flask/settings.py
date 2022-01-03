import secrets
from datetime import timedelta
from secretManager import access_secret_version

db_user = "gpu_a_service"
db_pass = access_secret_version(
    "projects/567768457788/secrets/GPU_A_SQL_PASSWORD", 1
)
db_name = "chatbots-gpu-a"

sql_instance_connection_name = "chatbot-project-3135:asia-east1:chatbots-gpu-a"


# Flask Settings
class FlaskSettings:
    DEBUG = False
    SECRET_KEY = access_secret_version("", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://"
        + f"{db_user}:{db_pass}@/{db_name}"
        + f"?unix_socket=cloudsql/{sql_instance_connection_name}"
    )
    LINE_CLIENT_ID = access_secret_version("CLIENT_ID", 1)
    LINE_CLIENT_SECRET = access_secret_version("CLIENT_SECRET", 1)

    SECRET_KEY = secrets.token_urlsafe(16)
    JWT_SECRET_KEY = secrets.token_urlsafe(16)
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


# Optional for development
service_account_key_path = "localServiceAccount.json"
