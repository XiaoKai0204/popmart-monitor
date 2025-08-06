def send_discord(name: str, url: str, img: str, status: str):
    if not DISCORD_WEBHOOK:
        raise ValueError("❌ 没有设置 DISCORD_WEBHOOK 环境变量")

    payload = {
        "content": "@everyone ⚡ 补货提醒！",
        "embeds": [
            {
                "title": name,
                "url": url,
                "description": f"库存状态: {status}",
                "color": 5763719,
                "thumbnail": {"url": img},
                "fields": [
                    {"name": "购买链接", "value": f"[点我购买]({url})"}
                ],
                "footer": {"text": "Popmart Labubu 补货监控"}
            }
        ]
    }

    resp = requests.post(DISCORD_WEBHOOK, json=payload)
    if resp.status_code != 204:
        print(f"❌ Discord 发送失败: {resp.text}")
