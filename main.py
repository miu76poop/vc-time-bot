import os
import discord
from flask import Flask
from threading import Thread

# 1. Renderに「ポートを開いているWebアプリだよ」と伝えるための簡易サーバー
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Renderが自動指定するポート番号を安全に受け取る設定
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Discord Botのメイン処理
intents = discord.Intents.default()
intents.voice_states = True  # VCの検知に必要
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # VC常駐のための処理（必要に応じて記述）
    # 例: channel = await client.fetch_channel(チャンネルID)
    # await channel.connect(reconnect=True)

# トークンを環境変数から安全に取得
TOKEN = os.environ.get('DISCORD_TOKEN')

if __name__ == "__main__":
    keep_alive()  # 簡易サーバーを裏で起動
    client.run(TOKEN)
