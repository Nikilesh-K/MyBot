import os
import discord
import sqlite3
import time
from discord.ext import commands
from dotenv import load_dotenv
from random import randint

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = commands.Bot(command_prefix="*", intents=intents)

#Sqlite Connection Code
dataConn = sqlite3.connect('C:\All Stuff\Programming\MyBot\SQLite Central DB\Central DB.db')
cursor = dataConn.cursor()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("Process interface active")


def listen(username, subservice):
    while True:
        data = cursor.execute("SELECT * FROM " + subservice)
        for row in data:
            if row[1] == username:
                response = row[3]
                if response != None and response != " ":
                    return response

def send(subservice, command, username):
    cursor.execute("UPDATE '{subservice}' SET TICKET = '{command}' WHERE USERNAME = '{username}'".format(subservice=subservice, command=command, username=username))
    dataConn.commit()

@client.command()
async def tempcalc(ctx, mode, inputTemp):
    command = "TEMPCALC " + mode + " " + inputTemp
    send("CALCULATOR", command, ctx.author.name)
    response = listen(ctx.author.name, "CALCULATOR")
    await ctx.channel.send(response)

    cursor.execute("UPDATE CALCULATOR SET TICKET = ' ' WHERE USERNAME = ' "+ ctx.author.name + "'")
    cursor.execute("UPDATE CALCULATOR SET RESPONSE = ' ' WHERE USERNAME = ' "+ ctx.author.name + "'" )
    dataConn.commit()

client.run(TOKEN)
