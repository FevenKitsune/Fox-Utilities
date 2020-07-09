"""
Fox Utilities > developertools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from utility.checks import *
import datetime
from db import session, UserSettings
from utility.generators import generate_footer


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
        name="setsetting",
        brief="Testing the database function.",
        usage="<string>",
        hidden=True
    )
    @is_developer()
    async def set_setting(self, ctx, args):
        """Push a string setting to the database."""
        query = session.query(UserSettings)
        to_set = query.filter(UserSettings.discord_id == ctx.message.author.id).first()
        if to_set is None:
            to_set = UserSettings(discord_id=ctx.message.author.id, settings_json=args)
            session.add(to_set)
        else:
            to_set.settings_json = args
        session.commit()

        await ctx.send(f"Setting has been changed to {to_set.settings_json}")

    @commands.command(
        name="getsetting",
        brief="Testing the database function.",
        usage="",
        hidden=True
    )
    @is_developer()
    async def get_setting(self, ctx):
        """Read setting from database and return as message"""
        query = session.query(UserSettings)
        to_get = query.filter(UserSettings.discord_id == ctx.message.author.id).first()
        if to_get is None:
            await ctx.send("You have no setting json stored in the database.")
        else:
            await ctx.send(to_get.settings_json)

    @commands.command(
        name="dumpdb",
        brief="Testing the database function.",
        usage="",
        hidden=True
    )
    @is_developer()
    async def dump_db(self, ctx):
        """Dump contents of database to chat."""
        string_buffer = ""
        query = session.query(UserSettings).all()
        for setting in query:
            string_buffer += str(setting) + "\n"

        await ctx.send(f"```{string_buffer}```")


def setup(client):
    """Register class with client object."""
    client.add_cog(DeveloperTools(client))
