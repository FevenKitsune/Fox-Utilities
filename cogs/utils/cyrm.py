from discord import Embed, Forbidden
from discord.ext.commands import Cog, command, guild_only

from config.globals import message_color, error_color
from utils.generators import generate_footer
from utils.log import logger


class CYRM(Cog):
    category = "utils"

    def __init__(self, client):
        self.client = client

    @command(
        name="cyrm",
        brief="A debugging command that verifies the bot has permission to send and receive in a given channel.",
        usage="",
        help=""
    )
    @guild_only()
    async def cyrm(self, ctx):
        """Runs through a series of checks to ensure the bot can access the invoked channel."""

        """
        Check 1: Can the bot see the command?
        True: If this command is invoked, then the bot can see the command. Continue to Check 2.
        """

        """
        Check 2: Check if the bot can write messages to the channel.
        True: Report success status in channel. End command.
        False: Report failure status to author. Continue to Check 3.
        """
        try:
            em = Embed(color=message_color)
            em.set_footer(text=generate_footer(ctx))
            em.add_field(
                name="Loud and Clear!",
                value="I can see and respond to commands in this channel."
            )
            await ctx.send(embed=em)
        except Forbidden:
            # Unable to send message to channel.
            pass
        else:
            # Able to send message to channel.
            return

        """
        Check 3: Check if the bot can write messages to author.
        True: Report failure status to author. End command.
        False: Attempt to report error with reactions. Continue to Check 4.
        """
        try:
            em = Embed(color=error_color)
            em.set_footer(text=generate_footer(ctx))
            em.add_field(
                name="I can't send messages!",
                value="I do not have permission to send messages in the invoked channel. "
                      "Check permissions or contact your server administrator!"
            )
            await ctx.author.send(embed=em)
        except Forbidden:
            # Unable to send error to message author.
            pass
        else:
            # Able to send error to message author.
            return

        """
        Check 4: Check if the bot can react to invoked message.
        True: React with :fox: :sos:. End command.
        False: Impossible to report error. Command fail.
        """
        try:
            await ctx.message.add_reaction("🦊")
            await ctx.message.add_reaction("🆘")
        except Forbidden:
            # No action possible.
            return
        else:
            # Error reaction success.
            return


def setup(client):
    client.add_cog(CYRM(client))
