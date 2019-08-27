"""
Fox Utilities > checks.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import discord
from discord.ext import commands
from ext.globals import *


def is_admin():
    async def predicate(ctx):
        return (
                ctx.message.channel.permissions_for(ctx.message.author).administrator
                or (ctx.author.id == DEV_ID)  # Permissions for dev.
                or (discord.utils.get(ctx.author.roles, name=str(f"fox:{ctx.command.name}")))
        )

    return commands.check(predicate)


def is_developer():
    async def predicate(ctx):
        return (
                ctx.author.id == DEV_ID
        )

    return commands.check(predicate)

async def get_prefix(bot, message):
        my_roles = [role.name for role in message.guild.me.roles]
        for role_name in my_roles:
                if role_name[:11] == "fox_prefix:":
                        return role_name[11:]
        return BOT_PREFIX