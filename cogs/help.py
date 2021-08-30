import discord
from datetime import datetime
from discord.ext import commands

staffids = [389897179701182465, 221188745414574080, 303901339891531779, 257900648618655746, 193962293342502912, 364045258004365312, 297278578435948545, 368446019035463681]
ccids = [364045258004365312, 167625500498329600, 221188745414574080, 694953679719104544, 164795852785844225, 257900648618655746, 464113463468359690, 496650374741229569, 573854828363776006, 721247603290931200, 482613393803444227, 163608986401243136, 219668296834875403, 675867865701679176, 384584297090252813, 738473939168133211]



class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        await channel.send("hey")

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            await ctx.send(embed=embed)
        else:
            raise error


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

       # Setting the cog for the help
        help_command = MyHelp()
        help_command.cog = self # Instance of YourCog class
        self.client.help_command = help_command

def setup(client):
    client.add_cog(help(client))
