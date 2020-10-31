"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from db.dict import snipe_dict
from utils.generators import generate_footer


class Snipe(Cog):
    category = "utils"

    def __init__(self, client):
        self.client = client

    @command(
        name="snipe",
        brief="Tells you the last person who mentioned you in a channel.",
        usage="",
        help="The snipe command can be used to see the last time you were mentioned in the channel. The channel used "
             "will be the channel you send this command in."
    )
    async def snipe(self, ctx):
        """Retrieves the last mention within a given channel, even if that mention was deleted."""
        em = Embed(color=message_color)
        em.set_footer(text=generate_footer(ctx))

        try:
            grabbed_message = snipe_dict[f"{ctx.author.id}"][f"{ctx.channel.id}"]
        except KeyError:
            em.add_field(
                name=f"I don't see the last mention...",
                value=f"Mentions are stored for a limited period of time!"
            )
        else:
            em.add_field(
                name=f"I found something:",
                value=f"Mentioned by: <@{grabbed_message['author_id']}>\n\n{grabbed_message['content']}"
            )

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Snipe(client))
