import os
import threading
import asyncio
from flask import Flask
import discord
from discord.opus import VoiceEncoder

# --- 1. Flaskを使った安全なWebサーバー（マルチスレッド対応） ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    # threaded=True でUptimeRobotのPingによる競合・クラッシュを防ぐ
    app.run(host='0.0.0.0', port=port, threaded=True)

# 別スレッドでWebサーバーを起動
threading.Thread(target=run_web, daemon=True).start()


# --- 2. Discord Botの処理 ---
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

# あなたのボイスチャンネルID
VOICE_CHANNEL_ID = 1462536983619309603

# --- 3. Discordのタイムアウト（自動切断）を防ぐための無音オーディオクラス ---
class SilentSource(discord.AudioSource):
    """
    Discord側に「無音の音声データ」を少しずつ送り続けることで、
    無言のまま放置されても切断されない（タイムアウトを防ぐ）ためのクラス
    """
    def __init__(self):
        self.opus_encoder = VoiceEncoder()

    def read(self):
        # Opus形式の無音パケット（20ms分の無音）を返し続ける
        # 20ミリ秒ごとに無音データを送信
        return b'\xF8\xFF\xFE'

    def is_opus(self):
        return True


@client.event
async def on_ready():
    print(f"========================================")
    print(f" 🚀 ログイン成功！ Bot名: {client.user} (ID: {client.user.id})")
    print(f" 参加しているサーバー数: {len(client.guilds)}")
    print(f"========================================")
    
    await asyncio.sleep(2)
    
    if len(client.guilds) == 0:
        print("⚠️ 【警告】ボットがどのDiscordサーバーにも招待されていません！")
        return

    for guild in client.guilds:
        print(f"サーバー確認中: {guild.name} (ID: {guild.id})")
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                # すでに接続していれば一度切断しておく（重複接続防止）
                if guild.voice_client:
                    await guild.voice_client.disconnect()

                # ボイスチャンネルに接続
                voice_client = await channel.connect(reconnect=True)
                print(f"✨ 【大成功】ボイスチャンネル '{channel.name}' に接続しました！")
                
                # ★ タイムアウト（30分での自動切断）を防ぐため、無音の音声を流し続ける
                if not voice_client.is_playing():
                    voice_client.play(SilentSource())
                    print("🎧 タイムアウト防止用の無音ストリーミングを開始しました。")

                return
            except Exception as e:
                print(f"❌ ボイスチャンネル接続エラー: {e}")
                
    print(f"⚠️ 警告: 指定されたID ({VOICE_CHANNEL_ID}) のチャンネルが見つかりませんでした。")


# --- 4. 万が一、何かの拍子に切断されたときに自動で再接続＆無音を再開する処理 ---
@client.event
async def on_voice_state_update(member, before, after):
    # ボット自身の状態の変化を監視
    if member.id == client.user.id:
        # ボットが意図せずチャンネルから追い出されたり切断された場合
        if before.channel is not None and after.channel is None:
            print("⚠️ ボットがボイスチャンネルから切断されました。再接続を試みます...")
            await asyncio.sleep(3)
            try:
                guild = before.channel.guild
                channel = guild.get_channel(VOICE_CHANNEL_ID)
                if channel:
                    voice_client = await channel.connect(reconnect=True)
                    if not voice_client.is_playing():
                        voice_client.play(SilentSource())
                    print("✨ 再接続に成功し、無音ストリーミングを再開しました！")
            except Exception as e:
                print(f"❌ 再接続エラー: {e}")


TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    print("Discordボットを起動しています...")
    client.run(TOKEN)
else:
    print("エラー: DISCORD_TOKEN が設定されていません。")
