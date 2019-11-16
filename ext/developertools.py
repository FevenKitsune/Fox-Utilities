"""
Fox Utilities > developertools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from ext.checks import *
import datetime


class DeveloperTools(commands.Cog):
    """
    DeveloperTools class

    Various commands and tools for development and testing.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="hello",
        brief="A simple \"Hello World!\" command. Things are running smoothly!",
        usage=""
    )
    async def hello_world(self, ctx):
        """Respond with an embedded response."""
        # Setup embed
        em = discord.Embed(
            title="Response",
            description="Hello world!",
            color=message_color
        )
        em.set_footer(text=f"Invoked by: {ctx.author.name}")

        await ctx.send(embed=em)

    @commands.command(
        name="except",
        brief="Throw a test error. Used to test the exception handler.",
        usage=""
    )
    async def test_exception(self, ctx):
        """Throw an exception to test the exception functions"""
        raise UserWarning("Testing exception!")

    @commands.command(
        name="cbs",
        brief="Change the bot status. Developer only command!",
        usage="string",
        hidden=True
    )
    @is_developer()
    async def change_status(self, ctx, args):
        """Change the game status of the bot."""
        # Command
        await ctx.bot.change_presence(activity=discord.Game(args))
        await ctx.send(args)

    @commands.command(
        name="system_uptime",
        aliases=["suptime", "uptime"],
        brief="Checks the container /proc/uptime. Developer only command!",
        usage="",
        hidden=True
    )
    @is_developer()
    async def sys_uptime(self, ctx):
        """Get system uptime from container."""
        with open("/proc/uptime", "r") as proc_ut:  # Read system uptime.
            ut = float(proc_ut.readline().split()[0])

        # Setup embed
        em = discord.Embed(
            title="Container Uptime",
            description=f"/proc/uptime: {str(datetime.timedelta(seconds=int(ut)))}",
            color=message_color
        )
        em.set_footer(text=f"Invoked by: {ctx.author.name}")

        await ctx.send(embed=em)

    @commands.command(
        name="botsay",
        aliases=["bs"],
        brief="Make the bot say something. Developer only command!",
        usage="<string>",
        hidden=True
    )
    @is_developer()
    async def botsay(self, ctx, args):
        """Echo back a string as an embedded message."""
        # Command
        await ctx.message.delete()
        await ctx.send(args)


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(DeveloperTools(client))
