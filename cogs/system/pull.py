from os import getcwd

from discord import Embed, ApplicationContext
from discord.ext.commands import Cog, slash_command, is_owner
from discord.commands import default_permissions
from git import Repo

from config.globals import message_color, developer_guild_id
from utils.generators import generate_footer


class Pull(Cog):
    category = "system"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="pull",
        description="Developer command. Git pull from GitHub repo.",
        guild_ids=[developer_guild_id]
    )
    @default_permissions(administrator=True)
    @is_owner()
    async def pull(
            self,
            ctx: ApplicationContext
    ):
        """Pulls the latest version of the bot from Git.

        Args:
            ctx: ApplicationContext represents a Discord application command interaction context.
        """
        # Find Git repository the bot is stored in
        repo = Repo(getcwd(), search_parent_directories=True)

        # Run git pull and post results into embed.
        em = Embed(
            title="Fox Utilities GitHub",
            description=f"```smalltalk\n{str(repo.git.pull())}\n```",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Pull(client))
