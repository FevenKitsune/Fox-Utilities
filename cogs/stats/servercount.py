"""
Fox Utilities > stats > servercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class ServerCount(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @command(
        name="servercount",
        aliases=["scount", "servers"],
        brief="Displays the number of servers the bot is currently connected to.",
        usage=""
    )
    async def server_count(self, ctx):
        """Counts the number of servers the bot is connected to."""
        em = Embed(
            title="Server Count",
            description=f"I am currently connected to {len(self.client.guilds):,} servers.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(ServerCount(client))
