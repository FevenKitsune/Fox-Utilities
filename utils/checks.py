from discord.ext import commands

from config.globals import developer_id


def is_developer():
    """Checks if author is the developer of this bot."""

    async def predicate(ctx):
        return ctx.author.id == developer_id

    return commands.check(predicate)
