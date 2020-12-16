from discord.ext.commands import Cog, command

from utils.checks import is_developer


class Stop(Cog):
    category = "system"

    def __init__(self, client):
        self.client = client

    @command(
        name="stop",
        brief="Force stop the bot.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def stop_bot(self, ctx):
        """Force stops the bot."""
        exit()


def setup(client):
    client.add_cog(Stop(client))
