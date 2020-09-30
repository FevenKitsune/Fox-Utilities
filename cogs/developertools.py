"""
Fox Utilities > developertools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import datetime

import discord
from discord.ext import commands

from config.globals import message_color
from db import session, UserSettings
from utils.checks import is_developer
from utils.generators import generate_footer


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
        em = discord.Embed(
            title="Response",
            description="Hello world!",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

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
        # Read system uptime.
        with open("/proc/uptime", "r") as proc_ut:
            ut = float(proc_ut.readline().split()[0])

        em = discord.Embed(
            title="Container Uptime",
            description=f"/proc/uptime: {str(datetime.timedelta(seconds=int(ut)))}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

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
        """Echo back a string as a message."""
        await ctx.message.delete()
        await ctx.send(args)

    @commands.command(
        name="lendb",
        brief="Check how many entries are in the database.",
        usage="",
        hidden=True
    )
    @is_developer()
    async def len_db(self, ctx):
        """Count the number of entries in the database."""
        query = session.query(UserSettings).all()
        await ctx.send(f"```{len(query)}```")


def setup(client):
    """Register class with client object."""
    client.add_cog(DeveloperTools(client))
