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

        # error.__cause__ finds cause of CommandInvokeError, useful if exception thrown from inside command.
        if isinstance(error.__cause__, UserWarning):
            title = "There was a user warning while running the command..."
            # Generate formatted string
            exc = f"{type(error.__cause__).__name__}: {error.__cause__}"
        else:
            title = "There was an unknown error while running the command..."
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
