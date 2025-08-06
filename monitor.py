import requests
from bs4 import BeautifulSoup
import os
import time

# 要监控的商品链接 + 名称
PRODUCTS = {
    "https://www.lazada.sg/products/i3339762748-s22353226995.html": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Lazada) – $37.90",
    "https://www.lazada.sg/products/pdp-i3437613695.html": "LABUBU THE MONSTERS 前方高能3.0系列盲盒 (Lazada) – $24.90",
    "https://www.lazada.sg/products/pdp-i3326516139.html": "LABUBU THE MONSTERS 坐坐派对盲盒 (Lazada) – $149.40",
    "https://www.lazada.sg/products/pdp-i3334915384.html": "LABUBU THE MONSTERS 心动马卡龙盲盒 (Lazada) – $24.90",

    "https://www.popmart.com/zh-hant-SG/products/6574/THE-MONSTERS-%E5%BF%83%E5%8B%95%E9%A6%AC%E5%8D%A1%E9%BE%8D%E5%A1%98%E8%86%A0%E8%87%89%E7%9B%B2%E7%9B%92": "LABUBU THE MONSTERS 心动马卡龙盲盒 (Popmart) – S$24.90",
    "https://www.popmart.com/zh-hant-SG/products/6572/THE-MONSTERS---%E5%9D%90%E5%9D%90%E6%B4%BE%E5%B0%8D%E6%90%AA%E8%86%A0%E6%AF%9B%E7%B5%A8%E7%9B%B2%E7%9B%92": "LABUBU THE MONSTERS 坐坐派对盲盒 (Popmart) – S$24.90",
    "https://www.popmart.com/zh-hans-SG/products/1149/LABUBU-HIDE-AND-SEEK-IN-SINGAPORE%E7%B3%BB%E5%88%97-%E6%90%AA%E8%86%A0%E6%AF%9B%E7%B5%A8%E6%8E%9B%E4%BB%B6": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Popmart) – S$37.90",

    "https://shopee.sg/POP-MART-LABUBU-HIDE-AND-SEEK-IN-SINGAPORE-SERIES-Vinyl-Plush-Doll-Pendant-i.1302248623.26473500180": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Shopee) – $37.90",
    "https://shopee.sg/POP-MART-LABUBU-HIDE-AND-SEEK-IN-SINGAPORE-SERIES-Vinyl-Plush-Doll-Pendant-Combo-set-i.1302248623.44402252224": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件套装 (Shopee) – $51.80",
    "https://shopee.sg/POP-MART-THE-MONSTERS-Have-a-Seat-Vinyl-Plush-Blind-Box-Action-Toys-Figure-Birthday-Gift-Kid-Toy-i.1302248623.29172981011": "LABUBU THE MONSTERS 坐坐派对盲盒单盒 (Shopee) – $24.90",
    "https://shopee.sg/POP-MART-THE-MONSTERS-Have-a-Seat-Vinyl-Plush-Blind-Box%EF%BC%88whole-set%EF%BC%89-i.1302248623.41558114307": "LABUBU THE MONSTERS 坐坐派对盲盒整端 (Shopee) – $149.40",
    "https://shopee.sg/POP-MART-THE-MONSTERS-Exciting-Macaron-Vinyl-Face-Blind-Box-i.1302248623.28924106333": "LABUBU THE MONSTERS 心动马卡龙盲盒单盒 (Shopee) – $24.90",
    "https://shopee.sg/POP-MART-THE-MONSTERS-Exciting-Macaron-Vinyl-Face-Blind-Box%EF%BC%88whole-set%EF%BC%89-i.1302248623.42108118140": "LABUBU THE MONSTERS 心动马卡龙盲盒整端 (Shopee) – $149.40",
    "https://shopee.sg/POP-MART-THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box-i.1302248623.26834776484": "LABUBU THE MONSTERS 前方高能3.0盲盒单盒 (Shopee) – $24.90",
    "https://shopee.sg/POP-MART-THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box-(Whole-Set)-i.1302248623.24344527163": "LABUBU THE MONSTERS 前方高能3.0盲盒整端 (Shopee) – $149.40"
}

# Discord Webhook（从 GitHub Secrets 里读取）
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def check_stock(url: str, name: str):
    """检测单个商品库存"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)

        # 直接判断关键字（不同平台可能不同）
        if any(key in resp.text for key in ["Add to Cart", "Buy Now", "加入购物车", "立即购买"]):
            send_discord(f"⚡ @everyone 补货啦！\n{name}\n👉 {url}")
        else:
            print(f"❌ 还没补货: {name}")
    except Exception as e:
        print(f"⚠️ 检查失败 {name}: {e}")


def send_discord(msg: str):
    """发送 Discord 消息"""
    if not DISCORD_WEBHOOK:
        raise ValueError("❌ 没有设置 DISCORD_WEBHOOK 环境变量")
    payload = {"content": msg}
    resp = requests.post(DISCORD_WEBHOOK, json=payload)
    if resp.status_code != 204:
        print(f"❌ Discord 发送失败: {resp.text}")


if __name__ == "__main__":
    for url, name in PRODUCTS.items():
        check_stock(url, name)
        time.sleep(2)  # 避免请求太快被封
