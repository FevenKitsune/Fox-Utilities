from os import getcwd

from discord import Embed
from discord.ext.commands import Cog, command
from git import Repo

from config.globals import message_color
from utils.checks import is_developer
from utils.generators import generate_footer


class Pull(Cog):
    category = "system"

    def __init__(self, client):
        self.client = client

    @command(
        name="pull",
        brief="Git pull from GitHub repo.",
        hidden=True,
        usage=""
    )
    @is_developer()
    async def pull(self, ctx):
        """Pulls the latest version of the bot from Git"""
        # Find Git repository the bot is stored in
        repo = Repo(getcwd(), search_parent_directories=True)

        # Run git pull and post results into embed.
        em = Embed(
            title="Fox Utilities GitHub",
            description=f"```smalltalk\n{str(repo.git.pull())}\n```",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Pull(client))
