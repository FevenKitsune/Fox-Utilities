"""
Fox Utilities > info > privacy.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext import commands

from config.globals import message_color
from utils.generators import generate_footer


class Privacy(commands.Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="privacy",
        brief="Information about our bots privacy.",
        usage="",
        help="The privacy command can be used to get information on how we store and process user data."
    )
    async def privacy_information(self, ctx):
        """Sends information on what data this bot collects and how we use it."""
        em = Embed(
            title="Privacy Information",
            description="Privacy is important to everyone, so this is a quick overview of the data we have stored.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Command
        em.add_field(
            name="Error Logging",
            value="If a command returns an error, the contents of the command will be logged for debugging purposes. "
                  "Neither the name of the sender nor the name of the server will be logged."
        )

        em.add_field(
            name="Data Persistence",
            value="Snipe tool data: the contents of your last mention is stored in "
                  "memory, meaning it is wiped as soon as the bot stops running.\n"
                  "User preferences: the user ID and guild ID (where applicable) is stored in a local database."
        )

        em.add_field(
            name="Misuse Policy",
            value="We do not, nor will we ever use the bot to access information not specified by this privacy notice."
        )

        em.add_field(
            name="Questions?",
            value="Feel free to ask questions in the Development Server!"
        )

        await ctx.author.send(embed=em)


def setup(client):
    client.add_cog(Privacy(client))
