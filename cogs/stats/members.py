import discord
from discord import Embed
from discord.ext.commands import Cog, slash_command, guild_only
from discord.ext import pages
from discord.commands import Option

from config.globals import message_color, bot_member_page_size, developer_guild_id
from utils.chunklist import chunklist
from utils.findbyname import find_by_name
from utils.generators import generate_footer
from utils.makerenderable import make_renderable


def match_emoji(status: discord.Status) -> str:
    match status:
        case discord.Status.online:
            return ":green_circle:"
        case discord.Status.offline:
            return ":black_circle:"
        case discord.Status.idle:
            return ":yellow_circle:"
        case discord.Status.dnd:
            return ":red_circle:"
        case discord.Status.streaming:
            return ":purple_circle:"
        case _:
            return ":question:"


class Members(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="members",
        description="Lists all members in a mentioned role.",
        guild_ids=[developer_guild_id]
    )
    @guild_only()
    async def member_list(
            self,
            ctx: discord.ApplicationContext,
            role: Option(discord.Role, description="Role to grab members from.", required=True)
    ):
        """Post a formatted list of the members in a given role."""
        # Generates a list containing n sized chunks of found_role.members
        chunked_members = chunklist(role.members, bot_member_page_size)

        if not len(chunked_members):
            raise UserWarning("This role has no members!")

        member_pages = []
        for index, member_chunk in enumerate(chunked_members):
            page_generator = discord.Embed(
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
