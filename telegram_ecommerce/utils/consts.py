from .text import text_en
from .utils import load_json_file

credentials_path = "telegram_ecommerce/utils/.user_credentials.json"
credentials = load_json_file(credentials_path)
db_credentials = credentials["db_credentials"]
TEXT = text_en

