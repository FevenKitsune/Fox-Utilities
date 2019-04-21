"""
Fox Utilities
Author: Feven Kitsune <fevenkitsune@gmail.com>
Do not redistribute!
"""

# Imports
import discord
from discord.ext import commands
import logging
import time
from requests import get
import psutil
import sys
import os
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


# System Commands
class CoreUtilities:

    def __init__(self, client):
        self.client = client

    # Extension reload command
    @commands.command(
        name="reload",
        brief="Reload bot extensions. Developer command.",
        hidden=True,
        usage="")
    async def reload(self, ctx, *args):
        if not (ctx.author.id == 276531286443556865):
            raise UserWarning("You must be the developer to run this command!")

        em_reload = discord.Embed(color=COL_MESSAGE)
        em_reload.set_footer(text="Invoked by: The Developer")

        # Check if there are any extensions first.
        if len(extensions) == 0:
            logger.info("No extensions found")
            em_reload.add_field(name="Oh well.", value="Doesn't look like there are any extensions defined.")
            await ctx.send(embed=em_reload)
            return

        for extension in extensions:
            try:
                client.unload_extension(extension)
            except Exception as e:
                expt = f"{type(e).__name__}: {e}"
                em_reload.add_field(
                    name=f"{extension}",
                    value=f"Failed to unload extension {extension}\nException: {expt}")
            else:
                em_reload.add_field(
                    name=f"{extension}", 
                    value=f"Successfully unloaded extension {extension}")

        for extension in extensions:
            try:
                client.load_extension(extension)
            except Exception as e:
                expt = f"{type(e).__name__}: {e}"
                em_reload.add_field(
                    name=f"{extension}",
                    value=f"Failed to load extension {extension}\nException: {expt}")
            else:
                em_reload.add_field(
                    name=f"{extension}",
                    value=f"Successfully loaded extension {extension}")

        await ctx.send(embed=em_reload)

    # Reboot command
    @commands.command(
        name="reboot",
        brief="Reboot core bot. Developer command.",
        hidden=True,
        usage="")
    async def reboot(self, ctx):
        if not (ctx.author.id == 276531286443556865):
            raise UserWarning("You must be developer to run this command!")

        em_reboot = discord.Embed(color=COL_MESSAGE)
        em_reboot.set_footer(text="Invoked by: The Developer")

        em_reboot.add_field(
            name="Rebooting bot!",
            value="Please wait while the bot reboots...")

        await ctx.send(embed=em_reboot)

        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)

        python = sys.executable
        os.execl(python, python, *sys.argv)

    # Help command
    @commands.command(
        name="help",
        brief="Display this message.",
        usage="")
    async def help(self, ctx, *args):
        em_help = discord.Embed(color=COL_MESSAGE)
        em_help.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        for cmd in sorted(client.commands, key=lambda command: command.cog_name):
            if (cmd.hidden) and not (ctx.author.id == 276531286443556865):
                pass
            else:
                em_help.add_field(
                    name=f"{'#' if cmd.hidden else ''}`{cmd.cog_name}`> {cmd.name} {cmd.usage}",
                    value=cmd.brief,
                    inline=False)

        await ctx.author.send(embed=em_help)


# Extension Loading
if __name__ == "__main__":

    # Remove default Help command.
    logger.info("Removing default help command.")
    client.remove_command("help")

    # Exception handler
    logger.info("Registering error handler.")
    client.add_listener(fex.on_command_error)

    # Local cogs
    logger.info("Registering Core commands.")
    client.add_cog(CoreUtilities(client))

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
