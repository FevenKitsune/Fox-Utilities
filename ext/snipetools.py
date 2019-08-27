"""
Fox Utilities > snipetools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from ext.checks import *
from ext.globals import snipe_db


class SnipeTools(commands.Cog):
    """
    SnipeTools class

    Function for SnipeTools.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        for member in message.mentions:
            snipe_db.update({
                f"{member.id}": {
                    f"{message.channel.id}": message
                }
            })

    @commands.command(
        name="snipe",
        brief="Tells you the last person who mentioned you in a channel.",
        usage=""
    )
    async def sniped(self, ctx):
        # Embed setup
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        try:
            grabbed_message = snipe_db[f"{ctx.author.id}"][f"{ctx.channel.id}"]
        except Exception:
            em.add_field(
                name=f"I don't see the last mention...",
                value=f"Mentions are stored for a limited period of time!"
            )
        else:
            em.add_field(
                name=f"You Were Last Mentioned By: {grabbed_message.author.mention}",
                value=f"{grabbed_message.content}"
            )

        await ctx.send(embed=em)

# Extension setup


def setup(client):
    client.add_cog(SnipeTools(client))
