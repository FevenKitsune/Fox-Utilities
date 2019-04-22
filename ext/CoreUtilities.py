"""
Fox Utilities > CoreUtilities.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
"""

# Imports
from discord.ext import commands
import discord
import psutil
import sys
import os
import git
from ext.globals import *


class CoreUtilities(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Extension reload command
    @commands.command(
        name="reload",
        brief="Reload bot extensions. Developer command.",
        hidden=True,
        usage="")
    async def reload(self, ctx, *args):
        if not (ctx.author.id == DEV_ID):
            raise UserWarning("You must be the developer to run this command!")

        em_reload = discord.Embed(color=COL_MESSAGE)
        em_reload.set_footer(text="Invoked by: The Developer")

        # Check if there are any extensions first.
        if len(extensions) == 0:
            em_reload.add_field(name="Oh well.", value="Doesn't look like there are any extensions defined.")
            await ctx.send(embed=em_reload)
            return

        for extension in extensions:
            try:
                self.client.unload_extension(extension)
            except Exception as e:
                expt = f"{type(e).__name__}: {e}"
                em_reload.add_field(
                    name=f"{extension}",
                    value=f"Failed to unload extension {extension}\nException: {expt}")
            else:
                em_reload.add_field(
                    name=f"{extension}", 
                    value=f"Successfully unloaded extension {extension}")

        for extension in extensions:
            try:
                self.client.load_extension(extension)
            except Exception as e:
                expt = f"{type(e).__name__}: {e}"
                em_reload.add_field(
                    name=f"{extension}",
                    value=f"Failed to load extension {extension}\nException: {expt}")
            else:
                em_reload.add_field(
                    name=f"{extension}",
                    value=f"Successfully loaded extension {extension}")

        await ctx.send(embed=em_reload)

    # Git Pull command
    @commands.command(
        name="pull",
        brief="Git pull from GitHub repo.",
        hidden=True,
        usage=""
    )
    async def git_pull(self, ctx):
        if not (ctx.author.id == DEV_ID):
            raise UserWarning("You must be developer to run this command!")

        repo = git.Repo(os.getcwd(), search_parent_directories=True)

        em_pull = discord.Embed(color=COL_MESSAGE)
        em_pull.set_footer(text="Invoked by: The Developer")
        em_pull.add_field(
            name="Fox Utilities GitHub",
            value=f"```smalltalk\n{str(repo.git.pull())}\n```"
        )

        await ctx.send(embed=em_pull)

    # Reboot command
    @commands.command(
        name="reboot",
        brief="Reboot core bot. Developer command.",
        hidden=True,
        usage=""
    )
    async def reboot(self, ctx):
        if not (ctx.author.id == DEV_ID):
            raise UserWarning("You must be developer to run this command!")

        em_reboot = discord.Embed(color=COL_MESSAGE)
        em_reboot.set_footer(text="Invoked by: The Developer")

        em_reboot.add_field(
            name="Rebooting bot!",
            value="Please wait while the bot reboots...")

        await ctx.send(embed=em_reboot)

        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)

        python = sys.executable
        os.execl(python, python, *sys.argv)

    # Help command
    @commands.command(
        name="help",
        brief="Display this message.",
        usage="")
    async def help(self, ctx, *args):
        em_help = discord.Embed(color=COL_MESSAGE)
        em_help.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        for cmd in sorted(self.client.commands, key=lambda command: command.cog_name):
            if (cmd.hidden) and not (ctx.author.id == DEV_ID):
                pass
            else:
                em_help.add_field(
                    name=f"{'#' if cmd.hidden else ''}`{cmd.cog_name}`> {cmd.name} {cmd.usage}",
                    value=cmd.brief,
                    inline=False)

        await ctx.author.send(embed=em_help)


# Extension setup
def setup(client):
    client.add_cog(CoreUtilities(client))