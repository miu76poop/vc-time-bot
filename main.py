import os
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import discord

# --- Webサーバー（24時間スリープ防止） ---
def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

# --- Discord Bot ---
intents = discord.Intents.all()
client = discord.Client(intents=intents)
VOICE_CHANNEL_ID = 1462536983619309603

@client.event
async def on_ready():
    print(f"--- ログイン成功: {client.user} ---")
    await client.wait_until_ready()
    time.sleep(3) # サーバー情報の同期をしっかり待つ
    
    for guild in client.guilds:
        print(f"サーバー確認中: {guild.name}")
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect(reconnect=True)
                print(f"【成功】チャンネル '{channel.name}' に接続しました！")
                return
            except Exception as e:
                print(f"接続失敗: {e}")
                
    print("【警告】指定されたボイスチャンネルが見つかりませんでした。")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    print("Botを起動しています...")
    client.run(TOKEN)
else:
    print("エラー: DISCORD_TOKEN が設定されていません。")
