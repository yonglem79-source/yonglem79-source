from config import STOCK_CODE, STOCK_NAME
from telegram_notifier import send_telegram_message

if __name__ == "__main__":
    send_telegram_message(f"[{STOCK_NAME}({STOCK_CODE})] 알림 봇 텔레그램 연결 테스트 메시지입니다.")
    print("전송 완료")
