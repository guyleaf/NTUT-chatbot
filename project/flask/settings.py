from secretManager import access_secret_version

db_user = "gpu_a_service"
db_pass = access_secret_version("", 1)
db_name = "chatbots-gpu-a"

sql_instance_connection_name = "chatbot-project-3135:asia-east1:chatbots-gpu-a"


# Flask Settings
class FlaskSettings:
    DEBUG = False
    SECRET_KEY = access_secret_version("", 1)
    SECURITY_PASSWORD_HASH = "argon2"
    SECURITY_PASSWORD_SALT = access_secret_version("", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}


# Optional for development
service_account_key_path = "localServiceAccount.json"
