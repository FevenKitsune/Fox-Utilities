"""
Fox Utilities > misctools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from utility.checks import *
import time


class MiscTools(commands.Cog):
    """
    MiscTools class

    Miscellaneous commands that don't need their own cog.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="time",
        aliases=["epoch"],
        brief="Returns current UNIX time",
        usage=""
    )
    async def epoch_time(self, ctx):
        # Embed setup
        em = discord.Embed(
            title=":clock1130: Current Epoch Time",
            description=f"{time.time():,.2f}s\n\n[What?](https://en.wikipedia.org/wiki/Unix_time)",
            color=message_color
        )
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        await ctx.send(embed=em)
    
    @commands.command(
        name="roll",
        aliases=["dice"],
        brief="Rolls the specified dice.",
        usage="[#dice]d[#face]"
    )
    async def roll(self, ctx, *args):
        await ctx.send(args)


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(MiscTools(client))
