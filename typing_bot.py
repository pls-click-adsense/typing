#!/usr/bin/env python3
import time
import os
import threading
from flask import Flask
from curl_cffi import requests

# ========== Webサーバー部分 ==========
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Typing bot is running", 200

@app.route('/health')
def health():
    return "OK", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Webサーバー起動: ポート {port}")
    app.run(host="0.0.0.0", port=port)

# ========== Typing送信部分 ==========
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    try:
        with open("token.txt", "r") as f:
            TOKEN = f.read().strip()
    except:
        print("❌ トークンが設定されていません")
        exit(1)

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

def typing_loop():
    print("🔒 TLS完全偽装 + Typing送信 開始")
    print(f"対象チャンネル: {CHANNEL_ID}")
    print("間隔: 8秒")
    
    while True:
        try:
            response = session.post(URL, headers=headers)
            if response.status_code == 204:
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: ✅ Typing送信成功")
            else:
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: ❌ エラー {response.status_code}")
        except Exception as e:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: ❌ 例外: {e}")
        
        time.sleep(8)

# ========== メイン ==========
if __name__ == "__main__":
    # Typingループを別スレッドで起動
    typing_thread = threading.Thread(target=typing_loop)
    typing_thread.daemon = True
    typing_thread.start()
    
    # Webサーバーを起動（メインスレッド）
    run_web_server()
