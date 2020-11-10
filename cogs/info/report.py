"""
Fox Utilities > info > report.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext.commands import Cog, command

from config.globals import message_color
from utils.generators import generate_footer


class Report(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @command(
        name="report",
        aliases=["bug", "error", "contact"],
        brief="Need to report a bug? Get information on how to do so here.",
        usage="",
        help="The report command can be used to get information and resources on where to report a bug. Bug reports "
             "are vital in ensuring Fox Utilities is the best it can be."
    )
    async def report_bug(self, ctx):
        """Gives the user information on how to report bugs they find."""
        em = Embed(
            title="Found a bug? :bee:",
            description="You can report bugs on the "
                        "[Fox Utilities issues](https://github.com/FevenKitsune/Fox-Utilities/issues) page on GitHub!",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Report(client))
