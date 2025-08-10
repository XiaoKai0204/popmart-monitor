
import requests
import re
import json
import os

PRODUCTS = {
    # ... 你的商品字典，保持不变
}

STATUS_FILE = "last_status.json"
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def load_status():
    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_status(status_dict):
    with open(STATUS_FILE, "w") as f:
        json.dump(status_dict, f)

def parse_status(status_str):
    if "In Stock" in status_str:
        return "in_stock"
    elif "Sold Out" in status_str:
        return "sold_out"
    else:
        return "unknown"

def check_stock(url):
    # 你的库存检测逻辑，不变
    pass

def send_discord_message(info, url, status):
    # 你的Discord推送函数，不变
    pass

def monitor_products():
    last_status = load_status()

    for url, info in PRODUCTS.items():
        status_str = check_stock(url)
        print(f"Checking {info['name']}: {status_str}")
        status = parse_status(status_str)

        if url not in last_status:
            last_status[url] = status
            continue

        if last_status[url] == "sold_out" and status == "in_stock":
            send_discord_message(info, url, status_str)

        last_status[url] = status

    save_status(last_status)

if __name__ == "__main__":
    monitor_products()
