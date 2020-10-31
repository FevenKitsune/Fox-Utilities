"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Game
from discord.ext.commands import Cog, command

from utils.checks import is_developer


class ChangeBotStatus(Cog):
    category = "config"

    def __init__(self, client):
        self.client = client

    @command(
        name="cbs",
        brief="Change the bot status. Developer only command!",
        usage="string",
        hidden=True
    )
    @is_developer()
    async def change_status(self, ctx, args):
        """Change the game status of the bot."""
        await ctx.bot.change_presence(activity=Game(args))
        await ctx.send(args)


def setup(client):
    client.add_cog(ChangeBotStatus(client))
