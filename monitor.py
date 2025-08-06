
import requests
import re
import time

# 商品字典（15个）
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
    "https://www.lazada.sg/products/pdp-i3326516139.html": {
        "name": "LABUBU THE MONSTERS 坐坐派对盲盒 (Lazada) – $149.40",
        "img": "https://s1.lazada.sg/images/sg-11134201-7rbld-lxj3pp8w6g5c5f.jpg",
        "price": "149.40 SGD",
        "product_id": "3326516139",
        "sku": "N/A"
    },
    "https://www.lazada.sg/products/pdp-i3334915384.html": {
        "name": "LABUBU THE MONSTERS 心动马卡龙盲盒 (Lazada) – $24.90",
        "img": "https://s1.lazada.sg/images/sg-11134201-7rbll-lxj2d9q6m09i37.jpg",
        "price": "24.90 SGD",
        "product_id": "3334915384",
        "sku": "N/A"
    },

    # Popmart 官网
    "https://www.popmart.com/zh-hant-SG/products/6574/THE-MONSTERS-%E5%BF%83%E5%8B%95%E9%A6%AC%E5%8D%A1%E9%BE%8D%E5%A1%98%E8%86%A0%E8%87%89%E7%9B%B2%E7%9B%92": {
        "name": "LABUBU THE MONSTERS 心动马卡龙盲盒 (Popmart) – S$24.90",
        "img": "https://images.popmart.com/20240814152343_6af980.png",
        "price": "24.90 SGD",
        "product_id": "6574",
        "sku": "N/A"
    },
    "https://www.popmart.com/zh-hant-SG/products/6572/THE-MONSTERS---%E5%9D%90%E5%9D%90%E6%B4%BE%E5%B0%8D%E6%90%AA%E8%86%A0%E6%AF%9B%E7%B5%A8%E7%9B%B2%E7%9B%92": {
        "name": "LABUBU THE MONSTERS 坐坐派对盲盒 (Popmart) – S$24.90",
        "img": "https://images.popmart.com/20240814152343_f87d39.png",
        "price": "24.90 SGD",
        "product_id": "6572",
        "sku": "N/A"
    },
    "https://www.popmart.com/zh-hans-SG/products/1149/LABUBU-HIDE-AND-SEEK-IN-SINGAPORE%E7%B3%BB%E5%88%97-%E6%90%AA%E8%86%A0%E6%AF%9B%E7%B5%A8%E6%8E%9B%E4%BB%B6": {
        "name": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Popmart) – S$37.90",
        "img": "https://images.popmart.com/20240814152343_f28e84.png",
        "price": "37.90 SGD",
        "product_id": "1149",
        "sku": "N/A"
    },

    # Shopee
    "https://shopee.sg/POP-MART-LABUBU-HIDE-AND-SEEK-IN-SINGAPORE-SERIES-Vinyl-Plush-Doll-Pendant-i.1302248623.26473500180": {
        "name": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件 (Shopee) – $37.90",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rbm4-lzj8h6g5o5c8df",
        "price": "37.90 SGD",
        "product_id": "26473500180",
        "sku": "N/A"
    },
    "https://shopee.sg/POP-MART-LABUBU-HIDE-AND-SEEK-IN-SINGAPORE-SERIES-Vinyl-Plush-Doll-Pendant-Combo-set-i.1302248623.44402252224": {
        "name": "LABUBU HIDE AND SEEK IN SINGAPORE 鱼尾狮挂件套装 (Shopee) – $51.80",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rbl8-lzj8h6g5o5c8a9",
        "price": "51.80 SGD",
        "product_id": "44402252224",
        "sku": "N/A"
    },
    "https://shopee.sg/POP-MART-THE-MONSTERS-Have-a-Seat-Vinyl-Plush-Blind-Box-Action-Toys-Figure-Birthday-Gift-Kid-Toy-i.1302248623.29172981011": {
        "name": "LABUBU THE MONSTERS 坐坐派对盲盒单盒 (Shopee) – $24.90",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rblq-lzj8h6g5o5c8cc",
        "price": "24.90 SGD",
        "product_id": "29172981011",
        "sku": "N/A"
    },
    "https://shopee.sg/POP-MART-THE-MONSTERS-Have-a-Seat-Vinyl-Plush-Blind-Box%EF%BC%88whole-set%EF%BC%89-i.1302248623.41558114307": {
        "name": "LABUBU THE MONSTERS 坐坐派对盲盒整端 (Shopee) – $149.40",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rbla-lzj8h6g5o5c8dd",
        "price": "149.40 SGD",
        "product_id": "41558114307",
        "sku": "N/A"
    },
    "https://shopee.sg/POP-MART-THE-MONSTERS-Exciting-Macaron-Vinyl-Face-Blind-Box-i.1302248623.28924106333": {
        "name": "LABUBU THE MONSTERS 心动马卡龙盲盒单盒 (Shopee) – $24.90",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rblz-lzj8h6g5o5c8aa",
        "price": "24.90 SGD",
        "product_id": "28924106333",
        "sku": "N/A"
    },
    "https://shopee.sg/POP-MART-THE-MONSTERS-Exciting-Macaron-Vinyl-Face-Blind-Box%EF%BC%88whole-set%EF%BC%89-i.1302248623.42108118140": {
        "name": "LABUBU THE MONSTERS 心动马卡龙盲盒整端 (Shopee) – $149.40",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rbly-lzj8h6g5o5c8ff",
        "price": "149.40 SGD",
        "product_id": "42108118140",
        "sku": "N/A"
    },
    "https://shopee.sg/POP-MART-THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box-i.1302248623.26834776484": {
        "name": "LABUBU THE MONSTERS 前方高能3.0盲盒单盒 (Shopee) – $24.90",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rbll-lxj2d9q6m09i37",
        "price": "24.90 SGD",
        "product_id": "26834776484",
        "sku": "N/A"
    },
    "https://shopee.sg/POP-MART-THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box-(Whole-Set)-i.1302248623.24344527163": {
        "name": "LABUBU THE MONSTERS 前方高能3.0盲盒整端 (Shopee) – $149.40",
        "img": "https://down-sg.img.susercontent.com/file/sg-11134201-7rbli-lzj8h6g5o5c8bc",
        "price": "149.40 SGD",
        "product_id": "24344527163",
        "sku": "N/A"
    }
}

# 你的 Discord Webhook
DISCORD_WEBHOOK = "你的Webhook URL"

# 保存上一次状态
last_status = {}

# 发送 Discord 消息
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
    try:
        requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        print(f"✅ 已推送到 Discord: {info['name']} - {status}")
    except Exception as e:
        print(f"❌ Discord 推送失败: {e}")

# 检查库存
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
            
            stock = r["data"]["stock"]
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

        # Popmart 暂未实现
        elif "popmart.com" in url:
            return "⚠️ Popmart check 未实现"

        return "Unknown ❓"

    except Exception as e:
        return f"Error ❌ ({str(e)})"

# 监控函数
def monitor_products():
    global last_status
    for url, info in PRODUCTS.items():
        status = check_stock(url)
        print(f"🔍 检查 {info['name']} → {status}")

        # 第一次运行：只记录，不推送
        if url not in last_status:
            last_status[url] = status
            continue

        # 状态变化才推送
        if last_status[url] != status:
            send_discord_message(info, url, status)
            last_status[url] = status  # 更新状态

# 主循环
if __name__ == "__main__":
    while True:
        monitor_products()
        time.sleep(60)  # 每隔 60 秒检查一次

