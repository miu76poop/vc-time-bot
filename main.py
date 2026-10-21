import os
import discord

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# 指定のボイスチャンネルID
VOICE_CHANNEL_ID = 1462536983619309603

@client.event
async def on_ready():
    print(f"========================================")
    print(f" 🚀 ログイン成功: {client.user}")
    print(f"========================================")
    
    # 参加しているサーバーをすべてチェック
    for guild in client.guilds:
        print(f"サーバー確認: {guild.name} (ID: {guild.id})")
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect(reconnect=True)
                print(f"✨ 【大成功】ボイスチャンネル '{channel.name}' に接続しました！")
                return
            except Exception as e:
                print(f"❌ 接続エラー: {e}")
                
    print("⚠️ 【警告】指定されたボイスチャンネルが見つかりませんでした。")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    print("ボットを起動中...")
    client.run(TOKEN)
else:
    print("エラー: DISCORD_TOKEN が設定されていません。")
