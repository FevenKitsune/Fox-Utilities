"""
Fox Utilities > main.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""


import discord
from discord.ext import commands

import db
import utils.exception as exception
from utils.log import logger
from config.globals import bot_description, extensions, bot_key
from utils.prefix import get_prefix

# Ensure database is created and up to date.
db.create_all()

# Declare system intents.
intents = discord.Intents.default()
intents.members = True

# Create discord.py Bot object.
client = commands.Bot(description=bot_description, command_prefix=get_prefix, intents=intents)

# Bot setup and loading
if __name__ == "__main__":
    # Remove default help command, this is replaced in Core Utilities.
    logger.info("Removing default help command.")
    client.remove_command("help")

    # Register exception.py as the exception handler.
    logger.info("Registering error handler.")
    client.add_listener(exception.on_command_error)

    # External cogs
    for extension in extensions:
        try:
            # Load all extensions
            client.load_extension(extension)
        except Exception as e:
            # If load failed, post to log.
            exc = f"{type(e).__name__}: {e}"
            logger.warning(f"Failed to load extension {extension}\n{exc}")
        else:
            # If load succeeded, post to log.
            logger.info(f"Loaded extension {extension}")

    # Start server.
    logger.info("Starting client.")
    client.run(bot_key)
