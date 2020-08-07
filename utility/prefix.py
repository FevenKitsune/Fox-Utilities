"""
Fox Utilities > prefix.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import discord
from config.globals import stable_client_id, testing_bot_prefix, testing_client_id, bot_prefix


async def get_default_prefix(bot):
    """Grabs the default prefix based on the branch version that is running. Allows testing and stable to coexist."""
    if bot.user.id == stable_client_id:
        return bot_prefix
    if bot.user.id == testing_client_id:
        return testing_bot_prefix
    else:
        raise UserWarning("Client ID does not match a valid branch configuration! Unable to return a default prefix.")


async def get_prefix(bot, message):
    """Checks if the bot has a configuration tag for the prefix. Otherwise, gets the default."""
    default_prefix = await get_default_prefix(bot)
    if isinstance(message.channel, discord.DMChannel):
        return default_prefix
    my_roles = [role.name for role in message.guild.me.roles]
    for role_name in my_roles:
        if role_name[:11] == "fox_prefix:":
            return role_name[11:]
    return default_prefix
