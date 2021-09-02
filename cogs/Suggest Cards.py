#Import libraries
import discord
from datetime import datetime
from discord.ext import commands
import random
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]

import sqlite3
database = sqlite3.connect('./database/dB.db')
cursor = database.cursor()

# Create class for this cog
class Suggest_Cards(commands.Cog, name='🗨️ Suggest Cards'):
    """Suggest cards to be added to the Minju bot!"""
    # ^ Docstring
    def __init__(self, client):
        self.client = client

    # Create a group of commands under the name `suggest`. This part won't be summoned unless someone does only "_suggest", hence the "invoke_without_command=True"
    @commands.group(invoke_without_command=True, aliases=['s'], description='Suggest cards to be added to the Minju bot! All subcommands have a 2 minute cooldown.', case_insensitive=True)
    @discord.ext.commands.dm_only()
    async def suggest(self, ctx):
        await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Suggestion', description='Missing arguments. Please use one of `group`, `drama`, or `soloist`.'))

    # Create a subcommand called 'group' that can only be used in DMs and has a 2 minute cooldown
    @suggest.group(aliases=['groups', 'g'], description='Suggest a group for the bot.')
    @discord.ext.commands.dm_only()
    @commands.cooldown(1,120,commands.BucketType.user)
    async def group(self, ctx):
        # Define variables for while loop
        AArtist = ""
        AGender = ""
        while (AArtist != "cancel") and (AGender != "cancel"):
            # Send two embeds
            await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Thanks for wanting to suggest a group!', description='Please remember that this should only be used if the artist is not already in the game or in the <#737721977816743966> channel!\nIf at any time you wish to cancel (e.g. if the bog bugs and 2 embeds are sent), type `cancel`!'))
            QGroup = discord.Embed(color=random.choice(embedcolours), title="Group Name (Without special characters):")
            await ctx.send(embed=QGroup)
            # Waits for user's reply
            MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            # Sets AArtist to be the contents of the message reply
            AArtist = (MessageReply.content)
            # Checks if the user wishes to cancel
            if AArtist.lower() == "cancel":
                # Send a cancellation message
                await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title="Group Suggestion", description="Suggestion process has been cancelled."))
                # Exit while loop, finish command
                break
            else:
                # Check if the group has already been suggested
                cursor.execute(f"SELECT * FROM Cards WHERE UPPER(aname)='{AArtist.upper()}';")
                result = cursor.fetchone()
                if result:
                    # If a value is returned
                    await MessageReply.reply(f'{AArtist} has already been suggested.')
                    # Exit while loop, finish command.
                    break
                else:
                    print('Is fine')
                    pass
            ##################
            # Asks for the group's gender
            QGender = discord.Embed(color=random.choice(embedcolours), title='Group Gender (Male, Female, or Mixed):')
            await ctx.send(embed=QGender)
            # If not one of the valid answers
            while (AGender.lower() != "female") or (AGender.lower() != "male") or (AGender.lower() != "mixed"):
                # Waits for response
                MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
                AGender = (MessageReply.content)
                # Making sure the answer is valid
                if AGender.lower() == "cancel":
                    await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title="Group Suggestion", description="Suggestion process has been cancelled."))
                    break
                elif (AGender.lower() == "female") or (AGender.lower() == "male") or (AGender.lower() == "mixed"):
                    AGender = AGender.capitalize()
                else:
                    await ctx.send("That's not a valid input! Try again.")
                    # Go back to the beginning of the while loop

            # The previous "break" would have exited that while loop, not both
            if AGender.lower() == "cancel":
                break

            # Generate embed to be sent to the user to verify their information
            ECheck = discord.Embed(title="Card Suggestion", description="Please check the contents below to make sure everything is typed properly!", color=random.choice(embedcolours))
            ECheck.add_field(name="**Artist Name:**", value=f"{AArtist}", inline=False)
            ECheck.add_field(name="**Artist Gender:**", value=f"{AGender}", inline=False)
            ECheck.add_field(name="**Artist Type:**", value="Group", inline=False)
            ECheck.set_footer(text=f'{ctx.author} ({ctx.author.id})')
            DMEmbed = await ctx.send(embed=ECheck)
            # Add reactions for them to confirm the information is correct
            await DMEmbed.add_reaction('❌')
            await DMEmbed.add_reaction('✅')
            # Attempt to wait for a reaction
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author,  timeout = 60.0)
            # If it times out
            except asyncio.TimeoutError:
                return await ctx.send('Validation timed out. Please try again.')
            else:
                # If they said the information was correct
                if reaction.emoji == '✅':
                    await ctx.send("Thanks for the suggestion! It's been sent to the Minju Managers to verify the information!")
                    # Remove reactions as they are no longer needed
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)

                    # Generate embed to be sent to checking channel
                    ECheck.set_footer(text=f'Suggested by {ctx.author} ({ctx.author.id})')
                    # Set the author name to the message link for the embed with the information in the user's DMs, so on acceptance/rejection they can be DMd with information about which suggestion was approved/denied.
                    ECheck.set_author(name=f'{ctx.message.channel.id}/{DMEmbed.id}')
                    CHECKEmbed = await self.client.get_channel(861687628881199104).send(f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).", embed=ECheck)
                    # Adds in the commands to accept/reject so that staff can copy/paste on PC.
                    await CHECKEmbed.edit(content=f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).\nUse `_accept {CHECKEmbed.id}` or `_reject {CHECKEmbed.id}` to accept or reject this card suggestion.\nAlso remember that they can't submit special characters so don't reject for that!", embed=ECheck)
                    # Logging
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been sent to the checking channel.')
                    break
                # If the information was incorrect
                elif reaction.emoji == '❌':
                    # Remove all reactions
                    CLDEmbed = discord.Embed(title='Card suggestion has been cancelled.', description='Please reuse the command to redo your entries!', color=random.choice(embedcolours))
                    await DMEmbed.edit(embed=CLDEmbed)
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been cancelled.')
                    break
                # If they reacted with something else
                else:
                    return await ctx.send(f'You reacted with {reaction}... start again.')
                    break
    
    # Create a subcommand called 'soloist' that can only be used in DMs and has a 2 minute cooldown
    @suggest.group(aliases=['solo', 's'], description='Suggest a soloist for the bot.')
    @discord.ext.commands.dm_only()
    @commands.cooldown(1,120,commands.BucketType.user)
    async def soloist(self, ctx):
        AArtist = ""
        AGender = ""
        # Whilst the user hasn't tried to cancel the command
        while (AArtist != "cancel") and (AGender != "cancel"):
            await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Thanks for wanting to suggest a soloist!', description='Please remember that this should only be used if the soloist is not already in the game or in the <#737721977816743966> channel!\nIf at any time you wish to cancel (e.g. if the bog bugs and 2 embeds are sent), type `cancel`!   '))
            QGroup = discord.Embed(color=random.choice(embedcolours), title="Soloist Name (Without special characters):")
            await ctx.send(embed=QGroup)
            # Wait for user's response
            MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            AArtist = (MessageReply.content)
            # Check if the user wants to cancel
            if AArtist.lower() == "cancel":
                await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title="Soloist Suggestion", description="Suggestion process has been cancelled."))
                break
            else:
                # Check if the artist has already been suggested before
                cursor.execute(f"SELECT * FROM Cards WHERE UPPER(aname)='{AArtist.upper()}';")
                result = cursor.fetchone()
                if result:
                    # If something is returned
                    await MessageReply.reply(f'{AArtist} has already been suggested.')
                    break
                else:
                    pass
            ##################
            # Get soloist's gender
            QGender = discord.Embed(color=random.choice(embedcolours), title='Soloist Gender (Male/Female):')
            await ctx.send(embed=QGender)
            while (AGender.lower() != "female") or (AGender.lower() != "male"):
                MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
                AGender = (MessageReply.content)
                # Making sure the answer is valid
                if AGender.lower() == "cancel":
                    await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title="Soloist Suggestion", description="Suggestion process has been cancelled."))
                    break
                elif (AGender.lower() == "female") or (AGender.lower() == "male"):
                    AGender = AGender.capitalize()
                else:
                    await ctx.send("That's not a valid input! Try again.")
                    # Return to the beginning of the while loop

            # Cancels if they wanted to
            if AGender.lower() == "cancel":
                break

            # Generate embed for the user to verify that the information is correct
            ECheck = discord.Embed(title="Card Suggestion", description="Please check the contents below to make sure everything is typed properly!", color=random.choice(embedcolours))
            ECheck.add_field(name="**Artist Name:**", value=f"{AArtist}", inline=False)
            ECheck.add_field(name="**Artist Gender:**", value=f"{AGender}", inline=False)
            ECheck.add_field(name="**Artist Type:**", value="Soloist", inline=False)
            ECheck.set_footer(text=f'{ctx.author} ({ctx.author.id})')
            DMEmbed = await ctx.send(embed=ECheck)
            # Add reactions
            await DMEmbed.add_reaction('❌')
            await DMEmbed.add_reaction('✅')
            # Wait for response
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author,  timeout = 60.0)
            # If it times out
            except asyncio.TimeoutError:
                return await ctx.send('Validation timed out. Please try again.')
            else:
                #If they reacted with yes
                if reaction.emoji == '✅':
                    await ctx.send("Thanks for the suggestion! It's been sent to the Minju Managers to verify the information!")
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)

                    ECheck.set_footer(text=f'Suggested by {ctx.author} ({ctx.author.id})')
                    ECheck.set_author(name=f'{ctx.message.channel.id}/{DMEmbed.id}')
                    CHECKEmbed = await self.client.get_channel(861687628881199104).send(f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).", embed=ECheck)
                    await CHECKEmbed.edit(content=f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).\nUse `_accept {CHECKEmbed.id}` or `_reject {CHECKEmbed.id}` to accept or reject this card suggestion.\nAlso remember that they can't submit special characters so don't reject for that!", embed=ECheck)
                    # Logging
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been sent to the checking channel.')
                    break
                # If they reacted with no
                elif reaction.emoji == '❌':
                    # Remove all reactions
                    CLDEmbed = discord.Embed(title='Card suggestion has been cancelled.', description='Please reuse the command to redo your entries!', color=random.choice(embedcolours))
                    await DMEmbed.edit(embed=CLDEmbed)
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been cancelled.')
                    break
                # If they reacted with something else
                else:
                    return await ctx.send(f'You reacted with {reaction}... start again.')
                    break

    # Create a subcommand called 'kdrama' that can only be used in DMs and has a 2 minute cooldown
    @suggest.group(aliases=['k-drama', 'drama', 'd', 'k', 'movie', 'm'], description='Suggest a k-drama/movie for the bot.')
    @discord.ext.commands.dm_only()
    @commands.cooldown(1,120,commands.BucketType.user)
    async def kdrama(self, ctx):
        AArtist = ""
        while AArtist != "cancel":
            await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Thanks for wanting to suggest a K-Drama!', description='Please remember that this should only be used if the K-Drama is not already in the game or in the <#737721977816743966> channel!\nIf at any time you wish to cancel (e.g. if the bog bugs and 2 embeds are sent), type `cancel`!'))
            QGroup = discord.Embed(color=random.choice(embedcolours), title="K-Drama/Movie Name (Without special characters):")
            await ctx.send(embed=QGroup)
            MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            AArtist = (MessageReply.content)
            # Check to cancel
            if AArtist.lower() == "cancel":
                await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title="K-Drama/Movie Suggestion", description="Suggestion process has been cancelled."))
                break
            else:
                cursor.execute(f"SELECT * FROM Cards WHERE UPPER(aname)='{AArtist.upper()}';")
                result = cursor.fetchone()
                if result:
                    await MessageReply.reply(f'{AArtist} has already been suggested.')
                    break
                else:
                    pass
                                               

            ECheck = discord.Embed(title="K-Drama/Movie Suggestion", description="Please check the contents below to make sure everything is typed properly!", color=random.choice(embedcolours))
            ECheck.add_field(name="**Name:**", value=f"{AArtist}", inline=False)
            ECheck.add_field(name="**Type:**", value="K-Drama/Movie", inline=False)
            ECheck.set_footer(text=f'{ctx.author} ({ctx.author.id})')
            DMEmbed = await ctx.send(embed=ECheck)
            await DMEmbed.add_reaction('❌')
            await DMEmbed.add_reaction('✅')
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author,  timeout = 60.0)
            # If they don't respond in time
            except asyncio.TimeoutError:
                return await ctx.send('Validation timed out. Please try again.')
            else:
                # If they confirmed the information was correct
                if reaction.emoji == '✅':
                    await ctx.send("Thanks for the suggestion! It's been sent to the Minju Managers to verify the information!")
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)
                    ECheck.set_footer(text=f'Suggested by {ctx.author} ({ctx.author.id})')
                    ECheck.set_author(name=f'{ctx.message.channel.id}/{DMEmbed.id}')
                    CHECKEmbed = await self.client.get_channel(861687628881199104).send(f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).", embed=ECheck)
                    await CHECKEmbed.edit(content=f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).\nUse `_accept {CHECKEmbed.id}` or `_reject {CHECKEmbed.id}` to accept or reject this card suggestion.\nAlso remember that they can't submit special characters so don't reject for that!", embed=ECheck)
                    # Logging
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been sent to the checking channel.')
                    break
                # If they reacted with no
                elif reaction.emoji == '❌':
                    # Remove all reactions
                    CLDEmbed = discord.Embed(title='Card suggestion has been cancelled.', description='Please reuse the command to redo your entries!', color=random.choice(embedcolours))
                    await DMEmbed.edit(embed=CLDEmbed)
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)
                    break
                # If they reacted with something else
                else:
                    return await ctx.send(f'You reacted with {reaction}... start again.')
                    break

# Setup the cog; called when bot is starting
def setup(client):
    client.add_cog(Suggest_Cards(client))
