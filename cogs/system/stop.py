from discord.ext.commands import Cog, slash_command

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
    @is_developer()
    async def stop_bot(self, ctx):
        """Force stops the bot."""
        exit()


def setup(client):
    client.add_cog(Stop(client))
