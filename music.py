#Pretend this file doesn't even exist I think the whole thing is broken 💀


import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
  def _init_(self, bot):
    self.client = bot

  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("Join a voice channel to use this command.")
    voiceChannel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voiceChannel.connect()
    else:
      await ctx.voice_client.move_to(voiceChannel)

  @commands.command()
  async def leave(self, ctx):
    await ctx.voice_client.disconnect()

  @commands.command()
  async def play(self, ctx, url):
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':'bestaudio'}
    vc = ctx.voice_client

    with youtube_dl.YouTubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      url2 = info['formats'][0]['url']
      song = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      vc.play(song)
    
  
async def setup(bot):
 await bot.add_cog(music(bot))