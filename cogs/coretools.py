"""
Fox Utilities > coretools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

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

    @commands.Cog.listener()
    async def on_ready(self):
        """Executes once the bot has finished starting up."""
        logger.info(f"Setting client presence to: {bot_default_status}")
        # Set the bot status
        await self.client.change_presence(activity=discord.Game(bot_default_status))
        logger.info("Fox Utilities is now ready!")

    @commands.command(
        name="tags",
        brief="Information about bot-permission tags.",
        usage=""
    )
    async def tags(self, ctx):
        """Gives the user information on permission tags, which allow non-admins to access admin commands."""
        em = discord.Embed(
            title="Fox Utilities Permission Tags",
            description="Create a role with the syntax `fox:name_of_command` to give them "
                        "permission to access that command! Will work with any admin command!",
            color=message_color)
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)

    @commands.command(
        name="report",
        aliases=["bug", "error", "contact"],
        brief="Need to report a bug? Get information on how to do so here.",
        usage=""
    )
    async def report_bug(self, ctx):
        """Gives the user information on how to report bugs they find."""
        em = discord.Embed(
            title="Found a bug? :bee:",
            description="You can report bugs on the "
                        "[Fox Utilities issues](https://github.com/FevenKitsune/Fox-Utilities/issues) page on GitHub!",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    """Register class with client object."""
    client.add_cog(CoreTools(client))
