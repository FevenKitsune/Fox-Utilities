import discord
from discord import Embed, Status, ApplicationContext
from discord.commands import Option
from discord.ext import pages
from discord.ext.commands import Cog, slash_command, guild_only
from discord.utils import find

from config.globals import message_color, bot_member_page_size
from utils.chunklist import chunklist
from utils.findbyname import find_and_rank
from utils.generators import generate_footer
from utils.makerenderable import make_renderable


def match_emoji(status: Status) -> str:
    """Matches a discord.Status object to an emoji that represents that status.

    Args:
        status: A discord.Status object to match.

    Returns:
        String containing a client tag for an emoji.
    """
    match status:
        case Status.online:
            return ":green_circle:"
        case Status.offline:
            return ":black_circle:"
        case Status.idle:
            return ":yellow_circle:"
        case Status.dnd:
            return ":red_circle:"
        case Status.streaming:
            return ":purple_circle:"
        case _:
            return ":question:"


async def get_roles(
        ctx: discord.AutocompleteContext
):
    """An AutocompleteContext to fuzzy match to a context's guild roles.

    Args:
        ctx: AutocompleteContext represents context for a slash command's option autocomplete.

    Returns:
        Returns a list of the top matched roles based on fuzzy matching.
    """
    return [ranking_tuple[0] for ranking_tuple in
            find_and_rank(ctx.value, [role.name for role in ctx.interaction.guild.roles])]


class Members(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="members",
        description="Lists all members in a mentioned role."
    )
    @guild_only()
    async def member_list(
            self,
            ctx: ApplicationContext,
            role_str: Option(
                str,
                name="role",
                description="Role to grab members from.",
                required=True,
                autocomplete=get_roles
            )
    ):
        """Post a formatted list of the members in a given role.

        Args:
            ctx: ApplicationContext represents a Discord application command interaction context.
            role_str: Discord slash command option. Matches a string to the roles of the guild using fuzzy matching.
        """
        # Find role from fuzzy-searched AutoComplete string
        role = find(lambda r: r.name == role_str, ctx.interaction.guild.roles)

        if not role:
            raise UserWarning(f"Could not find role \"{role_str}\"!")

        # Generates a list containing n sized chunks of found_role.members
        chunked_members = chunklist(role.members, bot_member_page_size)

        if not len(chunked_members):
            raise UserWarning("This role has no members!")

        member_pages = []
        for index, member_chunk in enumerate(chunked_members):
            page_generator = Embed(
                title=f":memo: {make_renderable(role.name)} Member List",
                color=message_color
            )
            page_generator.set_footer(
                text=f"{generate_footer(ctx)}"
            )
            for member in member_chunk:
                page_generator.add_field(name=f"{match_emoji(member.status)} {member}",
                                         value=f"`User` {member.mention}\n"
                                               f"`Tag` {make_renderable(member.top_role.name)}"
                                         )
            member_pages.append(page_generator)

        paginator = pages.Paginator(pages=member_pages)
        await paginator.respond(ctx.interaction, ephemeral=False)


def setup(client):
    client.add_cog(Members(client))
