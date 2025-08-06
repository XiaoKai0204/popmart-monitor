
# monitor.py
import requests
import time

# 你的商品字典
PRODUCTS = {
    # Lazada
    "https://www.lazada.sg/products/i3339762748-s22353226995.html": {
        "name": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Lazada) – $37.90",
        "img": "https://s1.lazada.sg/images/ffbe75c6d74b77a54f4da423a37e3d65.jpg",
        "price": "37.90 SGD",
        "product_id": "3339762748",
        "sku": "22353226995"
    },
    "https://www.lazada.sg/products/pdp-i3437613695.html": {
        "name": "LABUBU THE MONSTERS 前方高能3.0系列盲盒 (Lazada) – $24.90",
        "img": "https://s1.lazada.sg/images/sg-11134201-7rblj-lxj3pp8w6g5c5d.jpg",
        "price": "24.90 SGD",
        "product_id": "3437613695",
        "sku": "N/A"
    },
    # ... 这里把你剩下的 13 个商品也放进去
}

# 你的 Discord webhook
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/xxxxx/yyyyy"

# 保存上一次库存状态
last_status = {}

# 发消息到 Discord
def send_discord_message(info, url, status):
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
                    {"name": "🛒 ATC", "value": "x1 | x2", "inline": True},
                    {"name": "📅 RELEASE DATE", "value": "2025-08-06", "inline": False},
                    {"name": "购买链接", "value": f"[点我购买]({url})", "inline": False},
                ],
                "color": 16711680
            }
        ]
    }
    requests.post(DISCORD_WEBHOOK, json=payload)

# 假的库存检测逻辑（先占位，等你改成爬虫/接口）
def check_stock(url):
    if "shopee" in url:  # 这里你可以改逻辑
        return "In Stock ✅"
    else:
        return "Sold Out ❌"

# 监控逻辑
def monitor_products():
    global last_status
    for url, info in PRODUCTS.items():
        status = check_stock(url)

        # 第一次运行 → 只记录，不推送
        if url not in last_status:
            last_status[url] = status
            continue

        # 库存状态变化才推送
        if last_status[url] != status:
            send_discord_message(info, url, status)
            last_status[url] = status

# 主循环
if __name__ == "__main__":
    while True:
        monitor_products()
        time.sleep(60)  # 每隔 60 秒检查一次
