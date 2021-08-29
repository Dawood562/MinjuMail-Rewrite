import discord
from datetime import datetime
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.group(aliases=['h'], invoke_without_command=True)
    async def help(self, ctx, *helptype):
        cord.Embed(color=random.choice(embedcolours), title='Help'))
        HelpEmbed = discord.Embed(color=random.choice(embedcolours), title='Help'))


def setup(client):
    client.add_cog(help(client))
