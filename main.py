import time

import schedule

from config import STOCK_CODE, STOCK_NAME
from stock_monitor import check_new_reports, check_price_surge
from telegram_notifier import send_telegram_message


def run_check() -> None:
    print(f"[{STOCK_NAME}({STOCK_CODE})] 모니터링 실행")
    for check in (check_price_surge, check_new_reports):
        try:
            message = check()
            if message:
                send_telegram_message(message)
        except Exception as exc:
            send_telegram_message(f"[{STOCK_NAME}({STOCK_CODE})] 모니터링 오류: {exc}")


def main() -> None:
    run_check()
    schedule.every().hour.do(run_check)
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
