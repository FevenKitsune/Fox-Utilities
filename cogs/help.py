"""
Fox Utilities > help.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import discord
from discord.ext import commands

from config.globals import bot_description, message_color, developer_id
from utils.generators import generate_footer


class Help(commands.Cog):
    """
    Help class

    Generates and outputs the help menu.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="help",
        brief="Display this message.",
        usage="[command]",
        help="The help command can be used to get a list of commands that are available to the user. "
             "If you'd like to see more detailed information about a command, use `help [command]`.\n\n"
             "**Usage Information**\n"
             "Certain commands will have extra information on "
             "[arguments](https://en.wikipedia.org/wiki/Command-line_interface#Arguments) you can give the command to"
             "operate it.\n\n"
             "*[argument]*: Arguments marked with [] are optional, and are not required.\n"
             "*argument*: Arguments without [] are required to use the command.\n"
             "*argument/\"argument\"*: Arguments separated with a slash delineate two ways of stating the same argument."
    )
    async def help(self, ctx, *args):
        """Help menu. Processes the list of available commands into a readable menu."""
        em = discord.Embed(
            title="Fox Utilities Help Guide",
            description=bot_description,
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # If asking about a specific command, search for that command or its aliases.
        # Double := because I enjoy making Python programmers angry.
        if args and (search := args[0]):
            if command := self.client.get_command(search):
                em.add_field(
                    name=f"{'#' if command.hidden else ''}`{command.cog_name}`\n{command.name} {command.usage}",
                    value=f"{command.help}\n\n**Aliases**\n{command.aliases}"
                )
            else:
                # If the argument given was not a valid command, throw an error.
                raise UserWarning(f"Command \"{args[0]}\" was not found.")
        else:
            for cog in [self.client.get_cog(cog_name) for cog_name in sorted(self.client.cogs)]:
                # List of formatted strings containing each command.
                command_list = []
                # Get each command and figure out how they should be formatted.
                for command in sorted(cog.walk_commands(), key=lambda key: key.name):
                    if command.hidden and not (ctx.author.id == developer_id):
                        pass
                    # Add formatted string to the list.
                    command_list.append(
                        f"{'#' if command.hidden else ''}"
                        f"`{' '.join((command.name, command.usage)).strip()}` {command.brief}"
                    )
                em.add_field(name=cog.qualified_name, value="\n".join(command_list), inline=False)

        await ctx.author.send(embed=em)


def setup(client):
    """Register class with client object."""
    client.add_cog(Help(client))
