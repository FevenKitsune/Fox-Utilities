"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class Ping(Cog):
    category = "utils"

    def __init__(self, client):
        self.client = client

    @command(
        name="ping",
        aliases=["pong"],
        brief="A simple command to see if the bot is running.",
        usage=""
    )
    async def ping_bot(self, ctx):
        """Basic call and response command"""
        em = Embed(
            title="Pong!",
            description=f"Discord WebSocket latency: {round(ctx.bot.latency * 1000)}ms\n"
                        f"Shard Count: {len(ctx.bot.shards)}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Ping(client))
