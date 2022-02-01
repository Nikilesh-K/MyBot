import os
import discord
import sqlite3
import time
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
from youtube_dl import YoutubeDL
from requests import get
import asyncio

intents = discord.Intents.default()
intents.members = True

#Load Environment Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = commands.Bot(command_prefix="*", intents=intents)

#Sqlite Connection Code
dataConn = sqlite3.connect('C:\All Stuff\Programming\MyBot\SQLite Central DB\Central DB.db')
cursor = dataConn.cursor()

#Activation Indicator
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("Process musicPlayer active")

#Music Bot TESTING AND DEBUGGING - Used for connection debugging, etc.
@client.command()
async def connect(ctx):
    #Establish connection with vc
    vc = client.get_channel(849078196355989524)
    voiceClient = await vc.connect()

#Music Bot TOOLS - Support functions for commands

#Download a video from Youtube from user query, play video, return video metadata
def play(vClient, mpeg_ops, ydl_ops, query):
    with YoutubeDL(ydl_ops) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    URL = info['formats'][0]['url']
    PCMObj = discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg-4.4-full_build/ffmpeg-4.4-full_build/bin/ffmpeg.exe", source=URL, before_options=mpeg_ops)
    vClient.play(PCMObj)
    return info
    

#Music Bot COMMANDS - Used by users to control operations

#Play a song from Youtube, loop if needed - calls play()
@client.command()
async def playtube(ctx, query, loopChoice):
    YDL_OPTIONS = {'format': "best",
                   'noplaylist': True,
                   'source_address': '0.0.0.0'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    voice_state = ctx.author.voice
    if voice_state == None:
        await ctx.channel.send("Please connect to a voice channel first.")
        return
    vc = voice_state.channel
    voiceClient = await vc.connect()

    if loopChoice == "loopOn":
        if not voiceClient.is_playing():
            urlInfo = play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, query)
            await ctx.channel.send("Joined VC, playing: " + urlInfo['webpage_url'])
            while True:
                await asyncio.sleep(urlInfo['duration'])
                await asyncio.sleep(2)
                if voiceClient.is_paused():
                    continue
                play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, query)

    else:
        if not voiceClient.is_playing():
            urlInfo = play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, query)
            await ctx.channel.send("Joined VC, playing: " + urlInfo['webpage_url'])

#Pause player            
@client.command()
async def pause(ctx):
    voiceClient = client.voice_clients[0]
    voiceClient.pause()
    await ctx.channel.send("Paused!")

#Resume player
@client.command()
async def resume(ctx):
    voiceClient = client.voice_clients[0]
    voiceClient.resume()
    await ctx.channel.send("Resumed!")

#Stop player
@client.command()
async def stop(ctx):
    voiceClient = client.voice_clients[0]
    voiceClient.stop()
    await ctx.channel.send("Stopped playing!")

#Disconnect player
@client.command()
async def dc(ctx):
    voiceClient = client.voice_clients[0]
    await voiceClient.disconnect()
    await ctx.channel.send("Disconnected!")

client.run(TOKEN)
