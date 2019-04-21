"""
Fox Utilities > foxexc.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
Do not redistribute!
"""

from discord.ext import commands
import discord
from ext.globals import *


async def on_command_error(ctx, error):
    try:
        exc = f"{type(error).__name__}: {error}"
        em_error = discord.Embed(color=COL_ERROR)
        em_error.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        em_error.add_field(name="That's not right...", value=f"`{exc}`")
        await ctx.send(embed=em_error)
    except Exception as error:
        pass
