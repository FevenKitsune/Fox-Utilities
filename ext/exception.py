"""
Fox Utilities > exception.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import discord
from ext.globals import *


async def on_command_error(ctx, error):
    try:
        # If CommandNotFound, fail silently
        if isinstance(error, discord.ext.commands.CommandNotFound):
            return

        # Generate formatted string
        exc = f"{type(error).__name__}: {error}"
        em = discord.Embed(
            title="Something isn't right...",
            description=f"`{exc}`",
            color=error_color
        )
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        await ctx.send(embed=em)
    except Exception as error:
        # If there is an issue with sending a message to the error channel, just ignore it.
        pass
