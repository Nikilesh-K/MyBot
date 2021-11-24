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
dataConn = sqlite3.connect('C:\All Stuff\Programming\MyBot\RPGdata.db')
cursor = dataConn.cursor()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("Process interface active")


#CBSS TESTING AND DEBUGGING METHODS - Used for testing and debugging purposes from dev end
#Test connection to Chatbot Sub Service
@client.command()
async def testchat(ctx):
    #Send TEST ticket
    cursor.execute("UPDATE CHATBOT SET TICKET = 'TEST TICKET' WHERE ID = 1")
    dataConn.commit()
    await ctx.channel.send("Test connection initiated!")
    time.sleep(1)
    #Monitor for ACK
    response = cursor.execute("SELECT RESPONSE FROM CHATBOT")
    for row in response:
        if row[0] == "TEST ACK":
            await ctx.channel.send("Acknowledgement received!")
            break
        
    #Reset Communications
    cursor.execute("UPDATE CHATBOT SET TICKET = 'EMPTY', RESPONSE = 'EMPTY' WHERE ID = 1;")
    dataConn.commit()

#CBSS SUPPORT METHODS - Used to support CBSS Commands
#Outputs response from CB
#WIP
@client.command()
async def PrintResponse(ctx):
    exitLoop = False
    #Way to exclude inaccurate EMPTY responses
    while(exitLoop == False):
        response = cursor.execute("SELECT RESPONSE FROM CHATBOT")
        for row in response:
            if row[0] != "EMPTY":
                await ctx.channel.send(row[0])
                exitLoop = True
                break
            else:
                continue

#CBSS COMMANDS - User commands for controlling CBSS operations
#Start session with Chatbot Sub Service
#UNSTABLE - DO NOT RUN
@client.command()
async def startsession(ctx):
    #Send Ticket
    cursor.execute("UPDATE CHATBOT SET TICKET = 'NEW SESSION' WHERE ID = 1;")
    dataConn.commit()
    time.sleep(3)
    #Print Response from CBSS
    PrintResponse()
    #Check for response from user
    def check(m):
        return m.content
    msg = await client.wait_for('message', check=check)
    #Send Response to CBSS
    cursor.execute("UPDATE CHATBOT SET TICKET = 'NEW MSG' + ? WHERE ID = 1;", (msg,))
    dataConn.commit()

    #Wait two seconds to allow CBSS to respond
    time.sleep(2)

    #Print 2nd Response
    PrintResponse()
    
        
        

    #Reset Communications
    cursor.execute("UPDATE CHATBOT SET TICKET = 'EMPTY', RESPONSE = 'EMPTY' WHERE ID = 1;")
    dataConn.commit()

    

#CalcService TESTING AND DEBUGGING - Used for testing/debugging from dev end
@client.command()
async def testcalc(ctx):
    #Send TEST ticket
    cursor.execute("UPDATE CALCULATOR SET TICKET = 'TEST TICKET' WHERE ID = 1")
    dataConn.commit()
    await ctx.channel.send("Test connection initiated!")

    #Monitor for ACK
    response = cursor.execute("SELECT RESPONSE FROM CALCULATOR")
    for row in response:
        if row[0] == "TEST ACK":
            await ctx.channel.send("Acknowledgement received!")
            break
        
    #Reset Communications
    cursor.execute("UPDATE CALCULATOR SET TICKET = 'EMPTY', RESPONSE = 'EMPTY' WHERE ID = 1;")
    dataConn.commit()

#CalcService COMMANDS - Used by users to control operations
@client.command()
async def tempcalc(ctx, mode, param):
    cursor.execute("UPDATE CALCULATOR SET TICKET = 'TEMPCALC {runmode} {value}' WHERE ID = 1;".format(runmode = mode, value = param))
    dataConn.commit()

    #Wait for Subservice to respond
    time.sleep(1)
    #Monitor for Response
    response = cursor.execute("SELECT RESPONSE FROM CALCULATOR;")
    for row in response:
        await ctx.channel.send(row[0])
        break
    #Reset Commmunications
    cursor.execute("UPDATE CALCULATOR SET TICKET = 'EMPTY', RESPONSE = 'EMPTY' WHERE ID = 1;")
    dataConn.commit()
client.run(TOKEN)
