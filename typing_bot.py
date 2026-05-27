#!/usr/bin/env python3
import time
import os
import sys
import threading
from flask import Flask
from curl_cffi import requests

# 強制フラッシュ（ログを即時出力）
sys.stdout.reconfigure(line_buffering=True)

print("🚀 スクリプト起動", flush=True)

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
    print(f"🌐 Webサーバー起動: ポート {port}", flush=True)
    app.run(host="0.0.0.0", port=port, threaded=True)

# ========== Typing送信部分 ==========
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    print("❌ DISCORD_TOKEN環境変数が設定されていません", flush=True)
    sys.exit(1)

print(f"✅ トークン読み込み完了（長さ: {len(TOKEN)}文字）", flush=True)

CHANNEL_ID = "1507737734847139971"
URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/typing"

print(f"📡 対象チャンネル: {CHANNEL_ID}", flush=True)

try:
    print("🔧 curl_cffiセッション作成中...", flush=True)
    session = requests.Session(impersonate="chrome")
    print("✅ セッション作成完了", flush=True)
except Exception as e:
    print(f"❌ セッション作成失敗: {e}", flush=True)
    sys.exit(1)

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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

def typing_loop():
    print("🔄 Typing送信ループ開始", flush=True)
    count = 0
    
    while True:
        try:
            count += 1
            print(f"📤 送信中... (#{count})", flush=True)
            
            response = session.post(URL, headers=headers, timeout=30)
            
            print(f"📥 レスポンス: HTTP {response.status_code}", flush=True)
            
            if response.status_code == 204:
                print(f"✅ [{time.strftime('%H:%M:%S')}] Typing送信成功 (#{count})", flush=True)
            else:
                print(f"❌ [{time.strftime('%H:%M:%S')}] エラー {response.status_code} (#{count})", flush=True)
                if response.text:
                    print(f"    詳細: {response.text[:200]}", flush=True)
                    
        except requests.RequestException as e:
            print(f"❌ [{time.strftime('%H:%M:%S')}] リクエスト例外: {e}", flush=True)
        except Exception as e:
            print(f"❌ [{time.strftime('%H:%M:%S')}] 予期せぬ例外: {type(e).__name__}: {e}", flush=True)
        
        print(f"💤 {8}秒待機...", flush=True)
        time.sleep(8)

# ========== メイン ==========
if __name__ == "__main__":
    print("🏁 メイン関数開始", flush=True)
    
    # Typingループを別スレッドで起動
    print("▶️  Typingスレッド起動中...", flush=True)
    typing_thread = threading.Thread(target=typing_loop, daemon=True)
    typing_thread.start()
    print("✅ Typingスレッド起動完了", flush=True)
    
    # 少し待ってからWebサーバー起動（スレッドが落ちてないか確認）
    time.sleep(2)
    
    if not typing_thread.is_alive():
        print("⚠️  Typingスレッドが既に終了しています！", flush=True)
    else:
        print("✅ Typingスレッド生存確認", flush=True)
    
    # Webサーバーを起動（メインスレッド）
    print("🌐 Webサーバー起動準備...", flush=True)
    run_web_server()
