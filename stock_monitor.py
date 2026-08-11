import json
import os
from typing import Optional

import requests
from bs4 import BeautifulSoup

from config import PRICE_CHANGE_THRESHOLD_PCT, STATE_FILE, STOCK_CODE, STOCK_NAME

PRICE_API_URL = f"https://polling.finance.naver.com/api/realtime/domestic/stock/{STOCK_CODE}"
REPORT_LIST_URL = (
    "https://finance.naver.com/research/company_list.naver"
    f"?searchType=itemCode&itemCode={STOCK_CODE}"
)


def _load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_state(state: dict) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def check_price_surge() -> Optional[str]:
    response = requests.get(PRICE_API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()["datas"][0]

    current_price = data["closePrice"]
    day_change_rate = data["fluctuationsRatio"]

    state = _load_state()
    last_price = state.get("last_price")
    state["last_price"] = current_price
    _save_state(state)

    if last_price is None:
        return None

    change_from_last_check = (current_price - last_price) / last_price * 100
    if abs(change_from_last_check) < PRICE_CHANGE_THRESHOLD_PCT:
        return None

    direction = "급등" if change_from_last_check > 0 else "급락"
    return (
        f"[{STOCK_NAME}({STOCK_CODE})] {direction} 감지\n"
        f"직전 확인가 {last_price:,}원 -> 현재가 {current_price:,}원 "
        f"({change_from_last_check:+.2f}%)\n"
        f"당일 등락률: {day_change_rate:+.2f}%"
    )


def check_new_reports() -> Optional[str]:
    response = requests.get(REPORT_LIST_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    latest_report = None
    for row in soup.select("table.type_1 tr"):
        link = row.select_one("a")
        if link and link.get("href") and link.get_text(strip=True):
            latest_report = {"title": link.get_text(strip=True), "href": link["href"]}
            break

    if latest_report is None:
        return None

    state = _load_state()
    last_report_href = state.get("last_report_href")
    state["last_report_href"] = latest_report["href"]
    _save_state(state)

    if last_report_href is None or last_report_href == latest_report["href"]:
        return None

    return (
        f"[{STOCK_NAME}({STOCK_CODE})] 새 리포트 발견\n"
        f"{latest_report['title']}\n"
        f"https://finance.naver.com{latest_report['href']}"
    )
