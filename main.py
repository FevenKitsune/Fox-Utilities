"""
Fox Utilities > main.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord.ext import commands
import logging
from db.engine import engine
from config.globals import *
from utility.checks import get_prefix
import utility.exception as exception

# Logging
logger = logging.getLogger("discord")  # Set up logger called "discord"
logger.setLevel(logging.INFO)  # Log all

# Client
client = commands.Bot(description=bot_description, command_prefix=get_prefix)

# Bot setup and loading
if __name__ == "__main__":
    # Remove default help command, this is replaced in coreutilities.
    logging.info("Removing default help command.")
    client.remove_command("help")

    # Register exception.py as the exception handler.
    logging.info("Registering error handler.")
    client.add_listener(exception.on_command_error)

    # External cogs
    for extension in extensions:
        try:
            client.load_extension(extension)  # Load all extensions
        except Exception as e:  # If load failed, post to log.
            exc = f"{type(e).__name__}: {e}"
            logger.warning(f"Failed to load extension {extension}\n{exc}")
        else:  # If load succeeded, post to log.
            logger.info(f"Loaded extension {extension}")

    # Start Bot
    logging.info("Starting client.")
    client.run(bot_key)  # Start server.
