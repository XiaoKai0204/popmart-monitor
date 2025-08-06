import os
import requests

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_test():
    embed = {
        "title": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Lazada) – $37.90",
        "url": "https://www.lazada.sg/products/i3339762748-s22353226995.html",
        "color": 5763719,
        "thumbnail": {"url": "https://s1.lazada.sg/images/ffbe75c6d74b77a54f4da423a37e3d65.jpg"},
        "image": {"url": "https://s1.lazada.sg/images/ffbe75c6d74b77a54f4da423a37e3d65.jpg"},
        "fields": [
            {"name": "💰 PRICE", "value": "37.90 SGD", "inline": True},
            {"name": "🆔 PRODUCT", "value": "3339762748", "inline": True},
            {"name": "🆔 SKU", "value": "22353226995", "inline": True},
            {"name": "📊 STOCK", "value": "🟢 In Stock", "inline": True},
            {"name": "🛒 ATC", "value": "x1 | x2", "inline": True},
            {"name": "📅 RELEASE DATE", "value": "2025-08-06", "inline": False},
            {"name": "购买链接", "value": "[点我购买](https://www.lazada.sg/products/i3339762748-s22353226995.html)", "inline": False}
        ],
        "footer": {"text": "Popmart Labubu 补货监控"}
    }

    payload = {
        "content": "@everyone ⚡ 补货提醒！（演示消息）",
        "embeds": [embed]
    }

    resp = requests.post(DISCORD_WEBHOOK, json=payload)
    if resp.status_code != 204:
        print(f"❌ 发送失败: {resp.text}")
    else:
        print("✅ 测试消息已发送到 Discord")

if __name__ == "__main__":
    send_test()
