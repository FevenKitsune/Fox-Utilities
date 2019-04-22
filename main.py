"""
Fox Utilities > main.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import discord
from discord.ext import commands
from ext.globals import *
import ext.foxexc as fex

import logging


# Object Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")
client = commands.Bot(description="Fox Utilities", command_prefix=BOT_PREFIX)

# Startup
@client.event
async def on_ready():
    logger.info("Setting client presence.")
    await client.change_presence(activity=discord.Game(BOT_DEFAULT_STATUS))
    logger.info("Fox Utilities is now ready!")

# Extension Loading
if __name__ == "__main__":

    # Remove default Help command.
    logger.info("Removing default help command.")
    client.remove_command("help")

    # Exception handler
    logger.info("Registering error handler.")
    client.add_listener(fex.on_command_error)

    # External cogs
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            logger.warning(f"Failed to load extension {extension}\n{exc}")
        else:
            logger.info(f"Loaded extension {extension}")

    # Start Bot
    logger.info("Starting client.")
    client.run(BOT_KEY)
