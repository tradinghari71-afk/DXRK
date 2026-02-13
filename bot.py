import yt_dlp
from discord.ext import tasks

GUILD_ID = 1456868284296069150
VOICE_CHANNEL_ID = 1456893607616184395

MUSIC_URL = "https://youtu.be/WPrhl0pFY_o?si=Rh-UJ9_NTBYb-b-T"

def get_audio_source(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(info['url']),
            volume=0.5
        )

@tasks.loop(seconds=30)
async def stay_connected():
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(VOICE_CHANNEL_ID)

    if channel is None:
        return

    vc = guild.voice_client

    if vc is None or not vc.is_connected():
        vc = await channel.connect()
        vc.play(get_audio_source(MUSIC_URL))

@bot.event
async def on_ready():
    print(f"Music Bot Online as {bot.user}")
    stay_connected.start()

@bot.command()
async def volume(ctx, volume: int):
    vc = ctx.voice_client
    if vc and vc.source:
        vc.source.volume = volume / 100
        await ctx.send(f"🔊 Volume set to {volume}%")
