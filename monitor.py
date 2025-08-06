def send_discord(name: str, url: str, img: str, status: str):
    if not DISCORD_WEBHOOK:
        raise ValueError("❌ 没有设置 DISCORD_WEBHOOK 环境变量")

    embed = {
        "title": name,
        "url": url,
        "color": 5763719,
        "thumbnail": {"url": img},   # 左侧小图
        "image": {"url": img},       # 下方大图
        "fields": [
            {"name": "💰 PRICE", "value": "24.90 SGD", "inline": True},
            {"name": "🆔 PRODUCT", "value": "6572", "inline": True},
            {"name": "🆔 SKU", "value": "10076", "inline": True},
            {"name": "📊 STOCK", "value": status, "inline": True},
            {"name": "🛒 ATC", "value": "x1 | x2", "inline": True},
            {"name": "📅 RELEASE DATE", "value": "2025-08-06", "inline": False},
            {"name": "购买链接", "value": f"[点我购买]({url})", "inline": False}
        ],
        "footer": {"text": "Popmart Labubu 补货监控"}
    }

    payload = {
        "content": "@everyone ⚡ 补货提醒！",
        "embeds": [embed]
    }

    resp = requests.post(DISCORD_WEBHOOK, json=payload)
    if resp.status_code != 204:
        print(f"❌ Discord 发送失败: {resp.text}")
