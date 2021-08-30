import asyncio
import discord
import os
import json
import random
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import errors
from discord.message import Message
# from discord_slash import SlashCommand
# from discord_slash.utils.manage_commands import create_option, create_choice
from datetime import datetime
# from collections import namedtuple
import traceback
import sys
from lib.functions import *

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(command_prefix = '_', help_command=None, intents=intents, allowed_mentions = discord.AllowedMentions(everyone = False, roles = False), strip_after_prefix=True, case_insensitive=True, activity=discord.Activity(type=discord.ActivityType.listening, name='DMs!'))
# slash = SlashCommand(client, sync_commands=True)
# Wonyoung, Sakura, Yuri, Yena, Yujin, Nako, Eunbi, Hyewon, Hitomi, Chaewon, Minju, Chaeyeon
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]
helplist = [['reportabug', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['snow', 'Who knows?', '`snow`'], ['help', 'Displays the help message with all of the commands!', '`help`, `h`'], ['say', '**DEV-ONLY:** Lets the bot say something in a channel!', '`say`'], ['shutdown', '**DEV-ONLY:** Shuts the bot down.', '`shutdown`, `sd`, `jaljjayo`, `snowwhendubu`, `maliwhensunoo`'], ['ping', "Checks the bot's latency.", '`ping`, `p`'], ['pong', '**DM-ONLY:** Make the bot say "Pong"! Made to test DM-Only commands.', '`pong`'], ['bugreport', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['reportbug', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['rb', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['rab', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`']]
staffids = [389897179701182465, 221188745414574080, 303901339891531779, 257900648618655746, 193962293342502912, 364045258004365312, 297278578435948545, 368446019035463681]
ccids = [364045258004365312, 167625500498329600, 221188745414574080, 694953679719104544, 164795852785844225, 257900648618655746, 464113463468359690, 496650374741229569, 573854828363776006, 721247603290931200, 482613393803444227, 163608986401243136, 219668296834875403, 675867865701679176, 384584297090252813, 738473939168133211]
client.launch_time = datetime.utcnow()

@client.event
async def on_ready():
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bot is ready!')
# --Load cogs--
cogs = ["Accept and Reject", "Admin Commands", "Help", "Misc Commands", "Reporting", "Suggest Cards", "tickets"]

for cog in cogs:
    client.load_extension("cogs." + cog)
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Loaded {cog} cog')
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        try:
            await ctx.send(f'DM me to use commands {ctx.author.mention}!')
            await client.get_user(ctx.author.id).send('Use this channel to send me commands!')
        except discord.HTTPException:
            pass
    elif isinstance(error, commands.CommandOnCooldown):
        try:
            tleft = float(f'{error.retry_after:.2f}')
            minsleft = int(tleft//60)
            sleft = round(tleft%60, 2)
            if minsleft == 0:
                tlstring = f'{sleft} seconds'
            elif minsleft == 1 and sleft == 1:
                tlstring = f'1 minute **and** 1 second'
            elif minsleft == 1:
                tlstring = f'1 minute **and** {sleft} seconds'
            elif sleft == 1:
                tlstring = f'{minsleft} minutes and 1 second'
            else:    
                tlstring = f'{minsleft} minutes **and** {sleft} seconds'
            await ctx.send(f"You're on cooldown for another **{tlstring}** {ctx.author.mention}!")
        except discord.HTTPException:
            pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title=f'Missing Arguments in {ctx.command}', description='If you need help with a command, use `_help`!'))
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# --Start bot--
client_token = os.environ.get("TOKEN")
client.run(client_token)
