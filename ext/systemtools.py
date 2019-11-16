"""
Fox Utilities > systemtools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from ext.checks import *

import psutil
import sys
import os
import git


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
        # Command
        repo = git.Repo(
            os.getcwd(), search_parent_directories=True)  # Find git

        # Setup embed/command
        em = discord.Embed(
            title="Fox Utilities GitHub",
            description=f"```smalltalk\n{str(repo.git.pull())}\n```",
            color=message_color
        )  # Run git pull and post results into embed.
        em.set_footer(text="Invoked by: The Developer")
        await ctx.send(embed=em)

    @commands.command(
        name="reboot",
        brief="Reboot core bot. Developer command.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def reboot(self, ctx):
        em = discord.Embed(
            title="Rebooting the bot!",
            description="Please wait while the bot reboots...",
            color=message_color
        )
        em.set_footer(text="Invoked by: The Developer")
        await ctx.send(embed=em)

        # Command
        p = psutil.Process(os.getpid())  # Get bot process
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)  # Close all active connections and processes

        python = sys.executable  # Get python exec
        os.execl(python, python, *sys.argv)  # Start python process

    @commands.command(
        name="reload",
        brief="Reload bot extensions. Developer command.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def reload(self, ctx, *args):
        # Setup embed
        em = discord.Embed(
            title="System Reload",
            color=message_color
        )
        em.set_footer(text="Invoked by: The Developer")

        # Command variables
        success = []
        failed = []

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
            except Exception as e:  # Continue if unload failed.
                pass
        for extension in extensions:
            try:
                self.client.load_extension(extension)  # Load extension
            except Exception as e:  # Post error to embed if load failed.
                expt = f"{type(e).__name__}: {e}"
                failed.append([
                    extension,
                    expt
                ])
            else:  # Post to embed if load succeeded.
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
        exit()


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(SystemTools(client))
