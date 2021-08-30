import discord
from datetime import datetime
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
        embed.set_author(name='Bot', icon_url=ctx.author.avatar_url)
        embed.add_field(name='Latency', value=f'{round(self.client.latency*1000, 1)}ms', inline=True)
        embed.add_field(name='Members in Minju Support', value=f'{self.client.get_guild(714926445595721820).member_count}', inline=True)

        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")
        uptime = f'{days}d, {hours}h, {minutes}m, {seconds}s'
        embed.add_field(name='Uptime', value=f'{uptime}', inline=True)

        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Misc_Commands(client))
