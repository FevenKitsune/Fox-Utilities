"""
Fox Utilities > info > invite.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color, bot_invite, bot_development_server, bot_source, bot_wiki
from utils.generators import generate_footer


class GuildMailRemoved(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @command(
        name="guildmailremoved",
        aliases=["guildmail", "msgrole", "mr", "msgr", "msgnorole", "mnr", "msgnr", "mail", "block", "unblock", "unblockall", "blocklist"],
        brief="Guild Mail has been removed.",
        usage="",
        help="A temporary command that replaces all of the commands that were previously in the Guild Mail module. "
             "This is to inform users that the Guild Mail module has been removed. We have determined that the "
             "Guild Mail module was in violation of Terms of Service due to its ability to enable users to mass-market "
             "and spam users. This sort of behavior is something we do not condone."
    )
    async def guild_mail_removed(self, ctx):
        """Sends information on the development server, the GitHub, and the invite link."""
        em = Embed(
            title="Guild Mail has been removed.",
            description=f"All Guild Mail commands have been removed from the bot. For more information, please see "
                        f"`f.help mail`",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(GuildMailRemoved(client))
