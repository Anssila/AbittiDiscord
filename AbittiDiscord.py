import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import has_role
import requests
import json
import os

intents = discord.Intents.default()
intents.members = True

def botconfig(configparam):
    with open('config.json', 'r') as config:
        configjson = json.load(config)

    if configparam == 0:
        return(configjson['BOT_TOKEN'])
    elif configparam == 1:
        return(configjson['ADMINROLE'])
    elif configparam == 2:
        return(configjson['UPDATE_CHANNEL'])
    elif configparam == 3:
        return(configjson['PREFIX'])
    elif configparam == 4:
        return(configjson['UPDATE_FREQUENCY'])

bot = commands.Bot(command_prefix=botconfig(3), case_insensitive=True, intents=intents)

def versioncheck():
    with open('abittiversion.txt', 'r') as readcache:
        getcache = readcache.read()
    messagebuilder = f"```\nThe current version of Abitti is {getcache}\n```"
    return(messagebuilder)

def updater():
    file_exists = os.path.exists('abittiversion.txt')
    if file_exists == False:
        with open('abittiversion.txt', 'w+') as versioncache:
            versioncache.write("")

    url = "https://static.abitti.fi/etcher-usb/koe-etcher.ver"
    r = requests.get(url)

    with open('abittiversion.txt', 'r') as readcache:
        getcache = readcache.read()
    with open('abittiversion.txt', 'w+') as writecache:
        writecache.write(r.text)
    readcache.close()
    writecache.close()

    if getcache != r.text:
        buildmessage = f"```\nThere is a new version of Abitti available!\n\n{getcache} --> {r.text}\n\nClick here to download the new version:\n```https://static.abitti.fi/etcher-usb/koe-etcher.zip" 
        return(buildmessage)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with Abitti versions"))
    autoupdate.start()
    print('Logged in as: ' + bot.user.name)

@bot.command(name="abittiversion", aliases=["av"])
async def getestimate(ctx):
    try:
        checkversion = versioncheck()
        await ctx.send(checkversion)
    except:
        await ctx.send('Error fetching version from cache.')

@tasks.loop(minutes=int(botconfig(4)))
async def autoupdate():
    try:
        channel = bot.get_channel(int(botconfig(2)))
        updateversion = updater()
        print('Autoupdate completed')
        await channel.send(updateversion)
    except:
        pass

bot.run(botconfig(0))