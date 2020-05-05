"""
Fox Utilities > misctools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from utility.checks import *
import time
from random import sample
from utility.generators import generate_footer


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
        em.set_footer(text=generate_footer(ctx))
        await ctx.send(embed=em)
    
    @commands.command(
        name="roll",
        aliases=["dice"],
        brief="Rolls the specified dice.",
        usage="[#dice]d[#faces]"
    )
    async def roll(self, ctx, *args):
        if len(args) < 1:
            raise UserWarning("You must specify a roll to use this command!")
        
        try:
            d_index = args[0].lower().index('d')
            qty = int(args[0].lower()[0:d_index])
            faces = int(args[0].lower()[d_index+1:])
        except ValueError:
            raise UserWarning("Invalid formatting of dice roll!")

        if qty > 50: raise UserWarning("Maximum of 50 dice at once.")
        if faces > 10000: raise UserWarning("Maximum of 10,000 faces per die.")

        rolls = sample(range(1, faces + 1), qty)

        # Embed setup
        em = discord.Embed(
            title=f":game_die: Rolling {qty}d{'{:,}'.format(faces)}...",
            description=f"{', '.join(['{:,}'.format(i) for i in rolls])}\n\nTotal: {'{:,}'.format(sum(rolls))}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.send(embed=em)


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(MiscTools(client))
