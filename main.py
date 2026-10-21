import os
import discord
from flask import Flask
from threading import Thread

# 1. Render用簡易Webサーバー
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Discord Botのメイン処理
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

client = discord.Client(intents=intents)

# 【ここがポイント！】入らせたいボイスチャンネルのIDを数字で書く
# 例: VOICE_CHANNEL_ID = 123456789012345678
VOICE_CHANNEL_ID = 1462536983619309603  # ←ここに実際のVCのチャンネルIDを入れる！

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    # 指定したボイスチャンネルに接続する処理
    try:
        channel = client.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect(reconnect=True)
            print(f"Connected to voice channel: {channel.name}")
        else:
            print(f"Voice channel with ID {VOICE_CHANNEL_ID} not found.")
    except Exception as e:
        print(f"Failed to connect to voice: {e}")

TOKEN = os.environ.get('DISCORD_TOKEN')

if __name__ == "__main__":
    keep_alive()
    client.run(TOKEN)
