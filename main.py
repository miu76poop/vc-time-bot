import os
import threading
import asyncio
from http.server import HTTPServer, SimpleHTTPRequestHandler
import discord

# --- Renderのポート検出用Webサーバー ---
def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Webサーバーを別スレッドで裏で動かす
threading.Thread(target=run_http_server, daemon=True).start()

# --- Discord Botの処理 ---
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

# 指定のボイスチャンネルID
VOICE_CHANNEL_ID = 1462536983619309603

@client.event
async def on_ready():
    print(f"=== Logged in as {client.user} (ID: {client.user.id}) ===")
    print("Waiting for guilds to sync...")
    
    # サーバー情報が完全に読み込まれるまで少し待つ（3秒）
    await asyncio.sleep(3)
    
    connected = False
    for guild in client.guilds:
        print(f"Checking guild: {guild.name} (ID: {guild.id})")
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect(reconnect=True)
                print(f"SUCCESS: Connected to voice channel '{channel.name}' in guild '{guild.name}'")
                connected = True
                break
            except Exception as e:
                print(f"ERROR: Failed to connect to voice in guild {guild.name}: {e}")
                
    if not connected:
        print(f"WARNING: Voice channel with ID {VOICE_CHANNEL_ID} was not found in any connected guilds.")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    client.run(TOKEN)
else:
    print("DISCORD_TOKEN is not set.")
