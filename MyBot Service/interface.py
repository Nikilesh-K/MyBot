import os
import discord
import sqlite3
import time
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
import asyncio
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
chatRef = ["CSTART ", "PROGSTART ", "PROGRESS ", "TERMINATE "]

#DB Table Names
chatbot = "CHATBOT"
calc = "CALCULATOR"

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("Process interface active")


def listen(username, subservice):
    while True:
        data = cursor.execute("SELECT * FROM " + subservice + ";")
        for row in data:
            if row[1] == username:
                response = row[3]
                if response != None and response != " ":
                    return response

def send(subservice, command, username):
    cursor.execute("UPDATE {subservice} SET TICKET = '{command}' WHERE USERNAME = '{username}';".format(subservice=subservice, command=command, username=username))
    dataConn.commit()

def resetDB(subservice, username):
    cursor.execute("UPDATE {subservice} SET RESPONSE = ' ' WHERE USERNAME = '{username}';".format(subservice=subservice, username=username))
    dataConn.commit()

@client.command()
async def tempcalc(ctx, mode, inputTemp):
    command = "TEMPCALC " + mode + " " + inputTemp
    send(calc, command, ctx.author.name)
    response = listen(ctx.author.name, calc)
    await ctx.channel.send(response)

    resetDB(calc, ctx.author.name)

@client.command()
async def startchat(ctx):
    #Create DM with author
    dm = await ctx.author.create_dm()

    #Check SESSION_STATUS
    data = cursor.execute("SELECT * FROM CHATBOT;")
    for row in data:
        if row[1] == ctx.author.name:
            if row[4] == 'False':
                await ctx.channel.send("Chat session started!")
                cursor.execute("UPDATE CHATBOT SET SESSION_STATUS = 'True' WHERE USERNAME = '{username}';".format(username=ctx.author.name))
                dataConn.commit()
                break
            else:
                await ctx.channel.send("You already have a chat session in progress with the ChatBot")
                return
            
    #CSTART
    startCmd = chatRef[0] + "-" + ctx.author.name
    send(chatbot, startCmd, ctx.author.name)
    response = listen(ctx.author.name, chatbot)
    resetDB(chatbot, ctx.author.name)
    await dm.send(response)

    #Wait for user response - not used for PROGSTART
    def check(m):
        if m.channel == dm:
            return m.content == m.content

    msg = await client.wait_for('message', check=check)
    
    #PROGSTART
    progStartCmd = chatRef[1] + "-" + ctx.author.name
    send(chatbot, progStartCmd, ctx.author.name)
    response = listen(ctx.author.name, chatbot)
    resetDB(chatbot, ctx.author.name)
    await dm.send(response)
    
    msg = None
    #Wait for user response - used for PROGRESS
    def check(m):
        if m.author.name == ctx.author.name and m.channel == dm:
            return m.content == m.content
    msg = await client.wait_for('message', check=check)
    
    #PROGRESS
    needToTerminate = False
    while needToTerminate == False:
        progressCmd = chatRef[2] + "-" + ctx.author.name + "-" + msg.content
        send(chatbot, progressCmd, ctx.author.name)
        await asyncio.sleep(2)
        responseToUser = listen(ctx.author.name, chatbot)
        resetDB(chatbot, ctx.author.name)
        await dm.send(responseToUser)
        
        #Keep listening for progression 
        progression = listen(ctx.author.name, chatbot)
        print(progression)
        
        #If progression is a termination
        if chatRef[3] in progression:
            progression = progression.replace(chatRef[3], '')
            needToTerminate = True
        await dm.send(progression)
        resetDB(chatbot, ctx.author.name)

        #Immediately breaks out of the loop upon termination to allow session to end
        if needToTerminate == True:
            break

        #Wait for user response - used for PROGRESS
        def check(m):
            if m.author.name == ctx.author.name and m.channel == dm:
                return m.content == m.content
        msg = await client.wait_for('message', check=check)
        
    cursor.execute("UPDATE CHATBOT SET SESSION_STATUS = 'False' WHERE USERNAME = '{username}';".format(username=ctx.author.name))
    dataConn.commit()        
client.run(TOKEN)
