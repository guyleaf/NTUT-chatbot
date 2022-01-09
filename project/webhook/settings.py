import os

line_api_base_url = "https://api.line.me/v2/bot/"
# line
channel_secret = os.environ.get("CHANNEL_SECRET", "")
channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN", "")

# GCP
project_id = "chatbot-project-3135"
language_code = "zh-TW"

# richmenu
richmenu_for_customer_json_path = "richmenu/customerMenu.json"
richmenu_for_customer_image_path = "richmenu/customer.png"
richmenu_for_seller_json_path = "richmenu/sellerMenu.json"
richmenu_for_seller_image_path = "richmenu/seller.png"

# App Engine
web_url = "https://web-gpu-a-dot-chatbot-project-3135.de.r.appspot.com"
login_url = web_url + "/login"


# Cloud SQL
db_user = "gpu_a_service"
db_pass = os.environ.get("SQL_PASSWORD", "gpu_a_service")
db_name = "security"
sql_instance_connection_name = "chatbot-project-3135:asia-east1:chatbots-gpu-a"

DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@/{db_name}?unix_socket=/cloudsql/{sql_instance_connection_name}"
# DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@127.0.0.1/{db_name}"
