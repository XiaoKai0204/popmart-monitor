
import requests
import re
import json
import os
import time

# 商品字典示例（你可以补充完整）
PRODUCTS = {
    "https://www.lazada.sg/products/i3339762748-s22353226995.html": {
        "name": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Lazada) – $37.90",
        "img": "https://s1.lazada.sg/images/ffbe75c6d74b77a54f4da423a37e3d65.jpg",
        "price": "37.90 SGD",
        "product_id": "3339762748",
        "sku": "22353226995"
    },
    "https://shopee.sg/POP-MART-LABUBU-HIDE-AND-SEEK-IN-SINGAPORE-SERIES-Vinyl-Plush-Doll-Pendant-i.1302248623.26473500180": {
        "name": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Shopee) – $37.90",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rbm4-lzj8h6g5o5c8df",
        "price": "37.90 SGD",
        "product_id": "26473500180",
        "sku": "N/A"
    },
}

STATUS_FILE = "last_status.json"
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")  # 请在环境变量或GitHub Secrets里设置

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
    if "In Stock" in status_str or "✅" in status_str or "🟢" in status_str:
        return "in_stock"
    elif "Sold Out" in status_str or "❌" in status_str or "🔴" in status_str:
        return "sold_out"
    else:
        return "unknown"

def check_stock(url):
    try:
        # Shopee
        if "shopee.sg" in url:
            match = re.search(r"i\.(\d+)\.(\d+)", url)
            if not match:
                return "Unknown ❓"
            shopid, itemid = match.groups()
            api_url = f"https://shopee.sg/api/v4/item/get?itemid={itemid}&shopid={shopid}"

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
            }
            r = requests.get(api_url, headers=headers, timeout=10).json()
            stock = r["data"].get("stock", 0)
            if stock > 0:
                return f"In Stock ✅ ({stock})"
            else:
                return "Sold Out ❌"

        # Lazada
        elif "lazada.sg" in url:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10).text
            if '"soldOut":true' in r:
                return "Sold Out ❌"
            else:
                return "In Stock ✅"

        # Popmart (暂不支持自动检测，默认未知)
        elif "popmart.com" in url:
            return "Unknown (Popmart 未实现)"

        else:
            return "Unknown ❓"

    except Exception as e:
        return f"Error ❌ ({str(e)})"

def send_discord_message(info, url, status):
    if not DISCORD_WEBHOOK:
        print("❌ 未设置 DISCORD_WEBHOOK，无法发送通知")
        return

    payload = {
        "content": "@everyone ⚡ 补货提醒！",
        "embeds": [
            {
                "title": info["name"],
                "url": url,
                "image": {"url": info["img"]},
                "fields": [
                    {"name": "💰 PRICE", "value": info.get("price", "N/A"), "inline": True},
                    {"name": "🆔 PRODUCT", "value": info.get("product_id", "N/A"), "inline": True},
                    {"name": "🆔 SKU", "value": info.get("sku", "N/A"), "inline": True},
                    {"name": "📊 STOCK", "value": status, "inline": True},
                    {"name": "购买链接", "value": f"[点我购买]({url})", "inline": False},
                ],
                "color": 16711680
            }
        ]
    }

    try:
        r = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        if r.status_code == 204:
            print(f"✅ 已推送到 Discord: {info['name']} - {status}")
        else:
            print(f"❌ Discord 推送失败: HTTP {r.status_code} {r.text}")
    except Exception as e:
        print(f"❌ 发送 Discord 消息异常: {e}")

def monitor_products():
    last_status = load_status()

    for url, info in PRODUCTS.items():
        status_str = check_stock(url)
        print(f"🔍 检查 {info['name']} → {status_str}")
        status = parse_status(status_str)

        # 第一次检测，保存状态不通知
        if url not in last_status:
            last_status[url] = status
            continue

        # 只有之前售罄，现在有货才通知
        if last_status[url] == "sold_out" and status == "in_stock":
            send_discord_message(info, url, status_str)

        last_status[url] = status

    save_status(last_status)

if __name__ == "__main__":
    monitor_products()
