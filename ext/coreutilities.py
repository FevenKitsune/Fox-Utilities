"""
Fox Utilities > coreutilities.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import discord
from discord.ext import commands
from ext.globals import *
from ext.checks import *

import psutil
import sys
import os
import git


class CoreUtilities(commands.Cog):
    """
    CoreUtilities class

    Core system operation commands.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="help",
        brief="Display this message.",
        usage=""
    )
    async def help(self, ctx, *args):
        # Setup embed
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        for cmd in sorted(self.client.commands, key=lambda command: command.cog_name):
            if (cmd.hidden) and not (ctx.author.id == DEV_ID):
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
        brief="Lists all bot-permission tags.",
        usage=""
    )
    async def tags(self, ctx, *args):
        # Setup embed
        em = discord.Embed(
            title="Fox Utilities Permission Tags",
            description="Create a role with the name of a tag to give someone permission to run the tags respective command.",
            color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        for x in role_tag:
            em.add_field(
                name=x,
                value=role_tag[x]
            )

        await ctx.send(embed=em)

# Extension setup
def setup(client):
    client.add_cog(CoreUtilities(client))
