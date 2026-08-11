import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_message(text: str) -> None:
    response = requests.post(
        API_URL,
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=10,
    )
    response.raise_for_status()
