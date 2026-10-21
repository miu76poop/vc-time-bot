import os
import discord
from flask import Flask
from threading import Thread

# 簡易Webサーバー（Renderに「動いてるよ」と伝えるため）
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Discord Botの処理
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

TOKEN = os.environ.get('DISCORD_TOKEN')

if __name__ == "__main__":
    keep_alive()
    client.run(TOKEN)
