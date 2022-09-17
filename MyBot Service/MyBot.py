#RPG
import os
import discord
import sqlite3
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from random import randint

#Intent Declarations
intents = discord.Intents.default()
intents.members = True

#DotENV loading
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = commands.Bot(command_prefix="*", intents=intents)


#Sqlite Connection Code
dataConn = sqlite3.connect('C:\All Stuff\Programming\MyBot\SQLite Central DB\Central DB.db')
cursor = dataConn.cursor()

#Wordle constants
word_list = ["FLOCK",
             "LIVER",
             "BALLS",
             "TOKEN",
             "SWIFT",
             "SERVE",
             "PASTE",
             "MOODY",
             "CLOUD",
             "MUDDY"]
yellow_emoji_id = "<:yellow_square:1002012573106978918>"
black_emoji_id = "<:black_large_square:1002012761087283220>"
green_emoji_id = "<:green_square:1002012957653352519>"

#Status Indicator
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("Process RPG active")
    
#This event is called whenever MyBot joins a new guild
#Initalizes all Data Tables upon joining
@client.event
async def on_guild_join():
    #Initalize RPG Table
    i = 1
    for member in ctx.guild.members:
        if member.bot:
            continue
        memberName = member.name
        cursor.execute("INSERT INTO MONEY_DATA VALUES (?, ?, ?);", (i, memberName, 0))
        i += 1
    dataConn.commit()
    await ctx.channel.send("Initalized RPG!")

    #Initalize Army Table
    i = 1
    for member in ctx.guild.members:
        if member.bot:
            continue
        cursor.execute("INSERT INTO ARMY_DATA (ID, USERNAME) VALUES (?, ?)", (i, member.name,))
        i += 1
    dataConn.commit()
    await ctx.channel.send("Initalized Army Database!")

#RPG COMMAND SUPPORT: Used in User Commands

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

#RPG USER COMMANDS: Used to run RPG operations by user

@client.command()
async def test(ctx):
    await ctx.channel.send("<:smile:1002011646178377838>")
    
#Work, increase Money balance by random amount
@client.command()
async def work(ctx):
    money = randint(0, 5000)
    await ctx.channel.send("You worked! You have earned: ***$" + str(money) + "!***")
    data = retrieveTable("MONEY_DATA")
    previousMoney = RetrieveDataFromTarget(data, 1, ctx.author.name, 2)        
    currentMoney = previousMoney + money
    writeDB("MONEY_DATA", "MONEY", "USERNAME", currentMoney, ctx.author.name)

#Check Balance
@client.command()
async def checkbal(ctx, member):
    data = retrieveTable("MONEY_DATA")
    if member == "me":
        money = RetrieveDataFromTarget(data, 1, ctx.author.name, 2)
        await ctx.channel.send("Your current balance is: **" + str(money) + "**")
    else:
        money = RetrieveDataFromTarget(data, 1, member, 2)
        if money == None:
            await ctx.channel.send("Sorry, that member doesn't exist.")
        else:
            await ctx.channel.send(member + "'s current balance is: **" + str(money) + "**")

#Check Server Balance
@client.command()
async def serverbal(ctx):
    data = retrieveTable("MONEY_DATA")
    embed = discord.Embed(
        title="Total Server Balances",
        color=discord.Color.red())
    for row in data:
        name=row[1]
        money=row[2]
        embed.add_field(name=name, value=str(money), inline=False)
    await ctx.channel.send(embed=embed)

#Check Shop
@client.command()
async def checkshop(ctx):
    data = retrieveTable("SHOP")
    embed = discord.Embed(
        title="Welcome to the Shop!",
        description="Check out these awesome items!",
        color=discord.Color.green())
    for row in data:
        name = row[1]
        itemType = row[2]
        cost = row[3]
        if itemType == "Weapon Level":
            weaponDamage = row[5]
            embed.add_field(name="{name} (${cost})".format(name=name, cost=str(cost)), value= "Type: {itemType}, Damage: {damage}".format(itemType=itemType, damage=str(weaponDamage)), inline=False)
        else:
            shipHealth = row[4]
            embed.add_field(name="{name} (${cost})".format(name=name, cost=str(cost)), value="Type: {itemType}, Health: {health}".format(itemType=itemType, health=str(shipHealth)), inline=False)
    await ctx.channel.send(embed=embed)

#Buy, decrease Money balance
@client.command()
async def buy(ctx, item):
    #Retrieve cost, type of item
    shopData = retrieveTable("SHOP")
    itemType = RetrieveDataFromTarget(shopData, 1, item, 2)
    shopData = retrieveTable("SHOP")
    cost = RetrieveDataFromTarget(shopData, 1, item, 3)

    #Subtract cost from user's funds, update database
    moneyData = retrieveTable("MONEY_DATA")
    currentMoney = RetrieveDataFromTarget(moneyData, 1, ctx.author.name, 2)
    currentMoney -= cost
    writeDB("MONEY_DATA", "MONEY", "USERNAME", currentMoney, ctx.author.name)
    await ctx.channel.send("Bought **{item}** for ***{cost}***.".format(item=item, cost=cost))

    #Update Army database with item level info
    armyData = retrieveTable("ARMY_DATA")
    if itemType == "Weapon Level":
        writeDB("ARMY_DATA", "WEAPON_LEVEL", "USERNAME", item, ctx.author.name)
    else:
        writeDB("ARMY_DATA", "SHIP_LEVEL", "USERNAME", item, ctx.author.name)

#Check army
@client.command()
async def checkarmy(ctx):
    armyData = cursor.execute("SELECT * FROM ARMY_DATA;")
    embed = discord.Embed(
        title=ctx.author.name + "'s Army:",
        color=discord.Color.purple())
    for row in armyData:
        if row[1] == ctx.author.name:
            embed.add_field(name="Ship Level:", value=row[2], inline=False)
            embed.add_field(name="Weapon Level:", value=row[3], inline=False)
            break
    await ctx.channel.send(embed=embed)

#Fight another user
@client.command()
async def fight(ctx, name):
    #PART 1: VERIFICATION - Verify that:
    #1. The author is not trying to fight themself
    #2. The entered username is valid and exists
    #3. Both users have a weapon and ship level

    #Check that the author name is not the same as the entered name
    if name == ctx.author.name:
        await ctx.channel.send("You can't fight yourself! Please try again.")
        return
    
    #Check if the user exists
    i = 1
    for member in ctx.guild.members:
        if member.name == name:
            break
        if i == ctx.guild.member_count:
            await ctx.channel.send("Sorry, that member does not exist. Please try again.")
            return
        i += 1



    #Check if both users have a ship/weapon level
    armyData = cursor.execute("SELECT * FROM ARMY_DATA;")
    for row in armyData:
        if row[1] == ctx.author.name:
            if row[2] != None and row[3] != None:
                pass
            else:
                await ctx.channel.send("Before you can fight, you will first need a Weapon/Ship Level. Please buy one from the Shop before fighting again.")
                return

        if row[1] == name:
            if row[2] != None and row[3] != None:
                break
            else:
                await ctx.channel.send("Sorry, the other player you are trying to fight does not have a Weapon/Ship Level.")
                return
            
    #PART 2: BATTLE
    authorShip = None
    authorWeapon = None
    opponentShip = None
    opponentWeapon = None

    authorHealth = None
    authorDamage = None
    opponentHealth = None
    opponentDamage = None

    #STAGE 1: Retrieve Ship and Weapon Levels for Author and Opponent
    armyData = cursor.execute("SELECT * FROM ARMY_DATA;")
    for row in armyData:
        if row[1] == ctx.author.name:
            authorShip = row[2]
            authorWeapon = row[3]
        if row[1] == name:
            opponentShip = row[2]
            opponentWeapon = row[3]

    
    await ctx.channel.send("Author Ship: " + authorShip + ", Author Weapon: " + authorWeapon)
    await ctx.channel.send("Opponent Ship: " + opponentShip + ", Opponent Weapon: " + opponentWeapon)

    
    #STAGE 2: Retrieve Health and Damage Levels for Author and Opponent from Shop
    shopData = cursor.execute("SELECT * FROM SHOP;")
    for row in shopData:
        itemName = row[1]
        if itemName == authorShip:
            authorHealth = row[4]
        if itemName == opponentShip:
            opponentHealth = row[4]

        if itemName == authorWeapon:
            authorDamage = row[5]
        if itemName == opponentWeapon:
            opponentDamage = row[5]


    await ctx.channel.send("Author Health: " + str(authorHealth) + ", Author Damage: " + str(authorDamage))
    await ctx.channel.send("Opponent Health: " + str(opponentHealth) + ", Opponent Damage: " + str(opponentDamage))
    
    #STAGE 3: Facilitate Battle
    message = await ctx.channel.send("***" + ctx.author.name + " has started a new battle with " + name + "! " + ctx.author.name + ", what would you like to do first? ***")
    counter = 1
    author = ctx.author.name
    opponent = name
    while True:
        def check(m):
            if m.content == 'attack':
                return m.content == 'attack' and m.channel == ctx.channel
            if m.content == 'skip':
                return m.content == 'skip' and m.channel == ctx.channel

        msg = await client.wait_for('message', check=check)
        if msg.content == 'attack':
            await ctx.channel.send("Attacking!")
            outcomeNum = randint(0, 100)
            #Opponent's turn for attack
            if counter % 2 == 0:
                if msg.author.name == author:
                    await ctx.channel.send("Sorry, something went wrong! Please try again.")
                    break
                if outcomeNum >= 50:
                    authorHealth = authorHealth - opponentDamage
                    await ctx.channel.send(opponent + " just dealt " + str(opponentDamage) + "! " + author + " now has " + str(authorHealth) + " left!")
                else:
                    await ctx.channel.send(opponent + " missed!")
                    
            #Author's turn for attack
            else:
                if msg.author.name == opponent:
                    await ctx.channel.send("Sorry, something went wrong! Please try again.")
                    break
                if outcomeNum >= 50:
                    opponentHealth = opponentHealth - authorDamage
                    await ctx.channel.send(ctx.author.name + " just dealt " + str(authorDamage) + "! " + opponent + " now has " + str(opponentHealth) + " left!")
                else:
                    await ctx.channel.send(ctx.author.name + " missed!")
        if msg.content == 'skip':
            #Opponent's turn
            if counter % 2 == 0:
                if msg.author.name == author:
                    await ctx.channel.send("Sorry, something went wrong! Please try again.")
                    break
                else:
                    await ctx.channel.send("Skipping!")
                    await ctx.channel.send(opponent + " has skipped their turn!")
            #Author's turn
            else:
                if msg.author.name == opponent:
                    await ctx.channel.send("Sorry, something went wrong! Please try again.")
                    break
                else:
                    await ctx.channel.send("Skipping!")
                    await ctx.channel.send(author + " has skipped their turn!")
            
            counter +=1
            continue
        if authorHealth <= 0:
            await ctx.channel.send(author + " has ran out of Health. " + opponent + " wins!")
            break
        if opponentHealth <= 0:
            await ctx.channel.send(opponent + " has ran out of Health. " + author + " wins!")
            break
        
        counter += 1

#Wordle - WIP
@client.command()
async def wordle(ctx):
    correct_word = word_list[randint(0, len(word_list) - 1)]
    print(correct_word)
    word_char = list(correct_word)
    total_attempts = 0
    output_record = ""
    
    for i in range(6):
        #Listen for valid word
        await ctx.channel.send("Enter word:")
        while True:
            def check(m):
                if m.channel == ctx.channel and m.author == ctx.author:
                    return m
            msg = await client.wait_for('message', check=check)
            word_attempt = msg.content
            word_attempt = word_attempt.upper()
            attempt_char = list(word_attempt)
            if len(attempt_char) != 5:
                ctx.channel.send("Word is over 5 letters, please try again")
            else:
                break

        #Prepare output record header
        total_attempts = i + 1
        output_record_header = "TOTAL ATTEMPTS: " + str(total_attempts) + "\n"

        #Prepare attempt output header
        attempt_output = "ATTEMPT " + str(i + 1) + ": " + word_attempt + "  "
        
        #Determine accuracy of attempted word, update attempt output
        yellow_chars = [] #includes letters that were in the original word, but in the wrong position
        black_chars = [] #includes letters that weren't in the original word
        green_chars = [] #includes letters that were in the original word and the correct position
        for i in range(len(word_char)):
            print(i)
            if attempt_char[i] != word_char[i]:
                if attempt_char[i] in word_char:
                    yellow_chars.append(attempt_char[i])
                    attempt_output += yellow_emoji_id
                else:
                    black_chars.append(attempt_char[i])
                    attempt_output += black_emoji_id
            else:
                green_chars.append(attempt_char[i])
                attempt_output += green_emoji_id

            #Process duplicates - WIP
            if word_attempt.count(attempt_char[i]) != 1:
                try:
                    word_char[word_char.index(attempt_char[i])] = "SKIP"
                except:
                    continue
                
        #Update output record with new attempt output
        output_record += attempt_output + "\n"

        #Send attempt output and output record
        await ctx.channel.send(attempt_output)
        await asyncio.sleep(2)
        await ctx.channel.send(output_record_header + output_record)

        #If user guesses word correctly
        if len(green_chars) == 5:
            await ctx.channel.send("You guessed the correct word!")
            break

        #If user has run out of tries
        if i == 5:
            await ctx.channel.send("You have run out of tries! Correct word: " + correct_word)
        
                

            
        
    
#RPG DATA MANAGEMENT AND CONFIGURATION (FOR ADMINS ONLY)

#Delete single record
@client.command()
async def delete(ctx, name):
    if ctx.author.guild_permissions.administrator == True:
        cursor.execute("DELETE FROM DATA WHERE USERNAME = ?", (name,))
        await ctx.channel.send("Successfully deleted Record!")

    else:
        await ctx.channel.send("Sorry, you do not have the proper permissions.")

#Initialize Data Tables if not done so already
#Exact copy of on_guild_join()
@client.command()
async def init(ctx):
    #Initalize RPG Table
    i = 1
    for member in ctx.guild.members:
        if member.bot:
            continue
        memberName = member.name
        cursor.execute("INSERT INTO MONEY_DATA VALUES (?, ?, ?);", (i, memberName, 0))
        i += 1
    dataConn.commit()

    #Initalize Army Table
    i = 1
    for member in ctx.guild.members:
        if member.bot:
            continue
        cursor.execute("INSERT INTO ARMY_DATA (ID, USERNAME) VALUES (?, ?)", (i, member.name,))
        i += 1
    dataConn.commit()
    await ctx.channel.send("Initalized Database!")

#OVERALL: Help command for detailed documentation for all commands
#Redirects to a webpage
@client.command()
async def helpme(ctx):
    helpPageUrl = ""
    await ctx.channel.send("Click on this link for help: " + helpPageUrl)
client.run(TOKEN)


