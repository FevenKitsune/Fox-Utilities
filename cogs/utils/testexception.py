"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

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
