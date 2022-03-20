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
    URL = info['formats'][2]['url']
    PCMObj = discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg-4.4-full_build/ffmpeg-4.4-full_build/bin/ffmpeg.exe", source=URL, before_options=mpeg_ops)
    vClient.play(PCMObj)
    return info

#Write to a Table in the DB
def writeDB(tableName, targetColumn, conditionColumn, targetData, conditionData):
    command = "UPDATE {tableName} SET {targetColumn} = {targetData} WHERE {conditionColumn} = {conditionData};"
    
    #Check data parameters - add quotes if str
    if isinstance(targetData, str):
        targetData = "'" + targetData + "'"
    if isinstance(conditionData, str):
        conditionData = "'" + conditionData + "'"
        
    cursor.execute(command.format(tableName = tableName, targetColumn = targetColumn, targetData = targetData, conditionColumn = conditionColumn, conditionData = conditionData))
    dataConn.commit()
    
#Retrieve all data from a Table
def retrieveTable(tableName):
    tableData = cursor.execute("SELECT * FROM {table};".format(table = tableName))
    return tableData

#Retrieve data for a specified target (eg. user)
def RetrieveDataFromTarget(rpgData, targetIndex, target, requestedIndex):
    for row in rpgData:
        if row[targetIndex] == target:
            return row[requestedIndex]


#Music Bot COMMANDS - Used by users to control operations

#Play a song from Youtube, loop if needed - calls play()
@client.command()
async def playtube(ctx, query, loopChoice):
    YDL_OPTIONS = {'format': 'bestaudio', 'extractaudio': True, 'noplaylist': True, 'continue': True}
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

#Add song to playlist
@client.command()
async def add(ctx, song):
    playlistTable = retrieveTable("PLAYLIST")
    currentSongs = RetrieveDataFromTarget(playlistTable, 1, ctx.author.name, 2)
    processedSong = song.replace('-', '')
    writeDB("PLAYLIST", "SONGS", "USERNAME", currentSongs + "-" + processedSong, ctx.author.name)
    await ctx.channel.send("Added ***" + song + "*** to your playlist")

@client.command()
async def playlist(ctx):
    embed = discord.Embed(
        title=ctx.author.name + "'s Playlist",
        color=discord.Color.blue())
    playlistTable = retrieveTable("PLAYLIST")
    currentSongs = RetrieveDataFromTarget(playlistTable, 1, ctx.author.name, 2)
    songList = currentSongs.split('-')
    for song in songList:
        if song == '' or song == '-':
            continue
        else:
            embed.add_field(name=song, value='\u200b', inline=False)
    embed.add_field(name="Number of Songs: ", value=str(len(songList)), inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
async def shuffleplay(ctx):
    playlistTable = retrieveTable("PLAYLIST")
    currentSongs = RetrieveDataFromTarget(playlistTable, 1, ctx.author.name, 2)
    songList = currentSongs.split('-')

    YDL_OPTIONS = {'format': 'bestaudio', 'extractaudio': True, 'noplaylist': True, 'continue': True}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    vc = ctx.author.voice.channel
    voiceClient = await vc.connect()
    
    while True:
        songIndex = randint(0, len(songList) - 1)
        if songList[songIndex] == '':
            continue
        urlInfo = play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, songList[songIndex])
        await ctx.channel.send("Joined VC, playing: " + urlInfo['webpage_url'])
        await asyncio.sleep(urlInfo['duration'])
        await asyncio.sleep(2)
        if voiceClient.is_paused():
            continue
    
@client.command()
async def listplay(ctx, loopMode):
    playlistTable = retrieveTable("PLAYLIST")
    currentSongs = RetrieveDataFromTarget(playlistTable, 1, ctx.author.name, 2)
    songList = currentSongs.split('-')

    YDL_OPTIONS = {'format': 'bestaudio', 'extractaudio': True, 'noplaylist': True, 'continue': True}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    vc = ctx.author.voice.channel
    voiceClient = await vc.connect()
    
    if loopMode == "loopOn":
        while True:
            for song in songList:
                if song == '':
                    continue
                urlInfo = play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, song)
                await ctx.channel.send("Joined VC, playing: " + urlInfo['webpage_url'])
                await asyncio.sleep(urlInfo['duration'])
                await asyncio.sleep(2)
                while voiceClient.is_paused():
                    continue
    else:
        for song in songList:
            if song == '':
                continue
            urlInfo = play(voiceClient, FFMPEG_OPTIONS, YDL_OPTIONS, song)
            await ctx.channel.send("Joined VC, playing: " + urlInfo['webpage_url'])
            await asyncio.sleep(urlInfo['duration'])
            await asyncio.sleep(2)
            while voiceClient.is_paused():
                    continue

client.run(TOKEN)
