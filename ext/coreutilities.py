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
        name="reload",
        brief="Reload bot extensions. Developer command.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def reload(self, ctx, *args):
        # Setup embed
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text="Invoked by: The Developer")

        # Command
        if len(extensions) == 0:  # Check for extensions first.
            em.add_field(
                name="Oh well.",
                value="Doesn't look like there are any extensions defined.")
            await ctx.send(embed=em)
            return
        for extension in extensions:
            try:
                self.client.unload_extension(extension)  # Unload extension
            except Exception as e:  # Post error to embed if unload failed.
                expt = f"{type(e).__name__}: {e}"
                em.add_field(
                    name=f"{extension}",
                    value=f"Failed to unload extension {extension}\nException: {expt}"
                )
            else:  # Post to embed if unload succeeded.
                em.add_field(
                    name=f"{extension}",
                    value=f"Successfully unloaded extension {extension}"
                )
        for extension in extensions:
            try:
                self.client.load_extension(extension)  # Load extension
            except Exception as e:  # Post error to embed if load failed.
                expt = f"{type(e).__name__}: {e}"
                em.add_field(
                    name=f"{extension}",
                    value=f"Failed to load extension {extension}\nException: {expt}"
                )
            else:  # Post to embed if load succeeded.
                em.add_field(
                    name=f"{extension}",
                    value=f"Successfully loaded extension {extension}"
                )
        await ctx.send(embed=em)

    # Git Pull command
    @commands.command(
        name="pull",
        brief="Git pull from GitHub repo.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def git_pull(self, ctx):
        # Setup embed
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text="Invoked by: The Developer")

        # Command
        repo = git.Repo(os.getcwd(), search_parent_directories=True)  # Find git
        em.add_field(
            name="Fox Utilities GitHub",
            value=f"```smalltalk\n{str(repo.git.pull())}\n```"
        )  # Run git pull and post results into embed.

        await ctx.send(embed=em)

    # Reboot command
    @commands.command(
        name="reboot",
        brief="Reboot core bot. Developer command.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def reboot(self, ctx):
        # Setup embed
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text="Invoked by: The Developer")

        # Command
        em.add_field(
            name="Rebooting bot!",
            value="Please wait while the bot reboots..."
        )

        await ctx.send(embed=em)

        p = psutil.Process(os.getpid())  # Get bot process
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)  # Close all active connections and processes

        python = sys.executable  # Get python exec
        os.execl(python, python, *sys.argv)  # Start python process

    # Help command
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


# Extension setup
def setup(client):
    client.add_cog(CoreUtilities(client))
