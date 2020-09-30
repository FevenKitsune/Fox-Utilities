"""
Fox Utilities > systemtools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import os
import sys

import discord
import git
import psutil
from discord.ext import commands

from utils.checks import is_developer
from utils.generators import generate_footer


class SystemTools(commands.Cog):
    """
    SystemTools Class

    Core maitnence functionality to update, reboot, and reload the bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="pull",
        brief="Git pull from GitHub repo.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def git_pull(self, ctx):
        """Pulls the latest version of the bot from Git"""
        # Find Git repository the bot is stored in
        repo = git.Repo(os.getcwd(), search_parent_directories=True)

        # Run git pull and post results into embed.
        em = discord.Embed(
            title="Fox Utilities GitHub",
            description=f"```smalltalk\n{str(repo.git.pull())}\n```",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.send(embed=em)

    @commands.command(
        name="reboot",
        brief="Reboot core bot. Developer command.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def reboot(self, ctx):
        """Restart the bot on the system level."""
        em = discord.Embed(
            title="Rebooting the bot!",
            description="Please wait while the bot reboots...",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.send(embed=em)

        # Get bot process
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            # Close all active connections and processes
            os.close(handler.fd)

        # Get python exec
        python = sys.executable
        # Start python process
        os.execl(python, python, *sys.argv)

    @commands.command(
        name="reload",
        brief="Reload bot extensions. Developer command.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def reload(self, ctx, *args):
        """Unload all discord.py cogs and load them back. Easier than a full reboot."""
        em = discord.Embed(
            title="System Reload",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Stores which cogs passed and which cogs failed.
        success = []
        failed = []

        # Check for extensions first.
        if len(extensions) == 0:
            em.add_field(
                name="Oh well.",
                value="Doesn't look like there are any extensions defined.")
            await ctx.send(embed=em)
            return
        for extension in extensions:
            try:
                # Unload extension
                self.client.unload_extension(extension)
            # Continue if unload failed.
            except Exception as e:
                pass
        for extension in extensions:
            try:
                # Load extension
                self.client.load_extension(extension)
            except Exception as e:
                # Post error to embed if load failed.
                expt = f"{type(e).__name__}: {e}"
                failed.append([extension, expt])
            else:
                # Post to embed if load succeeded.
                success.append(extension)

        em.add_field(
            name=":white_check_mark: Load Passed:",
            value='\n'.join([
                f"`{i}: PASS`" for i in success
            ]) if success else "`None`"
        )

        em.add_field(
            name=":warning: Load Failed:",
            value='\n'.join([
                f"`{i[0]}: {i[1]}`" for i in failed
            ]) if failed else "`None`"
        )
        await ctx.send(embed=em)

    @commands.command(
        name="stop",
        brief="Force stop the bot.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def stop_bot(self, ctx):
        """Force stops the bot."""
        exit()


def setup(client):
    """Register class with client object."""
    client.add_cog(SystemTools(client))
