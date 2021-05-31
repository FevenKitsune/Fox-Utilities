from discord import Embed
from discord.ext.commands import Cog, command, guild_only

from config.globals import message_color, bot_member_page_size
from utils.chunklist import chunklist
from utils.findbyname import find_by_name
from utils.generators import generate_footer
from utils.makerenderable import make_renderable


class Members(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @command(
        name="members",
        aliases=["member", "memlist"],
        brief="Lists all members in a mentioned role.",
        usage="@role/\"role_name\" [page #]",
        help="The members command can be used to retrieve a list of members within a given role.\n\n"
             "**Usage Information**\n"
             "*@role_tag/\"role_name\"*: The desired role can be targeted by either tagging the role, or typing the "
             "name of the role in quotation marks. Roles using 𝓯𝓪𝓷𝓬𝔂 𝓽𝓮𝔁𝓽 will automatically be interpreted as "
             "standard QWERTY letters.\n"
             "*page #*: Member lists containing more than 25 members will be split between multiple pages. To see "
             "more pages, specify which page number to view."
    )
    @guild_only()
    async def member_list(self, ctx, *args):
        """Post a formatted list of the members in a given role."""
        if len(args) < 1:
            raise UserWarning("You must mention or name one role for this command")

        # If no mentions, do search.
        if len(ctx.message.role_mentions) < 1:
            found_role = await find_by_name(args[0], ctx.message.guild.roles)
            # If no roles found, error.
            if found_role is None:
                raise UserWarning("You must mention or name one role for this command.")
        else:
            found_role = ctx.message.role_mentions[0]

        # Parse page argument. Defaults to the 1st page.
        page_count = 1 if (len(args) < 2) else int(args[1])

        # Generates a list containing n sized chunks of found_role.members
        chunked_members = chunklist(found_role.members, bot_member_page_size)

        em = Embed(
            title=f":memo: {make_renderable(found_role.name)} Member List",
            color=message_color
        )
        em.set_footer(
            text=f"Page {page_count}/{str(len(chunked_members))} | {generate_footer(ctx)}"
        )

        try:
            # Grabs the list of members in the given index and generates embed fields.
            for member in chunked_members[page_count - 1]:
                em.add_field(
                    name=f":high_brightness: {make_renderable(member.top_role.name)}",
                    value=f"`User` {member.mention}\n"
                          f"`Tag` {member.name}#{member.discriminator}"
                )
        except IndexError:
            # Find cause of IndexError
            if page_count > len(chunked_members) != 0:
                raise UserWarning("There are no more pages for this role!")
            elif len(chunked_members) == 0:
                raise UserWarning("This role has no members!")
            else:
                raise UserWarning("An unknown IndexError has occured!")
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Members(client))
