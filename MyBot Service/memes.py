import os
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from random import randint

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = commands.Bot(command_prefix="*", intents=intents)

#Status indicator
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("Process memes active")
    
    
#Testing/debugging commands
@client.command()
async def test(ctx):
    await ctx.channel.send("TEST")

#Reddit Meme Commands (Uses Reddit API)
#WIP
@client.command()
async def meme(ctx):

#YM Jokes
#WIP
@client.command()
async def ym(ctx):
    


client.run(TOKEN)
