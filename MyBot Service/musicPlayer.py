import os
import discord
import sqlite3
import time
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
from youtube_dl import YoutubeDL
import asyncio

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = commands.Bot(command_prefix="*", intents=intents)

#Sqlite Connection Code
dataConn = sqlite3.connect('C:\All Stuff\Programming\mybot\MyBot Service\RPGdata.db')
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

#Music Bot TOOLS - Support functions
def play(vClient, mpeg_ops, ydl_ops, reqUrl):
    with YoutubeDL(ydl_ops) as ydl:
        info = ydl.extract_info(reqUrl, download=False)
    URL = info['url']
    PCMObj = discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg-4.4-full_build/ffmpeg-4.4-full_build/bin/ffmpeg.exe", source=URL, before_options=mpeg_ops)
    vClient.play(PCMObj)
    return info
            
    

#Music Bot COMMANDS - Used by users to control operations
@client.command()
async def playtube(ctx, url, loopChoice):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    vc = client.get_channel(902016508908150824)
    voiceClient = await vc.connect()

    if loopChoice == "loopOn":
        if not voiceClient.is_playing():
            urlInfo = play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, url)
            await ctx.channel.send("Joined VC, playing requested music.")
            while True:
                await asyncio.sleep(urlInfo['duration'])
                await asyncio.sleep(2)
                play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, url)

    else:
        if not voiceClient.is_playing():
            play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, url)
            voiceClient.is_playing()
            await ctx.channel.send("Joined VC, playing requested music")
            
@client.command()
async def pause(ctx):
    voiceClient = client.voice_clients[0]
    voiceClient.pause()
    await ctx.channel.send("Paused!")

@client.command()
async def resume(ctx):
    voiceClient = client.voice_clients[0]
    voiceClient.resume()
    await ctx.channel.send("Resumed!")

@client.command()
async def stop(ctx):
    voiceClient = client.voice_clients[0]
    voiceClient.stop()
    await ctx.channel.send("Stopped playing!")

@client.command()
async def dc(ctx):
    voiceClient = client.voice_clients[0]
    await voiceClient.disconnect()
    await ctx.channel.send("Disconnected!")

#Caching Commands

#Save song to Cache
@client.command()
async def save(ctx, name, url):
    cursor.execute('INSERT INTO PLAYCACHE VALUES (?, ?, ?);', (ctx.author.name, name, url,))
    dataConn.commit()

#Play song from Cache
@client.command()
async def cacheplay(ctx, name, loop):
    #Returns all songs cached for user
    cacheSongs = cursor.execute('SELECT SONGNAME, URL FROM PLAYCACHE WHERE USERNAME = ?', (ctx.author.name,))
    for row in cacheSongs:
        if row[0] == name:
            url = row[1]
            await playtube(ctx, row[1], loop)
            break
    
client.run(TOKEN)
