import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import has_role
import requests
import json
import os
import qrcode

intents = discord.Intents.default()
intents.members = True

def botconfig(configparam):
    with open('config.json', 'r') as config:
        configjson = json.load(config)

    configparams = ['BOT_TOKEN', 'ADMINROLE', 'UPDATE_CHANNEL', 'PREFIX', 'UPDATE_FREQUENCY']
    return configjson[configparams[configparam]]


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
        getcache = readcache.readline().strip()
    with open('abittiversion.txt', 'w+') as writecache:
        writecache.write((r.text).strip())
   

    if getcache != (r.text).strip():
        buildmessage = f"```\nThere is a new version of Abitti available!\n\n{getcache} --> {r.text}\n\nClick here to download the new version:\n```https://static.abitti.fi/etcher-usb/koe-etcher.zip" 
        return(buildmessage, 1)
    else:
        return("No new version available.", 2)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with Abitti versions"))
    autoupdate.start()
    print('Logged in as: ' + bot.user.name)

@bot.command(name="abittiversion", aliases=["av"])
async def versionchecker(ctx):
    try:
        checkversion = versioncheck()
        await ctx.send(checkversion)
    except:
        await ctx.send('Error fetching version from cache.')

@bot.command(name="qr")
async def getqr(ctx, *, var):
    try:
        image = qrcode.make(var)
        image.save("qrcode.png")
        await ctx.send(file=discord.File("qrcode.png"))
    except:
        await ctx.send('Unable to create image.')

@bot.command(name="update", aliases=["u"])
@commands.has_role(botconfig(1))
async def updateversion(ctx):
    try:
        checkversion = updater()
        await ctx.send(checkversion[0])
    except:
        await ctx.send('Error updating.')


@tasks.loop(minutes=int(botconfig(4)))
async def autoupdate():
    channel = bot.get_channel(int(botconfig(2)))
    updateversion = updater()
    if updateversion[1] == 1:
        await channel.send(updateversion[0])
    elif updateversion[1] == 2:
        print(updateversion[0])

bot.run(botconfig(0))
