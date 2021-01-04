from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class Prefix(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @command(
        name="prefix",
        brief="Information about setting Fox Utilities prefix.",
        usage="",
        help="Returns information on how to use the Fox Utilities prefix tags to configure the prefix used in your "
             "guild."
    )
    async def prefix(self, ctx):
        """Gives the user information on prefix tags. This allows per-guild prefix settings."""
        em = Embed(
            title="Fox Utilities Prefix Tags",
            description="Create a server role with the syntax `fox_prefix:desired_prefix`. Assign this role to the "
                        "Fox Utilities bot to give it a new prefix.",
            color=message_color)
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Prefix(client))
