"""
Fox Utilities > info > tags.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext import commands

from config.globals import message_color
from utils.generators import generate_footer


class Tags(commands.Cog):
    category = "testing"

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="tags",
        brief="Information about bot-permission tags.",
        usage="",
        help="The tags command can be used to get information on role-assigned permissions."
    )
    async def tags(self, ctx):
        """Gives the user information on permission tags, which allow non-admins to access admin commands."""
        em = Embed(
            title="Fox Utilities Permission Tags",
            description="Create a role with the syntax `fox:name_of_command` to give them "
                        "permission to access that command! Will work with any admin command!",
            color=message_color)
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Tags(client))
