#!/usr/bin/env python3
import time
import os
from curl_cffi import requests

# Renderの環境変数からトークンを取得
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    # ローカルテスト用
    with open("token.txt", "r") as f:
        TOKEN = f.read().strip()

CHANNEL_ID = "1507737734847139971"
URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/typing"

# Chromeの指紋を完全偽装
session = requests.Session(impersonate="chrome")

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Sec-Ch-Ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Origin": "https://discord.com",
    "Referer": "https://discord.com/channels/@me",
}

print("🔒 TLS完全偽装 + Typing送信 開始")
print("偽装: Chrome")
print("間隔: 8秒")

while True:
    try:
        response = session.post(URL, headers=headers)
        if response.status_code == 204:
            print(f"{time.strftime('%H:%M:%S')}: ✅ 成功")
        else:
            print(f"{time.strftime('%H:%M:%S')}: ❌ {response.status_code}")
    except Exception as e:
        print(f"{time.strftime('%H:%M:%S')}: ❌ 例外: {e}")
    
    time.sleep(8)
