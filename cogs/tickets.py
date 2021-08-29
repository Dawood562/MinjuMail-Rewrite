import discord
from datetime import datetime
from discord.ext import commands

class tickets(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(tickets(client))
