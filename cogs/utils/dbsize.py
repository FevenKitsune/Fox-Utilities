"""
Fox Utilities > stats > usercount.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord.ext.commands import Cog, command

from db import session, UserSettings
from utils.checks import is_developer


class DbSize(Cog):
    category = "utils"

    def __init__(self, client):
        self.client = client

    @command(
        name="dbsize",
        aliases=["lendb"],
        brief="Check how many entries are in the database.",
        usage="",
        hidden=True
    )
    @is_developer()
    async def db_size(self, ctx):
        """Count the number of entries in the database."""
        query = session.query(UserSettings).all()
        await ctx.send(f"```{len(query)}```")


def setup(client):
    client.add_cog(DbSize(client))
