"""
Fox Utilities > developertools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import discord
from discord.ext import commands
from ext.globals import *
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
        brief="A simple Hello World! command.",
        usage=""
    )
    async def hello_world(self, ctx):
        # Setup embed
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.author.name}")
        
        # Command
        em.add_field(
            name="Response",
            value="Hello world! [This is a test](https://www.google.com)"
        )
        await ctx.send(embed=em)

    @commands.command(
        name="except",
        brief="Throw a text exception.",
        usage=""
    )
    async def test_exception(self, ctx):
        # Command
        if (lambda r: r.name == role_tag[ctx.command.name], ctx.author.roles):
            await ctx.send(f"Has role```{role_tag[ctx.command.name]}``` ```{str((lambda r: r.name == role_tag[ctx.command.name], ctx.author.roles))}```")
        else:
            await ctx.send("Doesn't have role")
        raise UserWarning("Testing exception!")

    @commands.command(
        name="cbs",
        brief="Change bot status. Developer command.",
        usage="string",
        hidden=True
    )
    @is_developer()
    async def change_status(self, ctx, args):
        # Command
        await ctx.bot.change_presence(activity=discord.Game(args))
        await ctx.send(args)

    @commands.command(
        name="system_uptime",
        aliases=["suptime"],
        brief="Checks the system /proc/uptime.",
        usage="",
        hidden=True
    )
    @is_developer()
    async def sys_uptime(self, ctx):
        # Setup embed
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.author.name}")
        
        # Command
        with open("/proc/uptime", "r") as proc_ut:  # Read system uptime.
            ut = float(proc_ut.readline().split()[0])

        em.add_field(
            name="System Uptime",
            value=f"/proc/uptime: {str(datetime.timedelta(seconds=int(ut)))}"
        )
        await ctx.send(embed=em)

    @commands.command(
        name="botsay",
        aliases=["bs"],
        usage="<string>",
        hidden=True
    )
    @is_developer()
    async def botsay(self, ctx, args):
        # Command
        await ctx.message.delete()
        await ctx.send(args)


# Extension setup
def setup(client):
    client.add_cog(DeveloperTools(client))
