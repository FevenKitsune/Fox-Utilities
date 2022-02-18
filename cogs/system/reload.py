import discord
from discord import Embed
from discord.ext.commands import Cog, slash_command

from config.globals import message_color, extensions, developer_guild_id
from utils.checks import is_developer
from utils.generators import generate_footer


class Reload(Cog):
    category = "system"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="reload",
        description="Reload bot extensions. Developer command.",
        guild_ids=[developer_guild_id]
    )
    @is_developer()
    async def reload(
            self,
            ctx: discord.ApplicationContext
    ):
        """Unload all discord.py cogs and load them back. Easier than a full reboot."""
        em = Embed(
            title="System Reload",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Stores which cogs passed and which cogs failed.
        success = []
        failed = []

        # Check for extensions first.
        if len(extensions) == 0:
            em.add_field(
                name="Oh well.",
                value="Doesn't look like there are any extensions defined."
            )
            await ctx.respond(embed=em)
            return
        for extension in extensions:
            try:
                # Unload extension
                self.client.unload_extension(extension)
            # Continue if unload failed.
            except Exception as e:
                pass
        for extension in extensions:
            try:
                # Load extension
                self.client.load_extension(extension)
            except Exception as e:
                # Post error to embed if load failed.
                expt = f"{type(e).__name__}: {e}"
                failed.append([extension, expt])
            else:
                # Post to embed if load succeeded.
                success.append(extension)

        em.add_field(
            name=":white_check_mark: Load Passed:",
            value='\n'.join([
                f"`{i}` PASS" for i in success
            ]) if success else "`None`"
        )

        em.add_field(
            name=":warning: Load Failed:",
            value='\n'.join([
                f"`{i[0]}` {i[1]}" for i in failed
            ]) if failed else "`None`"
        )
        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Reload(client))
