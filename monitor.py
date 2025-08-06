import requests
from bs4 import BeautifulSoup
import os

# 👉 这里改成你要监控的 Popmart 商品链接
URL = "https://popmart.sg/products/labubu-energy-3-0"

# Discord Webhook（存放在 GitHub Secrets）
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def check_stock():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    # 判断是否有“加入购物车”按钮
    if "Add to Cart" in resp.text or "Buy Now" in resp.text:
        send_discord(f"⚡ @everyone LABUBU 补货啦！快冲！\n👉 {URL}")
    else:
        print("还没补货")

def send_discord(msg: str):
    if not DISCORD_WEBHOOK:
        raise ValueError("❌ 没有设置 DISCORD_WEBHOOK 环境变量")
    payload = {"content": msg}
    resp = requests.post(DISCORD_WEBHOOK, json=payload)
    if resp.status_code != 204:
        print(f"❌ Discord 发送失败: {resp.text}")

if __name__ == "__main__":
    check_stock()
