# LukioBot
A simple Discord bot with some studying tools. New features might be added later on. If you have good ideas, feel free to do a PR.

**Dependencies:**

To run the bot, you need to install [Discord.py](https://pypi.org/project/discord.py/), [Requests](https://pypi.org/project/requests/) and [Qrcode](https://pypi.org/project/qrcode/)

**Starting the bot:**

To get the bot running, create a file called config.json that looks like this:

```
{
    "BOT_TOKEN": "Place bot token here",    
    "ADMINROLE": "Admin role name",
    "UPDATE_CHANNEL": "Channel ID for Abitti version notifications",
    "PREFIX": "Character to start the commands with",
    "UPDATE_FREQUENCY": 60
}
```
The update frequency should be given in minutes.
After the bot is up and running, the bot should create all of the files it needs automatically. 


# Commands:

**abittiversion or av**: 
Get the current version of Abitti.

**qr**: 
Make a QR code from inputted text or URLs.

**update or u**: 
Manual update method for version changes.(Only for admins)
