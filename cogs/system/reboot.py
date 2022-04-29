from os import getpid, close, execl
from sys import executable, argv

from discord import Embed, ApplicationContext
from discord.ext.commands import Cog, slash_command
from psutil import Process

from config.globals import message_color, developer_guild_id
from utils.checks import is_developer
from utils.generators import generate_footer


class Reboot(Cog):
    category = "system"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="reboot",
        description="Reboot core bot. Developer command.",
        hidden=True,
        guild_ids=[developer_guild_id]
    )
    @is_developer()
    async def reboot(
            self,
            ctx: ApplicationContext
    ):
        """Restart the bot on the system level."""
        em = Embed(
            title="Rebooting the bot!",
            description="Please wait while the bot reboots...",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        await ctx.respond(embed=em)

        # Get bot process
        p = Process(getpid())
        for handler in p.open_files() + p.connections():
            # Close all active connections and processes
            close(handler.fd)

        # Get python exec
        python = executable
        # Start python process
        execl(python, python, *argv)


def setup(client):
    client.add_cog(Reboot(client))
