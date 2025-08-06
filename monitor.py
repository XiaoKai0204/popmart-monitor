import requests
from bs4 import BeautifulSoup
import os
import time

PRODUCTS = {
    "https://www.lazada.sg/products/i3339762748-s22353226995.html": {
        "name": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Lazada) – $37.90",
        "img": "https://s1.lazada.sg/images/ffbe75c6d74b77a54f4da423a37e3d65.jpg"
    },
    "https://www.popmart.com/sg/products/1149/LABUBU-HIDE-AND-SEEK-IN-SINGAPORE-SERIES-Vinyl-Plush-Doll-Pendant": {
        "name": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Popmart) – S$37.90",
        "img": "https://images.popmart.com/1149.jpg"
    },
    "https://shopee.sg/POP-MART-THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box-i.1302248623.26834776484": {
        "name": "LABUBU THE MONSTERS 前方高能3.0盲盒单盒 (Shopee) – $24.90",
        "img": "https://down-my.img.susercontent.com/file/sg-11134201-7rbll-lxj2d9q6m09i37"
    }
    # 你可以继续为其他商品添加 name 和 img 字段
}

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def check_stock(url: str, info: dict):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if any(k in resp.text for k in ["Add to Cart", "Buy Now", "加入购物车", "立即购买"]):
            send_discord(info["name"], url, info["img"], "🟢 有库存")
        else:
            print(f"❌ 还没补货: {info['name']}")
    except Exception as e:
        print(f"⚠️ 检查失败 {info['name']}: {e}")

def send_discord(name: str, url: str, img: str, status: str):
    if not DISCORD_WEBHOOK:
        raise ValueError("❌ 没有设置 DISCORD_WEBHOOK 环境变量")
    embed = {
        "title": name,
        "url": url,
        "description": f"库存状态: {status}",
        "color": 5763719,
        "thumbnail": {"url": img},
        "fields": [
            {"name": "购买链接", "value": f"[点我购买]({url})", "inline": False}
        ],
        "footer": {"text": "Popmart Labubu 补货监控"}
    }
    payload = {"content": "@everyone ⚡ 补货提醒！", "embeds": [embed]}
    resp = requests.post(DISCORD_WEBHOOK, json=payload)
    if resp.status_code != 204:
        print(f"❌ Discord 发送失败: {resp.text}")

if __name__ == "__main__":
    for url, info in PRODUCTS.items():
        check_stock(url, info)
        time.sleep(2)
