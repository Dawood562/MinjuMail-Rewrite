# Import required libraries
import discord
from datetime import datetime
from discord.ext import commands
import random

# Set variables to be used throughout the bot's life
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]
staffids = [389897179701182465, 221188745414574080, 303901339891531779, 257900648618655746, 193962293342502912, 364045258004365312, 297278578435948545]

# Create the cog
class Accept_and_Reject(commands.Cog, name='👑 Accept and Reject'):
    """Admin Commands: Accept and reject bug reports and card suggestions."""
    # ^ A docstring. It's the first line under a class, as a string, and can be accessed by class_name.__doc__
    def __init__(self, client):
        self.client = client

    # User requires 'Staff' role
    @commands.has_role(750430586560053359)
    @commands.command(description='Accept a bug report/card suggestion.')
    async def accept(self, ctx, msgid: int):
        # Retrieves specified message
        asd = await self.client.get_channel(861687628881199104).fetch_message(msgid)
        try:
            # Tries to retrieve the embed
            asdembeds = asd.embeds[0].title
        except IndexError:
            # If there is no embed:
            await ctx.send(embed=discord.Embed(title='Error in Accept Command', description=f'Please use a correct message ID!', color=random.choice(embedcolours)))
        except AttributeError:
            # If there is no embed/it has no title:
            await ctx.send(embed=discord.Embed(title='Error in Accept Command', description=f'Please use a correct message ID!', color=random.choice(embedcolours)))
        except:
            # Unexpected error
            await ctx.send(embed=discord.Embed(title='Error in Accept Command', description=f'An unexpected error occured.', color=random.choice(embedcolours)))
        else:
            # Checks if user is accepting a bug report or a card suggestion
            if asd.embeds[0].title == 'Bug Report':
                # Gets field values
                efields = asd.embeds[0].fields
                eauth = asd.embeds[0].author.name
                efooter = asd.embeds[0].footer.text
                steps = efields[0].value
                expected = efields[1].value
                actual = efields[2].value
                reporterid = int(efooter[efooter.find('(', 17, len(efooter))+1:-1])
                # Generates embed to be sent to known-bugs channel
                KEmbed = discord.Embed(title='Bug Report', description="React with ⬆️ if you've experienced this bug, and ⬇️ if you haven't!", color=random.choice(embedcolours))
                KEmbed.add_field(name="**Steps to Reproduce:**", value=f"{steps}", inline=False)
                KEmbed.add_field(name="**Expected result:**", value=f"{expected}", inline=False)
                KEmbed.add_field(name="**Actual result:**", value=f"{actual}", inline=False)
                # Checks if image given was a link or a file
                if len(efields) == 4:
                    KEmbed.add_field(name="**Image Link:**", value=f"{efields[3].value}", inline=False)
                    KEmbed.set_image(url=f'{efields[3].value}')
                KEmbed.set_footer(text=f'{efooter}')
                # Sends embed
                KNOWNEmbed = await client.get_channel(749732893743513629).send(embed=KEmbed)
                # Adds reactions
                await KNOWNEmbed.add_reaction('⬆️')
                await KNOWNEmbed.add_reaction('⬇️')
                # Sends confirmation of bug being accepted
                await ctx.send(embed=discord.Embed(title='Bug Report Accepted', description=f'Bug report [here](https://discord.com/channels/774031288318296085/861687628881199104/{msgid}) has been approved by **{ctx.author}**, and <@{reporterid}> has been DMd.', color=random.choice(embedcolours)))
                # Tells reporter their bug report was accepted.
                await self.client.get_user(reporterid).send(embed=discord.Embed(title='Bug Report Accepted', description=f'[Your bug](https://discord.com/channels/@me/{eauth}) has been approved by **{ctx.author}** and sent to <#749732893743513629>.', color=random.choice(embedcolours)))
            # If it's a card suggestion
            elif asd.embeds[0].title == 'Card Suggestion':
                # Gets field values
                efields = asd.embeds[0].fields
                eauth = asd.embeds[0].author.name
                efooter = asd.embeds[0].footer.text
                artist = efields[0].value
                gender = efields[1].value
                atype = efields[2].value
                # Generates embed to be sent to suggest-cards
                VEmbed = discord.Embed(title='Card Suggestion', description='React with ⬆️ if you would like to see this artist in the game!')
                VEmbed.add_field(name="**Artist Name:**", value=f"{artist}", inline=False)
                VEmbed.add_field(name="**Artist Gender:**", value=f"{gender}", inline=False)
                VEmbed.add_field(name="**Artist Type:**", value=f"{atype}", inline=False)
                VEmbed.set_footer(text=f'{efooter}')
                # Sends embed
                SUGGESTEmbed = await self.client.get_channel(737721977816743966).send(embed=VEmbed)
                # Adds reaction
                await SUGGESTEmbed.add_reaction('⬆️')
                # Sends confirmation of suggestion being accepted
                await ctx.send(embed=discord.Embed(title='Card Suggestion Accepted', description=f'Card suggestion [here](https://discord.com/channels/774031288318296085/861687628881199104/{msgid}) has been approved by **{ctx.author}**.', color=random.choice(embedcolours)))
                # Tells suggester their suggestion was accepted.
                await self.client.get_user(reporterid).send(embed=discord.Embed(title='Card Suggestion Accepted', description=f'[Your bug](https://discord.com/channels/@me/{eauth}) has been approved by **{ctx.author}** and sent to <#737721977816743966>.', color=random.choice(embedcolours)))
            # If the embed title is something else, i.e. wrong embed;
            else:
                await ctx.send(embed=discord.Embed(title='Error in Accept Command', description=f'Please use a correct message ID!', color=random.choice(embedcolours)))


    # User requires 'Staff' role
    @commands.has_role(750430586560053359)
    @commands.command(aliases=['deny'], description='Reject a bug report/card suggestion.')
    async def reject(self, ctx, msgid: int):
        asd = await self.client.get_channel(861687628881199104).fetch_message(msgid)
        try:
            # Gets embed values
            eauth = asd.embeds[0].author.name
            efooter = asd.embeds[0].footer.text
            reporterid = int(efooter[efooter.find('(', 17, len(efooter))+1:-1])
        # Error handling for wrong embed
        except IndexError:
            await ctx.send(embed=discord.Embed(title='Error in Reject Command', description=f'Please use a correct message ID!', color=random.choice(embedcolours)))
        except AttributeError:
            await ctx.send(embed=discord.Embed(title='Error in Reject Command', description=f'Please use a correct message ID!', color=random.choice(embedcolours)))
        except:
            await ctx.send(embed=discord.Embed(title='Error in Reject Command', description=f'An unexpected error occured.', color=random.choice(embedcolours)))
        else:
            # Get a reason for rejection (triple quotes allows for multi-line strings)
            rejectreason = await self.client.get_channel(861687628881199104).send(embed=discord.Embed(title='Why are you rejecting this?', 
                                                        description='''Below are a list of keywords you can use:\n
                                                        __Bugs:__
                                                        **known <link>** - Sends a message saying that the bug is known and has been reported at `link`.
                                                        **card** - Informs the user that it's a card bug and so isn't accepted
                                                        **fixed** - Informs the user that by the time they reported the bug and we've seen it, it's already been fixed.
                                                        __Cards:__
                                                        **suggested** - Sends a message saying that the artist has already been suggested.
                                                        **info** - Sends a message saying that their suggestion contains incorrect information.
                                                        **troll** - Doesn't send a response because they're trolling with the submission.
                                                        **blank** - Doesn't send a response.
                                                        ''', color=random.choice(embedcolours)))
            # Waits for a response
            MessageReply = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            # Check which reason was given
            reason = (MessageReply.content)
            if reason[:5].lower() == 'known': 
                reason = f'This bug is already known! Please upvote it [here]({reason[6:]}).'
            elif reason.lower() == 'card':
                reason = 'This is a card error which is not reported as a bug. Please check the channel for information on what to report and what not to report!'
            elif reason.lower() == 'fixed':
                reason = 'Thanks for the report, but by the time a Minju Manager had gotten to it the bug had already been fixed.'
            elif reason.lower() == 'suggested':
                reason = 'Thanks for the suggestion, but this is already in the channel! Please check next time!'
            elif reason.lower() == 'info':
                reason = 'Thanks for your suggestion, but the information you provided is incorrect!'
            else:
                pass

            if reason.lower() in ['troll', 'blank']:
                pass
            else:
                # Deletes reason message
                await MessageReply.delete()
                # Sends confirmation of report/suggestion being denied
                await rejectreason.edit(embed=discord.Embed(title=f'{asd.embeds[0].title} successfully rejected!', description=f'{asd.embeds[0].title} [here](https://discord.com/channels/774031288318296085/861687628881199104/{msgid}) has successfully been rejected by **{ctx.author}**, and <@{reporterid}> has been DMd. Reason:\n\n> {reason}', color=random.choice(embedcolours)))
            # Tells original user their report/suggestion was accepted.
            await self.client.get_user(reporterid).send(embed=discord.Embed(title=f'Your {asd.embeds[0].title} has been rejected.', description=f'[Your {asd.embeds[0].title}](https://discord.com/channels/@me/{eauth}) was rejected by {ctx.author}.\n\nReason:\n> {reason}', color=random.choice(embedcolours)))


# Used to load cog
def setup(client):
    client.add_cog(Accept_and_Reject(client))
