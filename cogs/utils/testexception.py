from discord import ApplicationContext
from discord.ext.commands import Cog, slash_command, is_owner
from discord.commands import default_permissions

from config.globals import developer_guild_id


class TestException(Cog):
    category = "utils"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="except",
        description="Developer command. Throw a test error. Used to test the exception handler.",
        guild_ids=[developer_guild_id]
    )
    @default_permissions(administrator=True)
    @is_owner()
    async def test_exception(
            self,
            ctx: ApplicationContext
    ):
        """Raise a UserWarning exception to test the bots' ability to handle an error.

        Args:
            ctx: ApplicationContext represents a Discord application command interaction context.
        """
        raise UserWarning("Testing exception!")


def setup(client):
    client.add_cog(TestException(client))
