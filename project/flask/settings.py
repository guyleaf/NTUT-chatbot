﻿import os
from datetime import timedelta
from secretManager import access_secret_version

# Optional for development
if os.environ["FLASK_ENV"] != "production":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "localServiceAccount.json"


company_id = "TinkOQBepEnTO80eEICe"

db_user = "gpu_a_service"
db_pass = access_secret_version(
    "projects/567768457788/secrets/GPU_A_SQL_PASSWORD", 1
)
db_name = "security"
db_ip = os.environ.get("DATABASE_IP", "127.0.0.1:3306")

sql_instance_connection_name = "chatbot-project-3135:asia-east1:chatbots-gpu-a"

# richmenu
line_api_base_url = "https://api.line.me/v2/bot/"
web_url = "https://web-gpu-a-dot-chatbot-project-3135.de.r.appspot.com"
richmenu_for_customer_json_path = "richmenu/customerMenu.json"
richmenu_for_customer_image_path = "richmenu/customer.png"
richmenu_for_seller_json_path = "richmenu/sellerMenu.json"
richmenu_for_seller_image_path = "richmenu/seller.png"

# reports
customer_report = "https://datastudio.google.com/embed/reporting/85cbdaae-3703-4f2b-b4cb-553fdfb5488e/page/AI7iC"
others_report = "https://datastudio.google.com/embed/reporting/855cb2b2-bc9b-4015-9bc5-bc3ddfacc2a1/page/tG7iC"

# Flask Settings
class FlaskSettings:
    SECRET_KEY = access_secret_version(
        "projects/567768457788/secrets/GPU_A_SECRET_KEY_FOR_WEBSITE", 1
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    if os.environ["FLASK_ENV"] != "production":
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{db_user}:{db_pass}@{db_ip}/{db_name}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@/{db_name}?unix_socket=/cloudsql/{sql_instance_connection_name}"

    LINE_CLIENT_ID = access_secret_version(
        "projects/567768457788/secrets/GPU_A_LINE_LOGIN_CLIENT_ID", 1
    )
    LINE_CLIENT_SECRET = access_secret_version(
        "projects/567768457788/secrets/GPU_A_LINE_LOGIN_CLIENT_SECRET", 1
    )
    LINE_CHANNEL_SECRET_TOKEN = access_secret_version(
        "projects/567768457788/secrets/GPU_A_LINE_CHANNEL_SECRET_TOKEN", 1
    )
    LINE_CHANNEL_ACCESS_TOKEN = access_secret_version(
        "projects/567768457788/secrets/GPU_A_LINE_CHANNEL_ACCESS_TOKEN", 1
    )

    JWT_SECRET_KEY = access_secret_version(
        "projects/567768457788/secrets/GPU_A_JWT_SECRET_KEY_FOR_WEBSITE", 1
    )
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_CSRF_CHECK_FORM = True
