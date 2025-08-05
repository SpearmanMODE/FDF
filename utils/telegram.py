import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    print(f"[DEBUG] Token: {token}")
    print(f"[DEBUG] Chat ID: {chat_id}")
    print(f"[DEBUG] Message: {message}")

    if not token or not chat_id:
        print("[Telegram] ⚠️ Missing credentials. Skipping message.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "MarkdownV2",  # ← more lenient for formatting
    }

    try:
        response = requests.post(url, json=payload)
        print(f"[Telegram] Status: {response.status_code}")
        print(f"[Telegram] Response: {response.text}")
    except Exception as e:
        print(f"[Telegram] ❌ Exception: {e}")





