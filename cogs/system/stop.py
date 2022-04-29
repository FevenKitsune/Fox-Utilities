from discord.ext.commands import Cog, slash_command

from config.globals import developer_guild_id
from utils.checks import is_developer


class Stop(Cog):
    category = "system"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="stop",
        description="Force stop the bot.",
        hidden=True,
        guild_ids=[developer_guild_id]
    )
    @is_developer()
    async def stop_bot(self, ctx):
        """Force stops the bot."""
        exit()


def setup(client):
    client.add_cog(Stop(client))
