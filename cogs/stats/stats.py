"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from datetime import timedelta

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class Stats(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @command(
        name="stats",
        aliases=["bot_stats", "servercount", "scount", "servers", "usercount", "ucount", "membercount", "mcount",
                 "users", "memcount", "ping", "pong", "system_uptime", "suptime", "uptime"],
        brief="Displays full system statistics and diagnostics.",
        usage=""
    )
    async def stats(self, ctx):
        """Posts a full system statistics page"""
        em = Embed(
            title="System Statistics",
            color=message_color
        )

        # Read container uptime and add it to a field.
        with open("/proc/uptime", "r") as proc_ut:
            ut = float(proc_ut.readline().split()[0])

        em.add_field(
            name="Container Uptime",
            value=f"/proc/uptime: {str(timedelta(seconds=int(ut)))}"
        )
