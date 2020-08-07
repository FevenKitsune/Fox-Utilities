"""
Fox Utilities > help.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from utility.checks import *
from utility.generators import generate_footer


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
        usage="<command>",
        help="The help command can be used to get a list of commands that are available to the user. "
             "If you'd like to see more detailed information about a command, use `help <command>`."
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
                    value=command.help
                )
            else:
                # If the argument given was not a valid command, throw an error.
                raise UserWarning(f"Command \"{args[0]}\" was not found.")
        else:
            for cmd in sorted(self.client.commands, key=lambda command: command.cog_name):
                # If not developer, do not show hidden commands.
                if cmd.hidden and not (ctx.author.id == developer_id):
                    pass
                else:
                    # Help field formatter.
                    em.add_field(
                        name=f"{'#' if cmd.hidden else ''}`{cmd.cog_name}`> {cmd.name} {cmd.usage}",
                        value=cmd.brief,
                        inline=False
                    )

        await ctx.author.send(embed=em)


def setup(client):
    """Register class with client object."""
    client.add_cog(Help(client))
