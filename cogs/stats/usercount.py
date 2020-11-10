"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class UserCount(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @command(
        name="usercount",
        aliases=["ucount", "membercount", "mcount", "users", "memcount"],
        brief="Displays the number of users the bot sees.",
        usage=""
    )
    async def user_count(self, ctx):
        """Counts the number of unique users the bot is connected to."""
        em = Embed(
            title="User Count",
            description=f"I can see a total of {len(ctx.bot.users):,} users!",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(UserCount(client))
