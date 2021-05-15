from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from db.dict import snipe_dict
from utils.generators import generate_footer


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
    async def cyrm(self, ctx):
        """Runs through a series of checks to ensure the bot can access the invoked channel."""
        em = Embed(color=message_color)
        em.set_footer(text=generate_footer(ctx))

        """
        Check 1: Can the bot see the command?
        True: If this command is invoked, then the bot can see the command. Continue to Check 2.
        """

        """
        Check 2: Check if the bot can write messages to the channel.
        True: Report success status in channel. End command.
        False: Report failure status to author. Continue to Check 3.
        """

        """
        Check 3: Check if the bot can write messages to author.
        True: Report failure status to author. End command.
        False: Attempt to report error with reactions. Continue to Check 4.
        """

        """
        Check 4: Check if the bot can react to invoked message.
        True: React with :fox: :sos:. End command.
        False: Impossible to report error. Command fail.
        """


def setup(client):
    client.add_cog(CYRM(client))
