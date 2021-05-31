import discord
from discord.ext import commands

import utils.exception as exception
import logging
from config.globals import bot_description, extensions, bot_key
from utils.prefix import get_prefix

# Configure logging
logging.basicConfig(level=logging.INFO)

# Declare system intents.
intents = discord.Intents.default()
intents.members = True

# Create discord.py Bot object.
client = commands.AutoShardedBot(description=bot_description, command_prefix=get_prefix, intents=intents)

# Bot setup and loading
if __name__ == "__main__":
    # Remove default help command, this is replaced in Core Utilities.
    logging.info("Removing default help command.")
    client.remove_command("help")

    # Register exception.py as the exception handler.
    logging.info("Registering error handler.")
    client.add_listener(exception.on_command_error)

    # External cogs
    for extension in extensions:
        try:
            # Load all extensions
            client.load_extension(extension)
        except Exception as e:
            # If load failed, post to log.
            exc = f"{type(e).__name__}: {e}"
            logging.warning(f"Failed to load extension {extension}\n{exc}")
        else:
            # If load succeeded, post to log.
            logging.info(f"Loaded extension {extension}")

    # Start server.
    logging.info("Starting client.")
    client.run(bot_key)
