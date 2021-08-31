import discord
from datetime import datetime
from discord.ext import commands
import random

staffids = [389897179701182465, 221188745414574080, 303901339891531779, 257900648618655746, 193962293342502912, 364045258004365312, 297278578435948545, 368446019035463681]
ccids = [364045258004365312, 167625500498329600, 221188745414574080, 694953679719104544, 164795852785844225, 257900648618655746, 464113463468359690, 496650374741229569, 573854828363776006, 721247603290931200, 482613393803444227, 163608986401243136, 219668296834875403, 675867865701679176, 384584297090252813, 738473939168133211]
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]

attributes = {
   'name': "help",
   'aliases': ["h"],
   'description': "Get help with commands."
}


class MyHelp(commands.HelpCommand):
    """Get help with commands!"""
    def get_command_signature(self, command):
        if command.signature == '':
            return '`{0.clean_prefix}{1.qualified_name}`'.format(self, command)
        else:
           return '`{0.clean_prefix}{1.qualified_name}` `{1.signature}`'.format(self, command)
    
    # _help
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=random.choice(embedcolours))
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Miscellaneous")
                embed.add_field(name=f'{cog_name}', value="\n".join(command_signatures), inline=True)
        embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
        await self.get_destination().send(embed=embed)
                
    # _help <cog name>
    async def send_cog_help(self, cog):
        command_signatures = [self.get_command_signature(command) for command in cog.get_commands()]
        desc = None
        if command_signatures:
            desc = '\n'.join(command_signatures)
        embed = discord.Embed(title=f'{cog.qualified_name[2:]} Help', description=f'**{cog.__doc__}**\n\n{desc}', color=random.choice(embedcolours))
        embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
        await self.get_destination().send(embed=embed)
    
    # _help <group name>
    async def send_group_help(self, group):
        scmdname = [command.name for index, command in enumerate(group.commands)]
        scmddesc = [command.description for index, command in enumerate(group.commands)]
        command_signatures = [self.get_command_signature(command) for command in group.commands]
        await self.get_destination().send(f'CMD Signatures: {command_signatures}')
        await self.get_destination().send(f'CMD qualified name(s?): {[command.qualified_name for command in group.commands]}')
        await self.get_destination().send(f'Group name: {group}, {group.name}')
        tostrip = f'_{group} '
        arg_subcmds = '<'
        for i in scmdname:
            arg_subcmds += f'{i}|'
        arg_subcmds = f'{arg_subcmds[:-1]}>'
        embed = discord.Embed(title=f'Help for {group.name}', description=f'Displaying help for {group}.\n`<>` marks required parameters.\n`[]` marks optional parameters.', color=random.choice(embedcolours))
        for i in range(len(scmdname)):
            embed.add_field(name=f'{scmdname[i].capitalize()}', value=f"{scmddesc[i]}", inline=True)
        embed.add_field(name=f'Description', value=f"{' '.join(scmddesc)}", inline=True)
        
        if len(command.aliases) == 0:
            aliases = None
        else:
            aliases = []
            for i in range(len(command.aliases)):
                aliases.append(f'`{command.aliases[i]}`')
                aliases = ', '.join(aliases)
        embed.add_field(name=f'Aliases', value=aliases, inline=True)

        embed.add_field(name=f'Usage', value='\n'.join(command_signatures), inline=True)
        embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
        await self.get_destination().send(embed=embed)

    
    # _help <command name>
    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help for {command.name}", description=f'Displaying help for {command.name}.\n`<>` marks required parameters.\n`[]` marks optional parameters.', color=random.choice(embedcolours))
        embed.add_field(name='Description', value=command.description, inline=False)
        if len(command.aliases) == 0:
            aliases = None
        else:
            aliases = []
            for i in range(len(command.aliases)):
                aliases.append(f'`{command.aliases[i]}`')
                aliases = ', '.join(aliases)
        embed.add_field(name='Aliases', value=aliases, inline=False)
        embed.add_field(name='Usage', value=self.get_command_signature(command), inline=False)
        embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
        await self.get_destination().send(embed=embed)

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            raise error


class Help(commands.Cog, name='🤔 Help'):
    """Get help with commands!"""
    def __init__(self, client):
        self.client = client

       # Setting the cog for the help
        help_command = MyHelp(command_attrs=attributes)
        help_command.cog = self # Instance of YourCog class
        self.client.help_command = help_command

def setup(client):
    client.add_cog(Help(client))
