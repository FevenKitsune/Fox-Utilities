from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class Tags(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @command(
        name="tags",
        brief="Information about permission tags.",
        usage="",
        help="Returns information on how to use the Fox Utilities permission tags to give any user access to "
             "commands that require administrator permissions."
    )
    async def tags(self, ctx):
        """Gives the user information on permission tags, which allow non-admins to access admin commands."""
        em = Embed(
            title="Fox Utilities Permission Tags",
            description="Create a server role with the syntax `fox:name_of_command`. Assign any user to this role to "
                        "give them access to the named command. This will work with any command that requires "
                        "administrator permissions to access.",
            color=message_color)
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Tags(client))
