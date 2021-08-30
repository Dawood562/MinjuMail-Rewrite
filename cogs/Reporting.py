import discord
from datetime import datetime
from discord.ext import commands

class Reporting(commands.Cog, name='🗨️ Reporting'):
    """Report bugs, players, and scams!"""
    def __init__(self, client):
        self.client = client


    @commands.command(description='Report a bug or player.')
    async def report(self, ctx):
        await ctx.send('Reporting has begun. From scratch. I hate my life.')

def setup(client):
    client.add_cog(Reporting(client))
