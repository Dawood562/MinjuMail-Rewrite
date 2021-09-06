import discord
from datetime import datetime
from discord.ext import commands

class tickets(commands.Cog):
    def __init__(self, client):
        self.client = client

#    @commands.Cog.listener()
#    async def on_raw_reaction(self, ctx):
#        if ctx.channel_id == ticket_channel_id:
            # Check if user has an existing channel (using user ID)
            # If they have, DM them with "no"
            # Else
            # DM User, ask for a reason to start a ticket
            # Add reactions, ask for confirmation
            # Create a channel only staff + user can see under the Ticket category
            # Send embed in new channel
            # Add a reaction X
            # If a staff reacts to it, ask why. Lock main user out of channel
            # DMs the original user with "Your ticket was closed. Reason:"
            # Creates a log of channel if more than 5 messages.
        else:
            pass
        
def setup(client):
    client.add_cog(tickets(client))
