import os
from dotenv import load_dotenv

# ✅ Explicit path to .env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

from utils.telegram import send_telegram_message

send_telegram_message("✅ Telegram test from Flynn Delta Fund.")
