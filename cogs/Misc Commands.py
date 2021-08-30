import discord
from datetime import datetime
from discord.ext import commands
import random
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]

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
        embed = discord.Embed(title='Bot Information', description='No, I do not simp for Kim Dahyun.', color=random.choice(embedcolours))
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/780189371256668210/882035565653004368/dubu.png')
        embed.set_author(name='Bot', icon_url=ctx.author.avatar_url)
        embed.add_field(name='Developer', value='<@221188745414574080>', inline=False)
        embed.add_field(name='Latency', value=f'{round(self.client.latency*1000, 1)}ms', inline=True)

        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime = f'{days}d, {hours}h, {minutes}m, {seconds}s'
        embed.add_field(name='Uptime', value=f'{uptime}', inline=True)

        embed.add_field(name='Members in Minju Support', value=f'{self.client.get_guild(714926445595721820).member_count} players', inline=True)
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Misc_Commands(client))
