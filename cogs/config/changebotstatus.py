from discord import Game, ApplicationContext
from discord.commands import Option, default_permissions
from discord.ext.commands import Cog, slash_command, is_owner

from config.globals import developer_guild_id


class ChangeBotStatus(Cog):
    category = "config"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="cbs",
        description="Change the bot status. Developer only command!",
        guild_ids=[developer_guild_id]
    )
    @default_permissions(administrator=True)
    @is_owner()
    async def change_status(
            self,
            ctx: ApplicationContext,
            new_status: Option(str, description="New status for the bot.", required=True)
    ):
        """Change the game status of the bot.

        Args:
            ctx: ApplicationContext represents a Discord application command interaction context.
            new_status: Discord application command option to request string input from the user.
        """
        await self.client.change_presence(activity=Game(new_status))
        await ctx.respond(new_status)


def setup(client):
    client.add_cog(ChangeBotStatus(client))
