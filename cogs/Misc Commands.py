import discord
from discord.ext import commands

class Misc_Commands(commands.Cog, name='❓ Miscellaneous Commands'):
    """Miscellaneous commands."""
    def __init__(self, client):
        self.client = client

    @commands.command(description='Check the latency of the bot.')
    async def ping(self, ctx):
        await ctx.send(f'**Latency:** {round(self.client.latency*1000, 1)}ms')

    @commands.command(description='Snow.')
    async def snow(self, ctx):
        await ctx.send(f'This bot was coded by Snow (**DaSnow562#0562**). If it breaks, get a Minju\'s Manager to reach out to him to fix it!')


    @commands.command(description='Bot information.')
    async def bot(self, ctx):
        embed = discord.Embed(title='Bot Information')
        embed.set_author(name='Bot', icon_url=self.context.author.avatar_url)
        embed.add_field(name='Latency', value=f'{round(self.client.latency*1000, 1)}ms', inline=True)
        embed.add_field(name='Members in Minju Support', value=f'{client.get_guild(714926445595721820).member_count}', inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Misc_Commands(client))
