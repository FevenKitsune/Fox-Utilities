from discord import ApplicationContext
from discord.ext.commands import Cog, slash_command


class TestException(Cog):
    category = "utils"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="except",
        description="Throw a test error. Used to test the exception handler.",
        guild_ids=[developer_guild_id]
    )
    @default_permissions(administrator=True)
    @is_owner()
    async def test_exception(
            self,
            ctx: ApplicationContext
    ):
        """Throw an exception to test the exception functions"""
        raise UserWarning("Testing exception!")


def setup(client):
    client.add_cog(TestException(client))
