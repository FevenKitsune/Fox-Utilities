"""
Fox Utilities > info > systemuptime.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from datetime import timedelta

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class SystemUptime(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @command(
        name="system_uptime",
        aliases=["suptime", "uptime"],
        brief="Checks the container /proc/uptime.",
        usage=""
    )
    async def system_uptime(self, ctx):
        """Get system uptime from container."""
        # Read system uptime.
        with open("/proc/uptime", "r") as proc_ut:
            ut = float(proc_ut.readline().split()[0])

        em = Embed(
            title="Container Uptime",
            description=f"/proc/uptime: {str(timedelta(seconds=int(ut)))}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(SystemUptime(client))
