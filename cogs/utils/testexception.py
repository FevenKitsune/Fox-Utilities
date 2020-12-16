from discord.ext.commands import Cog, command


class TestException(Cog):
    category = "utils"

    def __init__(self, client):
        self.client = client

    @command(
        name="except",
        brief="Throw a test error. Used to test the exception handler.",
        usage=""
    )
    async def test_exception(self, ctx):
        """Throw an exception to test the exception functions"""
        raise UserWarning("Testing exception!")


def setup(client):
    client.add_cog(TestException(client))
