import os

product_type = "GPU"
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
richmenu_for_admin_json_path = "richmenu/adminMenu.json"
richmenu_for_admin_image_path = "richmenu/admin.png"

# App Engine
web_url = "https://chatbot-project-3135.de.r.appspot.com"
