import os
import discord
from flask import Flask
from threading import Thread

# 1. Renderに「ポートを開いているWebアプリだよ」と教えるための簡易サーバー
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Discord Botのメイン処理
intents = discord.Intents.default()
intents.voice_states = True  # VCの検知に必要なら
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# トークンを環境変数から安全に取得
TOKEN = os.environ.get('DISCORD_TOKEN')

if __name__ == "__main__":
    keep_alive()  # 簡易サーバーを裏で起動
    client.run(TOKEN)
