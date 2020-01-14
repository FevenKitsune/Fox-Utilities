"""
Fox Utilities > misctools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
<<<<<<< HEAD:cogs/misctools.py
from utility.checks import *
import time

=======
from ext.checks import *

>>>>>>> 63e7596485a0bc46aa0ce63977335994af23cb3e:ext/misctools.py

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


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(MiscTools(client))
