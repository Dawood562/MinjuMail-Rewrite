import discord
from datetime import datetime
from discord.ext import commands

staffids = [389897179701182465, 221188745414574080, 303901339891531779, 257900648618655746, 193962293342502912, 364045258004365312, 297278578435948545, 368446019035463681]
ccids = [364045258004365312, 167625500498329600, 221188745414574080, 694953679719104544, 164795852785844225, 257900648618655746, 464113463468359690, 496650374741229569, 573854828363776006, 721247603290931200, 482613393803444227, 163608986401243136, 219668296834875403, 675867865701679176, 384584297090252813, 738473939168133211]


class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.group(aliases=['h'], invoke_without_command=True)
    async def help(self, ctx):
        HelpEmbed = discord.Embed(color=random.choice(embedcolours), title='List of all commands', description='help\nreport\nsuggest\n')
        if ctx.author.id in staffids:
            HelpEmbed.add_field(name='Admin', value='accept\nload\nreject\nreload\nunload', inline=True)
        if ctx.author.id in ccids:
            HelpEmbed.add_field(name='Card Creators', value='ingame', inline=True)
    
    
    @help.commands(aliases=['h'])
    async def help(self, ctx):
        HelpEmbed = discord.Embed(color=random.choice(embedcolours), title='Help for Help', description='`<>` marks required parameters.\n`[]` marks optional parameters.')
        HelpEmbed.add_field(name='Description', value='Get help with commands.')
        HelpEmbed.add_field(name='Alias', value='h')
        HelpEmbed.add_field(name='Valid Arguments', value='Any command.')
        HelpEmbed.add_field(name='Usage', value='`_help` `[command_name]`')
                            
                            
                            
    @help.commands(aliases=['r'])
    async def report(self, ctx):
        HelpEmbed = discord.Embed(color=random.choice(embedcolours), title='Help for Report', description='`<>` marks required parameters.\n`[]` marks optional parameters.')
        HelpEmbed.add_field(name='Description', value='Suggest a group, soloist, or k-drama to be added to Minju bot!')
        HelpEmbed.add_field(name='Alias', value='s')
        HelpEmbed.add_field(name='Valid Arguments', value='`bug`/`b`\n`player`/`user`\n`scam`')
        HelpEmbed.add_field(name='Usage', value='`_report` `<bug|player|scam>`')
    
    
    @help.commands(aliases=['s'])
    async def suggest(self, ctx):
        HelpEmbed = discord.Embed(color=random.choice(embedcolours), title='Help for Suggest', description='`<>` marks required parameters.\n`[]` marks optional parameters.')
        HelpEmbed.add_field(name='Description', value='Suggest a group, soloist, or k-drama to be added to Minju bot!')
        HelpEmbed.add_field(name='Alias', value='s')
        HelpEmbed.add_field(name='Valid Arguments', value='`drama`/`k-drama`/`d`/`k`\n`group`/`groups`/`g`\n`soloist`/`solo`/`s`')
        HelpEmbed.add_field(name='Usage', value='`_suggest` `<drama|group|soloist>`')
        
        
def setup(client):
    client.add_cog(help(client))
