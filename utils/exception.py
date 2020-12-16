import discord
from utils.log import logger

from config.globals import error_color
from utils.generators import generate_footer


async def on_command_error(ctx, error):
    """Error handler, parses how message author should be notified about an error."""
    # If CommandNotFound, fail silently
    if isinstance(error, discord.ext.commands.CommandNotFound):
        return

    # error.__cause__ finds cause of CommandInvokeError, useful if exception thrown from inside command.
    if isinstance(error.__cause__, UserWarning):
        title = "There was a user warning while running the command!"
        # Generate formatted string
        exc = f"{type(error.__cause__).__name__}: {error.__cause__}"
    else:
        title = "There was an error while running the command!"
        # Generate formatted string
        exc = f"{type(error).__name__}: {error}"

    em = discord.Embed(
        title=title,
        description=f"`{exc}`",
        color=error_color
    )
    em.set_footer(text=generate_footer(ctx))
    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        # Was unable to send exception message, ignore.
        pass
    except discord.HTTPException as http_exception:
        # Was unable to send message due to HTTP error.
        logger.warn(
            f"{type(http_exception)} when sending an exception message. "
            f"{http_exception.status}: {http_exception.text}"
        )
        pass
