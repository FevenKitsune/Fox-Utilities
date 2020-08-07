"""
Fox Utilities > checks.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import discord
from discord.ext import commands
from config.globals import *


def is_admin():
    """Checks if author is a server administrator, or has the correct permission tags."""
    async def predicate(ctx):
        return (
                ctx.message.channel.permissions_for(
                    ctx.message.author).administrator
                # Permissions for dev.
                or (ctx.author.id == developer_id)
                or (discord.utils.get(ctx.author.roles, name=str(f"fox:{ctx.command.name}")))
        )
    return commands.check(predicate)


def is_developer():
    """Checks if author is the developer of this bot."""
    async def predicate(ctx):
        return ctx.author.id == developer_id
    return commands.check(predicate)
