import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import discord

# --- Renderの24時間スリープ防止用Webサーバー ---
def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

# 別スレッドでWebサーバーを起動
threading.Thread(target=run_http_server, daemon=True).start()

# --- Discord Botの処理 ---
intents = discord.Intents.all()  # すべてのインテントを有効化してトラブルを防ぐ
client = discord.Client(intents=intents)

# 指定のボイスチャンネルID
VOICE_CHANNEL_ID = 1462536983619309603

@client.event
async def on_ready():
    print(f"========================================")
    print(f" ログイン成功！ Bot名: {client.user} (ID: {client.user.id})")
    print(f"========================================")
    
    # 参加しているすべてのサーバーを確認
    for guild in client.guilds:
        print(f"参加サーバー: {guild.name} (ID: {guild.id})")
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect(reconnect=True)
                print(f"✨ 【大成功】ボイスチャンネル '{channel.name}' に接続しました！")
                return
            except Exception as e:
                print(f"❌ 接続エラー: {e}")
                
    print("⚠️ 警告: 指定されたIDのボイスチャンネルが見つかりませんでした。ボットがそのサーバーに参加しているか確認してください。")

# ボットの起動
TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    client.run(TOKEN)
else:
    print("エラー: DISCORD_TOKEN が設定されていません。")
