"""
Fox Utilities > FoxUtils.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
Do not redistribute!
"""

# Imports
import discord
from discord.ext import commands
import logging
import time
from requests import get
import ext.foxexc as fex

# Constants
BOT_KEY = os.environ['FU_KEY']

# Object Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")
client = commands.Bot(description="Fox Utilities", command_prefix="f.")

logger.info("Test")

# Colors
COL_MESSAGE = 0xFFB600

# Extensions
extensions = [
    "ext.CoreUtilities",
    "ext.DeveloperTools",
    "ext.MemberManagement",
    "ext.BotCommands",
    "ext.InviteTools"
    ]

# Bot Status
default_status = "with code."

# Startup
@client.event
async def on_ready():
    logger.info("Setting client presence.")
    await client.change_presence(activity=discord.Game(default_status))
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
