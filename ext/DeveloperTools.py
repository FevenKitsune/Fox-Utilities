"""
Fox Utilities > DeveloperTools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
Do not redistribute!
"""

# Imports
from discord.ext import commands
import discord
import datetime

# Colors
COL_MESSAGE = 0xFFB600


# DeveloperTools extension class
class DeveloperTools:

    # Constructor
    def __init__(self, client):
        self.client = client

    # Hello world command
    @commands.command(
        name="hello",
        brief="A simple Hello World! command.",
        usage="")
    async def hello_world(self, ctx):
        em_hello = discord.Embed(color=COL_MESSAGE)
        em_hello.set_footer(text=f"Invoked by: {ctx.author.name}")
        em_hello.add_field(name="Response", value="Hello world! [This is a test](https://www.google.com)")
        await ctx.send(embed=em_hello)

    # Exception testing
    @commands.command(
        name="except",
        brief="Throw a text exception.",
        usage="")
    async def test_exception(self, ctx):
        raise UserWarning("Testing an exception!")

    # Change bot status
    @commands.command(
        name="cbs",
        brief="Change bot status. Developer command.",
        usage="string",
        hidden=True)
    async def change_status(self, ctx, args):
        if not (ctx.author.id == 276531286443556865):
            raise UserWarning("You must be the Developer to run this command!")

        await ctx.bot.change_presence(activity=discord.Game(args))
        await ctx.send(args)

    # Get system uptime
    @commands.command(
        name="system_uptime",
        aliases=["suptime"],
        brief="Checks the system /proc/uptime.",
        usage="",
        hidden=True)
    async def sys_uptime(self, ctx):
        if not (ctx.author.id == 276531286443556865):
            raise UserWarning("You must be the Developer to run this command!")

        em_sys_uptime = discord.Embed(color=COL_MESSAGE)
        em_sys_uptime.set_footer(text=f"Invoked by: {ctx.author.name}")
        with open("/proc/uptime", "r") as proc_ut:
            proc_ut_seconds = float(proc_ut.readline().split()[0])

        em_sys_uptime.add_field(name="System Uptime", value=f"/proc/uptime: {str(datetime.timedelta(seconds=int(proc_ut_seconds)))}")
        await ctx.send(embed=em_sys_uptime)

    # Botsay
    @commands.command(
        name="botsay",
        aliases=["bs"],
        usage="<string>",
        hidden=True)
    async def botsay(self, ctx, args):
        if not (ctx.author.id == 276531286443556865):
            return

        await ctx.message.delete()
        await ctx.send(args)\


# Extension setup
def setup(client):
    client.add_cog(DeveloperTools(client))
