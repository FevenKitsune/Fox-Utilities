"""
Fox Utilities > info > invite.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext import commands

from config.globals import message_color, bot_invite, bot_development_server, bot_source, bot_wiki
from utils.generators import generate_footer


class Invite(commands.Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="invite",
        aliases=["source", "code"],
        brief="Invite this bot to your guild.",
        usage="",
        help="The invite command can be used to get information on how to invite the bot to your guild. It also "
             "contains links to the development server, GitHub page, and Wiki."
    )
    async def invite_bot(self, ctx):
        """Sends information on the development server, the GitHub, and the invite link."""
        em = Embed(
            title="Invite me!",
            description=f"[Invite link!]({bot_invite})\n"
                        f"[Development server!]({bot_development_server})\n"
                        f"[GitHub!]({bot_source})\n"
                        f"[Wiki!]({bot_wiki})",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Invite(client))
