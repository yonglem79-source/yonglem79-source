import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

STOCK_CODE = os.environ.get("STOCK_CODE", "318060")
STOCK_NAME = os.environ.get("STOCK_NAME", "그래피")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID 환경 변수가 필요합니다. "
        ".env.example을 복사해 .env를 만들고 값을 채워주세요."
    )

PRICE_CHANGE_THRESHOLD_PCT = float(os.environ.get("PRICE_CHANGE_THRESHOLD_PCT", "5.0"))
STATE_FILE = os.environ.get("STATE_FILE", "state.json")
