from discord import Embed, ApplicationContext
from discord.ext.commands import Cog, slash_command

from config.globals import message_color, developer_guild_id
from utils.generators import generate_footer


class Tags(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="tags",
        description="Information about permission tags.",
        guild_ids=[developer_guild_id]
    )
    async def tags(
            self,
            ctx: ApplicationContext
    ):
        """Gives the user information on permission tags, which allow non-admins to access admin commands."""
        em = Embed(
            title="Fox Utilities Permission Tags",
            description="Create a server role with the syntax `fox:name_of_command`. Assign any user to this role to "
                        "give them access to the named command. This will work with any command that requires "
                        "administrator permissions to access.",
            color=message_color)
        em.set_footer(text=generate_footer(ctx))

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Tags(client))
