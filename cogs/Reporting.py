import discord
from datetime import datetime
from discord.ext import commands

class Reporting(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Reporting(client))
