import time

import schedule

from job import run_check


def main() -> None:
    run_check()
    schedule.every().hour.do(run_check)
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
