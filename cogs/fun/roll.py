"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from random import sample

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class Roll(Cog):
    category = "fun"

    def __init__(self, client):
        self.client = client

    @command(
        name="roll",
        aliases=["dice"],
        brief="Rolls the specified dice.",
        usage="[#dice]d[#faces]"
    )
    async def roll(self, ctx, *args):
        """Generate a random number based on dice given in D&D style parameters (ex. 1d6)"""
        if len(args) < 1:
            raise UserWarning("You must specify a roll to use this command!")

        try:
            d_index = args[0].lower().index('d')
            qty = int(args[0].lower()[0:d_index])
            faces = int(args[0].lower()[d_index + 1:])
        except ValueError:
            raise UserWarning("Invalid formatting of dice roll!")

        if qty > 50:
            raise UserWarning("Maximum of 50 dice at once.")
        if faces > 10000:
            raise UserWarning("Maximum of 10,000 faces per die.")

        rolls = sample(range(1, faces + 1), qty)

        em = Embed(
            title=f":game_die: Rolling {qty}d{'{:,}'.format(faces)}...",
            description=f"{', '.join(['{:,}'.format(i) for i in rolls])}\n\nTotal: {'{:,}'.format(sum(rolls))}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Roll(client))
