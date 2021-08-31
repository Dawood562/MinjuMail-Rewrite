import discord
from datetime import datetime
from discord.ext import commands
import random
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]

import sqlite3
database = sqlite3.connect('./database/dB.db')
cursor = database.cursor()

class Suggest_Cards(commands.Cog, name='🗨️ Suggest Cards'):
    """Suggest cards to be added to the Minju bot!"""
    def __init__(self, client):
        self.client = client

        
    @commands.group(invoke_without_command=True, aliases=['s'], description='Suggest cards to be added to the Minju bot! All subcommands have a 2 minute cooldown.', case_insensitive=True)
    @discord.ext.commands.dm_only()
    async def suggest(self, ctx):
        await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Suggestion', description='Missing arguments. Please use one of `group`, `drama`, or `soloist`.'))
    
    @suggest.group(aliases=['groups', 'g'], description='Suggest a group for the bot.')
    @discord.ext.commands.dm_only()
    @commands.cooldown(1,120,commands.BucketType.user)
    async def group(self, ctx):
        AArtist = ""
        AGender = ""
        while (AArtist != "cancel") and (AGender != "cancel"):
            await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Thanks for wanting to suggest an artist!', description='Please remember that this should only be used if the artist is not already in the game or in the <#737721977816743966> channel!\nIf at any time you wish to cancel (e.g. if the bog bugs and 2 embeds are sent), type `cancel`!'))
            QGroup = discord.Embed(color=random.choice(embedcolours), title="Group Name (Without special characters):")
            await ctx.send(embed=QGroup)
            MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            AArtist = (MessageReply.content)
            # Check to cancel
            if AArtist.lower() == "cancel":
                await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title="Group Suggestion", description="Suggestion process has been cancelled."))
                break
            else:
                cursor.execute(f"SELECT * FROM Cards WHERE UPPER(aname)='{AArtist.upper()}';")
                result = cursor.fetchone()
                if result:
                    print('Suggested existing.')
                    await MessageReply.reply(f'{AArtist} has already been suggested.')
                    break
                else:
                    print('Is fine')
                    pass
            ##################
            QGender = discord.Embed(color=random.choice(embedcolours), title='Group Gender (Male, Female, or Mixed):')
            await ctx.send(embed=QGender)
            while (AGender != "female") or (AGender != "male") or (AGender != "mixed"):
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

            if AGender.lower() == "cancel":
                break

            ECheck = discord.Embed(title="Card Suggestion", description="Please check the contents below to make sure everything is typed properly!", color=random.choice(embedcolours))
            ECheck.add_field(name="**Artist Name:**", value=f"{AArtist}", inline=False)
            ECheck.add_field(name="**Artist Gender:**", value=f"{AGender}", inline=False)
            ECheck.add_field(name="**Artist Type:**", value="Group", inline=False)
            ECheck.set_footer(text=f'{ctx.author} ({ctx.author.id})')
            DMEmbed = await ctx.send(embed=ECheck)
            await DMEmbed.add_reaction('❌')
            await DMEmbed.add_reaction('✅')
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Adds both reactions')
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author,  timeout = 60.0)
            except asyncio.TimeoutError:
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: A card suggestion by {ctx.message.author} timed out.')
                return await ctx.send('Validation timed out. Please try again.')
            else:
                if reaction.emoji == '✅':
                    await ctx.send("Thanks for the suggestion! It's been sent to the Minju Managers to verify the information!")
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)

                    ECheck.set_footer(text=f'Suggested by {ctx.author} ({ctx.author.id})')
                    ECheck.set_author(name=f'{ctx.message.channel.id}/{DMEmbed.id}')
                    CHECKEmbed = await self.client.get_channel(861687628881199104).send(f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).", embed=ECheck)
                    await CHECKEmbed.edit(content=f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).\nUse `_accept {CHECKEmbed.id}` or `_reject {CHECKEmbed.id}` to accept or reject this card suggestion.\nAlso remember that they can't submit special characters so don't reject for that!", embed=ECheck)
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been sent to the checking channel.')
                    break
                elif reaction.emoji == '❌':
                    # Remove all reactions
                    CLDEmbed = discord.Embed(title='Card suggestion has been cancelled.', description='Please reuse the command to redo your entries!', color=random.choice(embedcolours))
                    await DMEmbed.edit(embed=CLDEmbed)
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been cancelled.')
                    break
                else:
                    return await ctx.send(f'You reacted with {reaction}... start again.')
                    break
    
    
    @suggest.group(aliases=['solo', 's'], description='Suggest a soloist for the bot.')
    @discord.ext.commands.dm_only()
    @commands.cooldown(1,120,commands.BucketType.user)
    async def soloist(self, ctx):
        AArtist = ""
        AGender = ""
        while (AArtist != "cancel") and (AGender != "cancel"):
            await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Thanks for wanting to suggest an artist!', description='Please remember that this should only be used if the soloist is not already in the game or in the <#737721977816743966> channel!\nIf at any time you wish to cancel (e.g. if the bog bugs and 2 embeds are sent), type `cancel`!   '))
            QGroup = discord.Embed(color=random.choice(embedcolours), title="Soloist Name (Without special characters):")
            await ctx.send(embed=QGroup)
            MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            AArtist = (MessageReply.content)
            # Check to cancel
            if AArtist.lower() == "cancel":
                await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title="Group Suggestion", description="Suggestion process has been cancelled."))
                break
            else:
                pass
            ##################
            QGender = discord.Embed(color=random.choice(embedcolours), title='Soloist Gender (Male or Female):')
            await ctx.send(embed=QGender)
            MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            AGender = (MessageReply.content)
            # Check to cancel
            if AGender.lower() == "cancel":
                await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title="Soloist Suggestion", description="Suggestion process has been cancelled."))
                break
            else:
                AGender = AGender.capitalize()
                pass

            ECheck = discord.Embed(title="Card Suggestion", description="Please check the contents below to make sure everything is typed properly!", color=random.choice(embedcolours))
            ECheck.add_field(name="**Artist Name:**", value=f"{AArtist}", inline=False)
            ECheck.add_field(name="**Artist Gender:**", value=f"{AGender}", inline=False)
            ECheck.add_field(name="**Artist Type:**", value="Soloist", inline=False)
            ECheck.set_footer(text=f'{ctx.author} ({ctx.author.id})')
            DMEmbed = await ctx.send(embed=ECheck)
            await DMEmbed.add_reaction('❌')
            await DMEmbed.add_reaction('✅')
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Adds both reactions')
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author,  timeout = 60.0)
            except asyncio.TimeoutError:
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: A card suggestion by {ctx.message.author} timed out.')
                return await ctx.send('Validation timed out. Please try again.')
            else:
                if reaction.emoji == '✅':
                    await ctx.send("Thanks for the suggestion! It's been sent to the Minju Managers to verify the information!")
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)

                    ECheck.set_footer(text=f'Suggested by {ctx.author} ({ctx.author.id})')
                    ECheck.set_author(name=f'{ctx.message.channel.id}/{DMEmbed.id}')
                    CHECKEmbed = await self.client.get_channel(861687628881199104).send(f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).", embed=ECheck)
                    await CHECKEmbed.edit(content=f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).\nUse `_accept {CHECKEmbed.id}` or `_reject {CHECKEmbed.id}` to accept or reject this card suggestion.\nAlso remember that they can't submit special characters so don't reject for that!", embed=ECheck)
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been sent to the checking channel.')
                    break
                elif reaction.emoji == '❌':
                    # Remove all reactions
                    CLDEmbed = discord.Embed(title='Card suggestion has been cancelled.', description='Please reuse the command to redo your entries!', color=random.choice(embedcolours))
                    await DMEmbed.edit(embed=CLDEmbed)
                    await DMEmbed.remove_reaction('❌', self.client.user)
                    await DMEmbed.remove_reaction('✅', self.client.user)
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been cancelled.')
                    break
                else:
                    return await ctx.send(f'You reacted with {reaction}... start again.')
                    break
        
    @suggest.group(aliases=['kdrama', 'k-drama', 'd', 'k'], description='Suggest a k-drama for the bot.')
    @discord.ext.commands.dm_only()
    @commands.cooldown(1,120,commands.BucketType.user)
    async def drama(self, ctx):
        await ctx.send('Suggest drama yes? Drama name?')
        # sex

def setup(client):
    client.add_cog(Suggest_Cards(client))
