"""
Fox Utilities > coretools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from utility.checks import *
from main import logger
from utility.generators import generate_footer


class CoreTools(commands.Cog):
    """
    CoreTools class

    Core bot functions and commands.
    """

    def __init__(self, client):
        self.client = client

    # Executes once the bot has finished starting.
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Setting client presence to: {bot_default_status}")
        # Set the bot status
        await client.change_presence(activity=discord.Game(bot_default_status))
        logger.info("Fox Utilities is now ready!")

    @commands.command(
        name="help",
        brief="Display this message.",
        usage=""
    )
    async def help(self, ctx, *args):
        # Setup embed
        em = discord.Embed(
            title="Fox Utilities Help Guide",
            description=bot_description,
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Command
        for cmd in sorted(self.client.commands, key=lambda command: command.cog_name):
            if cmd.hidden and not (ctx.author.id == developer_id):
                pass  # If not developer, do not show hidden commands.
            else:
                em.add_field(
                    name=f"{'#' if cmd.hidden else ''}`{cmd.cog_name}`> {cmd.name} {cmd.usage}",
                    value=cmd.brief,
                    inline=False
                )  # Help field formatter.

        await ctx.author.send(embed=em)

    @commands.command(
        name="tags",
        brief="Information about bot-permission tags.",
        usage=""
    )
    async def tags(self, ctx, *args):
        # Setup embed
        em = discord.Embed(
            title="Fox Utilities Permission Tags",
            description="Create a role with the syntax `fox:name_of_command` to give them permission to access that command! Will work with any admin command!",
            color=message_color)
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(CoreTools(client))
