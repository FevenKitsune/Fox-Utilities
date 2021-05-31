from discord import Game
from discord.ext.commands import Cog

from config.globals import bot_default_status
import logging


class DefaultStatus(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener("on_connect")
    async def set_default_status(self):
        """Executes once the bot has finished starting up."""
        logging.info(f"Setting client presence to: {bot_default_status}")
        # Set the bot status
        await self.client.change_presence(activity=Game(bot_default_status))
        logging.info("Default status has been set.")


def setup(client):
    client.add_cog(DefaultStatus(client))
