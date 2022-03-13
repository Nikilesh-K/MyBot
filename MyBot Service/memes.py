import os
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
import requests

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
REDDIT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET_TOKEN')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
client = commands.Bot(command_prefix="*", intents=intents)

#Status indicator
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("Process memes active")

#REDDIT - Pull recent posts off of Reddit

#Find a meme from Reddit
@client.command()
async def meme(ctx):
    auth = requests.auth.HTTPBasicAuth(REDDIT_ID, REDDIT_SECRET)
    data = {'grant_type': 'password',
            'username': REDDIT_USERNAME,
            'password': REDDIT_PASSWORD}
    headers = {'User-Agent': 'MyBot/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    token = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {token}"}}

    posts = requests.get("https://oauth.reddit.com/r/memes", headers=headers)
    postData = posts.json()
    postNum = len(postData['data']['children'])
    post = postData['data']['children'][randint(0, postNum - 1)]
    await ctx.channel.send(post['data']['title'])
    await ctx.channel.send(post['data']['url'])
    
client.run(TOKEN)
