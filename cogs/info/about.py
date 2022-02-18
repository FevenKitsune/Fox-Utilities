import discord
from discord import Embed
from discord.ext.commands import Cog, slash_command

from config.globals import message_color, bot_invite, bot_development_server, bot_source, bot_wiki
from utils.generators import generate_footer


class About(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="about",
        description="Information about this bot.",
    )
    async def about_bot(
            self,
            ctx: discord.ApplicationContext
    ):
        """Sends information on the development server and the GitHub."""
        em = Embed(
            title="About Fox Utilities!",
            description=f"[Development server!]({bot_development_server})\n"
                        f"[GitHub!]({bot_source})\n"
                        f"[Wiki!]({bot_wiki})",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(About(client))
