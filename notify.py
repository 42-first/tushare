import requests
from config import SEND_KEY

def send(msg):
    if not SEND_KEY:
        print("未配置SEND_KEY")
        return

    url = f"https://sctapi.ftqq.com/{SEND_KEY}.send"

    data = {
        "title": "📈 今日潜力股",
        "desp": msg
    }

    try:
        requests.post(url, data=data)
        print("✅ 推送成功")
    except Exception as e:
        print("❌ 推送失败", e)