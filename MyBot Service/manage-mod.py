#FOR ADMINS ONLY
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

#Activation Indicator
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("Process manage-mod active")
#CHANNEL MANAGEMENT:

#Creates one Text Channel
@client.command()
async def createtext(ctx, name, cat):
    if ctx.author.guild_permissions.administrator == True:
        for category in ctx.guild.categories:
            if category.name == cat:
                await category.create_text_channel(name)
                break
    else:
        await ctx.channel.send("Sorry, you do not have the proper permissions.")

#Creates one VC
@client.command()
async def createvoice(ctx, name, cat):
    if ctx.author.guild_permissions.administrator == True:
        for category in ctx.guild.categories:
            if category.name == cat:
                await category.create_voice_channel(name)
                break
    else:
        await ctx.channel.send("Sorry, you do not have the proper permissions.")

#Creates a whole Channel Category
@client.command()
async def createcat(ctx, name):
    if ctx.author.guild_permissions.administrator == True:
        await ctx.guild.create_category(name)
    else:
        await ctx.channel.send("Sorry, you do not have the proper permissions.")
    
#Deletes a whole Channel Category
@client.command()
async def deletecat(ctx, cat):
    if ctx.author.guild_permissions.administrator == True:
        for category in ctx.guild.categories:
            if category.name == cat:
                for channel in category.channels:
                    await channel.delete()
                await category.delete()
                break
    else:
        await ctx.channel.send("Sorry, you do not have the proper permissions.")

#Deletes one Channel
@client.command()
async def deletechannel(ctx, name):
    if ctx.author.guild_permissions.administrator == True:
        for channel in ctx.guild.channels:
            if channel.name == name:
                await channel.delete()
                break
    else:
        await ctx.channel.send("Sorry, you do not have the proper permissions.")


#ROLE MANAGEMENT:
@client.command()
async def createrole(ctx, roleName):
    if ctx.author.guild_permissions.administrator == True:
        await ctx.guild.create_role(name=roleName)
        await ctx.channel.send("Created role " + roleName)
        
#Delete a role
@client.command()
async def deleterole(ctx, roleName):
    if ctx.author.guild_permissions.administrator == True:
        for role in ctx.guild.roles:
            if role.name == roleName:
                await ctx.channel.send("Deleted role!")
                await role.delete()
#Edit a role
@client.command()
async def editrole(ctx, roleName, **perms):
    if ctx.author.guild_permissions.administrator == True:
        permission = discord.Permissions()
        for role in ctx.guild.roles:
            if role.name == roleName:
                permsList = list(perms)
                for i in range(len(permsList) - 1):
                    permission.update(permsList[i]=permsList[i+1])
                await role.edit(permission)

#PUNISHMENT MANAGEMENT:

#Ban
@client.command()
async def ban(ctx, memberName):
    if ctx.author.guild_permissions.administrator == True:
        for member in ctx.guild.members:
            if member.name == memberName or member.nick == memberName:
                await member.ban()
#Kick
@client.command()
async def kick(ctx, memberName):
    if ctx.author.guild_permissions.administrator == True:
        for member in ctx.guild.members:
            if member.name == memberName or member.nick == memberName:
                await member.kick()



client.run(TOKEN)
