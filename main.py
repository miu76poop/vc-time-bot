import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import discord

# --- Renderのポート検出用Webサーバー ---
def run_http_server():
    # Renderが指定するポートを確実に取得する（デフォルトは8080）
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Webサーバーを別スレッドで裏で動かす
threading.Thread(target=run_http_server, daemon=True).start()

# --- Discord Botの処理 ---
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

client = discord.Client(intents=intents)

# 指定のボイスチャンネルID
VOICE_CHANNEL_ID = 1462536983619309603

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        channel = client.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect(reconnect=True)
            print(f"Connected to voice channel: {channel.name}")
        else:
            print(f"Voice channel with ID {VOICE_CHANNEL_ID} not found.")
    except Exception as e:
        print(f"Failed to connect to voice: {e}")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    client.run(TOKEN)
else:
    print("DISCORD_TOKEN is not set.")
