"""
Fox Utilities > checks.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import discord
from discord.ext import commands


def is_admin(ctx):
    async def predicate(ctx):
        return (
            ctx.message.channel.permissions_for(ctx.message.author).administrator
            or (ctx.author.id == 276531286443556865)
        )
    return commands.check(predicate)
