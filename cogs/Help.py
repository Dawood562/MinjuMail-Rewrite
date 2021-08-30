import discord
from datetime import datetime
from discord.ext import commands

staffids = [389897179701182465, 221188745414574080, 303901339891531779, 257900648618655746, 193962293342502912, 364045258004365312, 297278578435948545, 368446019035463681]
ccids = [364045258004365312, 167625500498329600, 221188745414574080, 694953679719104544, 164795852785844225, 257900648618655746, 464113463468359690, 496650374741229569, 573854828363776006, 721247603290931200, 482613393803444227, 163608986401243136, 219668296834875403, 675867865701679176, 384584297090252813, 738473939168133211]

attributes = {
   'name': "help",
   'aliases': ["h"],
}


class MyHelp(commands.HelpCommand):
    """Get help with commands!"""
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)
    
    # _help
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Miscellaneous")
                embed.add_field(name=f'{cog_name}', value="\n".join(command_signatures), inline=True)
        await self.get_destination().send(embed=embed)
                
    # _help <cog name>
    async def send_cog_help(self, cog):
        command_signatures = [self.get_command_signature(command) for command in cog.get_commands()]
        desc = None
        if command_signatures:
            desc = '\n'.join(command_signatures)
        embed = discord.Embed(title=f'{cog.qualified_name[2:]} Help', description=f'**{cog.__doc__}**\n\n{desc}')
        await self.get_destination().send(embed=embed)
    
    # _help <group name>
    async def send_group_help(self, group):
        scmdname = [command.name for index, command in enumerate(group.commands)]
        scmddesc = [command.description for index, command in enumerate(group.commands)]
        command_signatures = [self.get_command_signature(command) for command in group.get_commands()]
        await self.get_destination().send(f'{group.name}: {subcommands}')
        embed = discord.Embed(title=f'Help for {group}', description=f'**{group.description}**')
        for i in range(len(scmd)-1):
            embed.add_field(name=f'{scmdname[i]}', value=f"a{scmddesc[i]}", inline=True)
        await self.get_destination().send(embed=embed)

    
    # _help <command name>
    async def send_command_help(self, command):
        await self.get_destination().send(command.name)

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
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
