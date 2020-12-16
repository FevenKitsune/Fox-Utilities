import discord
from discord.ext import commands

from config.globals import developer_id


def is_admin():
    """Checks if author is a server administrator, or has the correct permission tags."""

    async def predicate(ctx):
        return (
            # User is a server administrator.
            ctx.message.channel.permissions_for(ctx.message.author).administrator
            # User is a developer.
            or (ctx.author.id == developer_id)
            # User has a permission tag.
            or (discord.utils.get(ctx.author.roles, name=str(f"fox:{ctx.command.name}")))
        )

    return commands.check(predicate)


def is_developer():
    """Checks if author is the developer of this bot."""

    async def predicate(ctx):
        return ctx.author.id == developer_id

    return commands.check(predicate)
