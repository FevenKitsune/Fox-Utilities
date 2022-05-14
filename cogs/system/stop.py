from discord.ext.commands import Cog, slash_command, is_owner
from discord.commands import default_permissions

from config.globals import developer_guild_id


class Stop(Cog):
    category = "system"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="stop",
        description="Force stop the bot.",
        guild_ids=[developer_guild_id]
    )
    @default_permissions(administrator=True)
    @is_owner()
    async def stop_bot(self, ctx):
        """Force stops the bot."""
        exit()


def setup(client):
    client.add_cog(Stop(client))
