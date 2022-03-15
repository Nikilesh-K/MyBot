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

#Command Reference lists
chatRef = ["CSTART ", "PROGSTART ", "PROGRESS "]
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

def resetDB(subservice, username):
    cursor.execute("UPDATE '{subservice}' SET TICKET = ' ' WHERE USERNAME = '{username}'".format(subservice=subservice, username=username))
    cursor.execute("UPDATE '{subservice}' SET RESPONSE = ' ' WHERE USERNAME = '{username}'".format(subservice=subservice, username=username))
    dataConn.commit()

@client.command()
async def tempcalc(ctx, mode, inputTemp):
    command = "TEMPCALC " + mode + " " + inputTemp
    send("CALCULATOR", command, ctx.author.name)
    response = listen(ctx.author.name, "CALCULATOR")
    await ctx.channel.send(response)

    resetDB("CALCULATOR", ctx.author.name)

@client.command()
async def startchat(ctx):
    #Create DM with author
    dm = await ctx.author.create_dm()

    #CSTART
    startCmd = chatRef[0] + ctx.author.name
    send("CHATBOT", startCmd, ctx.author.name)
    startResponse = listen(ctx.author.name, "CHATBOT")
    resetDB("CHATBOT", ctx.author.name)
    await dm.send(startResponse)

client.run(TOKEN)
