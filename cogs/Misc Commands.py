import discord
from discord.ext import commands

class Misc_Commands(commands.Cog, name='❓ Miscellaneous Commands'):
    """Miscellaneous commands."""
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'**Latency:** {round(self.client.latency*1000, 1)}ms')

    @commands.command()
    async def snow(self, ctx):
        await ctx.send(f'This bot was coded by Snow (**DaSnow562#0562**). If it breaks, get a Minju\'s Manager to reach out to him to fix it!')

def setup(client):
    client.add_cog(Misc_Commands(client))
