import discord
from datetime import datetime
from discord.ext import commands
import pandas

class tickets(commands.Cog):
    def __init__(self, client):
        self.client = client

#    @commands.Cog.listener()
#    async def on_raw_reaction(self, ctx):
#        if ctx.channel_id == ticket_channel_id:
            # Check if the user has an existing channel
#           existing = False
#           for channel in (get category via id):
#               if channel.name[] == str(ctx.user.id):
#                   existing = True
            # If the user has an existing ticket
#           if existing == True:
#                self.client.get_user(ctx.user.id).send('You already have an existing ticket! Please be patient!')
#           else:
            # Make a channel
            # DM User, ask for a reason to start a ticket
            # Add reactions, ask for confirmation
            # Create a channel only staff + user can see under the Ticket category
            # Send embed in new channel
            # Add a reaction X
            # If a staff reacts to it, ask why. Lock main user out of channel
            # DMs the original user with "Your ticket was closed. Reason:"
            # Creates a log of channel if more than 5 messages.
#        else:
#            pass
        
    

#   https://levelup.gitconnected.com/how-to-gather-message-data-using-a-discord-bot-from-scratch-with-python-2fe239da3bcd
#    @commands.command()
#    async def log(self, ctx):
#        data = pd.DataFrame(columns=['content', 'time', 'author'])

#       async for msg in ctx.message.channel.history(limit=1000):
#           if msg.author != client.user:
#               data = data.append({'content': msg.content,
#                                'time': msg.created_at,
#                                'author': msg.author.name}, ignore_index=True)
#           if len(data) == limit:
#               break
#    
#       file_location = "data.csv" # Set the string to where you want the file to be saved to
#       data.to_csv(file_location)


def setup(client):
    client.add_cog(tickets(client))
