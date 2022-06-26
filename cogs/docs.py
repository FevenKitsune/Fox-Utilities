import discord
from discord import Embed, ApplicationContext, AutocompleteContext
from discord.commands import Option
from discord.ext.commands import Cog, slash_command

from config.globals import bot_description, message_color
from utils.generators import generate_footer


async def get_command(
        ctx: AutocompleteContext
):
    """An AutocompleteContext for matching to the bots' available commands.

    Args:
        ctx: AutocompleteContext represents context for a slash command's option autocomplete.

    Returns:
        Returns a list of commands that the user may want based on what has already been typed.
    """
    filtered_commands = filter(
        lambda command: command.guild_ids is None or ctx.interaction.guild_id in command.guild_ids,
        ctx.bot.walk_application_commands())
    return [command.name for command in filtered_commands]


class Docs(Cog):
    """Docs class
    Generates doc for provided command.
    """
    category = "info"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="docs",
        description="Detailed information about provided command."
    )
    async def docs(
            self,
            ctx: ApplicationContext,
            command_search: Option(
                str,
                name="command",
                description="Command to retrieve documentation on",
                required=True,
                autocomplete=get_command
            )
    ):
        """Aggregates a list of commands registered with the bot and compiles it into a human-readable list.

        Args:
            ctx: ApplicationContext represents a Discord application command interaction context.
            command_search: Discord slash command option. Autocompletes to the closest match.
        """
        em = Embed(
            title="Fox Utilities Help Guide",
            description=bot_description,
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        if found_command := self.client.get_application_command(command_search):
            em.add_field(
                name=f"`{found_command.cog.qualified_name}`"
                     f"\n{found_command.name}",
                value=f"{found_command.description}"
            )
        else:
            raise UserWarning(f"Command \"{found_command}\" was not found.")
        await ctx.respond(embed=em)


def setup(client):
    """Register class with client object."""
    client.add_cog(Docs(client))
