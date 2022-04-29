from datetime import timedelta
from time import time

from discord import Embed, ApplicationContext
from discord.ext.commands import Cog, slash_command
from psutil import boot_time, virtual_memory, cpu_count, getloadavg

from config.globals import message_color
from utils.generators import generate_footer


class Stats(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="stats",
        description="Display full application statistics and diagnostics."
    )
    async def stats(
            self,
            ctx: ApplicationContext
    ):
        """Posts a full application statistics page"""

        em = Embed(
            title="Application Statistics",
            color=message_color
        )

        # Collect system uptime
        ut = time() - boot_time()

        # Collect memory statistics
        memory = virtual_memory()

        em.add_field(
            name=":desktop: System Information",
            value=f"`Uptime` {str(timedelta(seconds=int(ut)))}\n"
                  f"`Memory` {round(memory.used / 1000000000, 1)}/{round(memory.total / 1000000000, 1)} GB "
                  f"({round((memory.used / memory.total) * 100)}%)\n"
                  f"`Load (1/5/15)` {'/'.join([str(round(x / cpu_count() * 100, 2)) for x in getloadavg()])}",
            inline=False
        )

        em.add_field(
            name=":globe_with_meridians: API Information",
            value=f"`WebSocket Latency` {round(self.client.latency * 1000)}ms\n"
                  f"`Client ID` {self.client.user.id}\n"
                  f"`Shards` {len(self.client.shards)}\n"
                  f"`Users` {len(self.client.users):,}\n"
                  f"`Guilds` {len(self.client.guilds):,}",
            inline=False
        )

        em.set_footer(text=generate_footer(ctx))

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Stats(client))
