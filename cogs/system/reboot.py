"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from os import getpid, close, execl
from sys import executable, argv

from discord import Embed
from discord.ext.commands import Cog, command
from psutil import Process

from config.globals import message_color
from utils.checks import is_developer
from utils.generators import generate_footer


class Reboot(Cog):
    category = "system"

    def __init__(self, client):
        self.client = client

    @command(
        name="reboot",
        brief="Reboot core bot. Developer command.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def reboot(self, ctx):
        """Restart the bot on the system level."""
        em = Embed(
            title="Rebooting the bot!",
            description="Please wait while the bot reboots...",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.send(embed=em)

        # Get bot process
        p = Process(getpid())
        for handler in p.open_files() + p.connections():
            # Close all active connections and processes
            close(handler.fd)

        # Get python exec
        python = executable
        # Start python process
        execl(python, python, *argv)


def setup(client):
    client.add_cog(Reboot(client))
