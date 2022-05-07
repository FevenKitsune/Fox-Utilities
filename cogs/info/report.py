from discord import Embed, ApplicationContext
from discord.ext.commands import Cog, slash_command

from config.globals import message_color, developer_guild_id
from utils.generators import generate_footer


class Report(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="report",
        description="Need to report a bug? Get information on how to do so here."
    )
    async def report_bug(
            self,
            ctx: ApplicationContext
    ):
        """Gives the user information on how to report bugs they find."""
        em = Embed(
            title="Found a bug? :bee:",
            description="You can report bugs on the "
                        "[Fox Utilities issues](https://github.com/FevenKitsune/Fox-Utilities/issues) page on GitHub!",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Report(client))
