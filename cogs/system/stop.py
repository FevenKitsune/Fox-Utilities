"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

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
