"""
Fox Utilities > misctools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from ext.checks import *
import time

class MiscTools(commands.Cog):
    """
    MiscTools class

    Miscellaneous commands and utilities.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="time",
        aliases=["epoch"],
        brief="Returns current UNIX time",
        usage=""
    )
    def epoch_time(self, ctx):
        # Embed setup
        em = discord.Embed(
            title="Current Epoch Time",
            description=f"{str(time.time())}",
            color=message_color
        )
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        await ctx.send(embed=em)


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(MiscTools(client))
