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


class Help(Cog):
    """Help class
    Generates and outputs the help menu.
    TODO: Hide commands that the author does not have access to.
    """
    category = "info"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="help",
        description="Display a help menu."
    )
    async def help(
            self,
            ctx: ApplicationContext,
            command_help: Option(
                str,
                name="command",
                description="Optional command to retrieve information on",
                required=False,
                autocomplete=get_command
            )
    ):
        """Aggregates a list of commands registered with the bot and compiles it into a human-readable list.

        Args:
            ctx: ApplicationContext represents a Discord application command interaction context.
            command_help: Discord slash command option. Autocompletes to the closest match.
        """
        em = Embed(
            title="Fox Utilities Help Guide",
            description=bot_description,
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        if command_help and (search := command_help):
            # If there is an args list, assign variable search with the first value.
            # User is requesting information about a specific command.
            if found_command := self.client.get_application_command(search):
                # Search client for given command. Assign found_command with found value.
                # found_command will be None if no command is found.
                em.add_field(
                    name=f"`{found_command.cog.qualified_name}`"
                         f"\n{found_command.name}",
                    value=f"{found_command.description}"
                )
            else:
                # Variable command is None. Throw UserWarning.
                raise UserWarning(f"Command \"{command_help}\" was not found.")
        else:
            # User did not provide a specific command to read about. Generate an overview of available commands.
            # Dictionary structure that will contain cogs sorted by their class attribute "category"
            # categories["category_name"] = [list of cogs that belong to that category]
            categories = {}
            for cog in [self.client.get_cog(cog_name) for cog_name in sorted(self.client.cogs)]:
                # Get discord.ext.commands.Cog object in alphabetical order.
                if not hasattr(cog, "category"):
                    # If the Cog object doesn't have a category class attribute, ignore it.
                    # This is useful for cogs containing only helper functions.
                    continue

                if cog.category not in categories:
                    # Cog category hasn't been seen before, create new key in categories dictionary.
                    categories[cog.category] = [cog]
                else:
                    # Cog category has been seen before, append to existing list in categories dictionary.
                    categories[cog.category].append(cog)

            for key in list(categories):
                # Get each key in the categories' dictionary.
                command_list = []
                for cog in categories[key]:
                    # With each key, iterate through the cogs in that category and generate the appropriate embed field.
                    for cog_commands in cog.walk_commands():
                        """
                        if cog_commands.hidden and not (ctx.author.id == developer_id):
                            # Hide Developer commands.
                            continue
                        """
                        command_list.append(
                            f"`{cog_commands.name}` {cog_commands.description}"
                        )
                if command_list:
                    # There are commands in this category the user can access. Show this category.
                    em.add_field(name=key.capitalize(), value="\n".join(command_list), inline=False)
                else:
                    # The user has access to none of the commands in this category. Don't add an empty embed.
                    continue

        await ctx.respond(embed=em)


def setup(client):
    """Register class with client object."""
    client.add_cog(Help(client))
