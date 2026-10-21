import os
import discord

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

client = discord.Client(intents=intents)

# 指定されたボイスチャンネルのIDを設定
VOICE_CHANNEL_ID = 1462536983619309603

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
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
client.run(TOKEN)
