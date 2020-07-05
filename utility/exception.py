"""
Fox Utilities > exception.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import discord
from config.globals import *
from utility.generators import generate_footer


async def on_command_error(ctx, error):
    try:
        # If CommandNotFound, fail silently
        if isinstance(error, discord.ext.commands.CommandNotFound):
            return

        if isinstance(error, UserWarning):
            title = "There was a user error running the command..."
        else:
            title = "Something isn't right..."

        # Generate formatted string
        exc = f"{type(error).__name__}: {error}"
        em = discord.Embed(
            title=title,
            description=f"`{exc}`",
            color=error_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.send(embed=em)
    except Exception as error:
        # If there is an issue with sending a message to the error channel, just ignore it.
        pass
