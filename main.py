import os
import threading
import asyncio
from flask import Flask
import discord

# --- 1. Flaskを使った確実にポートを開くWebサーバー ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    # host='0.0.0.0' で外部からのアクセスを受け付ける
    app.run(host='0.0.0.0', port=port)

# 別スレッドでWebサーバーを即座に起動
threading.Thread(target=run_web, daemon=True).start()


# --- 2. Discord Botの処理 ---
intents = discord.Intents.all()
client = discord.Client(intents=intents)

VOICE_CHANNEL_ID = 1462536983619309603

@client.event
async def on_ready():
    print(f"========================================")
    print(f" 🚀 ログイン成功: {client.user} (ID: {client.user.id})")
    print(f" 参加サーバー数: {len(client.guilds)}")
    print(f"========================================")
    
    await asyncio.sleep(3)
    
    if len(client.guilds) == 0:
        print("⚠️ 【注意】ボットがどのDiscordサーバーにも参加していません！")
        return

    for guild in client.guilds:
        print(f"サーバー確認中: {guild.name} (ID: {guild.id})")
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect(reconnect=True)
                print(f"✨ 【大成功】ボイスチャンネル '{channel.name}' に接続しました！")
                return
            except Exception as e:
                print(f"❌ 接続エラー: {e}")
                
    print(f"⚠️ 指定されたID ({VOICE_CHANNEL_ID}) のボイスチャンネルが見つかりませんでした。")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    print("Discordボットを起動中...")
    client.run(TOKEN)
else:
    print("エラー: DISCORD_TOKEN が設定されていません。")
