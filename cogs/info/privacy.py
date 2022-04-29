from discord import Embed, ApplicationContext
from discord.ext.commands import Cog, slash_command

from config.globals import message_color, developer_guild_id, bot_development_server
from utils.generators import generate_footer


class Privacy(Cog):
    category = "info"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="privacy",
        description="Information about our bots privacy.",
        guild_ids=[developer_guild_id]
    )
    async def privacy_information(
            self,
            ctx: ApplicationContext
    ):
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
            value="This bot currently does not contain any persistent data storage (databases, log files, etc)."
        )

        em.add_field(
            name="Misuse Policy",
            value="We do not, nor will we ever use the bot to access information not specified by this privacy notice."
        )

        em.add_field(
            name="Questions?",
            value=f"Feel free to ask questions in the [development server]({bot_development_server})!"
        )

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Privacy(client))
