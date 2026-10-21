import os
import asyncio
from aiohttp import web
import discord

# --- Renderのポート監視用ミニWebサーバー（aiohttp使用） ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

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

async def main():
    # WebサーバーとDiscordボットを同時に起動する
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("DISCORD_TOKEN is not set.")
        return

    await start_web_server()
    await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
