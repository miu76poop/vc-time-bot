import discord
from discord.ext import tasks
import datetime
import os

intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)

# --------【ここを自分のVCのチャンネルIDに書き換える】--------
TARGET_VC_ID = 1462536983619309603  # ← ここを自分のVCのIDにする
# ---------------------------------------------------------

# トークンは安全な場所（Koyeb）から自動で読み込みます
TOKEN = os.environ.get('DISCORD_TOKEN')

start_time = None

@client.event
async def on_ready():
    global start_time
    print(f'ログインしました: {client.user}')
    
    channel = client.get_channel(TARGET_VC_ID)
    if channel:
        await channel.connect(reconnect=True)
        start_time = datetime.datetime.now()
        print(f'{channel.name} に接続しました！')
        update_channel_name.start()

@tasks.loop(minutes=10)
async def update_channel_name():
    global start_time
    if start_time:
        elapsed = datetime.datetime.now() - start_time
        hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        time_str = f"{hours}:{minutes:02d}:{seconds:02d}"
        
        channel = client.get_channel(TARGET_VC_ID)
        if channel:
            new_name = f"voice-channel [{time_str}]"
            await channel.edit(name=new_name)

client.run(TOKEN)