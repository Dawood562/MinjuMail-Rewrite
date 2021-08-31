import discord
import os
from datetime import datetime
from discord.ext import commands
import sqlite3
database = sqlite3.connect('./database/dB.db')
cursor = database.cursor()


class Admin_Commands(commands.Cog, name='👑 Admin Commands'):
    """Admin Commands: Load/unload cogs and shut the bot down."""
    def __init__(self, client):
        self.client = client

    @commands.has_role(737604230759841792)
    @commands.command(description='Loads a specified cog.')
    async def load(self, ctx, module : str):
        if ctx.author.id != 221188745414574080:
            pass
        else:
            try:
                self.client.load_extension(f'cogs.{module}')
            except Exception as e:
                await ctx.send('{}: {}'.format(type(e).__name__, e))
            else:
                await ctx.send('Loaded cog.')

    @commands.has_role(737604230759841792)
    @commands.command(description='Unloads a specified cog.')
    async def unload(self, ctx, module : str):
        if ctx.author.id != 221188745414574080:
            pass
        else:
            try:
                self.client.unload_extension(f'cogs.{module}')
            except Exception as e:
                await ctx.send('{}: {}'.format(type(e).__name__, e))
            else:
                await ctx.send('Unloaded cog.')

    @commands.has_role(737604230759841792)
    @commands.command(aliases=['reload'], description='Reloads a specified cog.')
    async def _reload(self, ctx, module : str):
        if ctx.author.id != 221188745414574080:
            pass
        else:
            try:
                self.client.unload_extension(f'cogs.{module}')
                self.client.load_extension(f'cogs.{module}')
            except Exception as e:
                await ctx.send('{}: {}'.format(type(e).__name__, e))
            else:
                await ctx.send('Successfully reloaded cog.')

    @commands.has_role(737604230759841792)
    @commands.command(aliases=['goodnight', 'jaljjayo', 'sd', 'snowwhendubu', 'maliwhensunoo', 'JaljayoUriKkumsogeseo'], description='Shuts down the bot.')
    async def shutdown(self, ctx):
        if (ctx.message.author.id != 221188745414574080) and (ctx.message.author.id != 303901339891531779):
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: {ctx.message.author} tried to shut the bot down lol')
        else:
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bot has been shut down.')
            await ctx.send('Shutting down...')
            await self.client.close()
            exit()

    @commands.has_role(737604230759841792)
    @commands.command(description='Perform a query. Please don\'t fucking abuse this.')
    async def query(self, ctx, *query: str):
        query = ' '.join(query)
        cursor.execute(query)
        if query[:6].lower() == 'select':
            msg = ''
            result = cursor.fetchall()
            for i in range(len(result)):
                msg += f"{', '.join(result[i])}\n"
            await ctx.reply(msg)
        else:
            database.commit()
            await ctx.reply('Successfully comitted changes.')
def setup(client):
    client.add_cog(Admin_Commands(client))
