"""
Fox Utilities > membermanagement.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from ext.checks import *

from fuzzywuzzy import process


class MemberManagement(commands.Cog):
    """
    MemberManagement class

    Server administration commands and useful utilities.
    """

    # Constructor
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="members",
        aliases=["member", "memlist"],
        brief="Lists all members in a mentioned role.",
        usage="@role/\"role_name\" <page #>"
    )
    async def member_list(self, ctx, *args):
        # Error checking
        if len(args) < 1:
            raise UserWarning("You must mention or name one role for this command")

        if len(ctx.message.role_mentions) < 1:  # If no mentions, do search.
            found_name = process.extractOne(
                args[0], [role.name for role in ctx.message.guild.roles]
            )
            found_role = discord.utils.find(
                lambda m: m.name == found_name[0], ctx.message.guild.roles
            )  # Do search on guild roles.
            if found_role is None:  # If no roles found, error.
                raise UserWarning(f"You must mention or name one role for this command.")
        else:
            found_role = ctx.message.role_mentions[0]

        # Page argument
        page_count = 1  # Default to 1st page
        if (len(args) == 2):
            page_count = int(args[1])

        # Generates a list containing n sized chunks of found_role.members
        n = 25  # Page size
        chunked_members = [
            # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
            found_role.members[
            i * n:(i + 1) * n
            ] for i in range(
                (len(found_role.members) + n - 1) // n
            )
        ]

        # Embed setup
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(
            text=f"Page {page_count}/{str(len(chunked_members))} "
                 f"| Invoked by: {ctx.author.name}"
        )

        # Command logic
        try:
            for member in chunked_members[page_count - 1]:
                em.add_field(
                    name=member.top_role,
                    value=f"`User`: {member.mention}\n"
                          f"`Tag`: {member.name}#{member.discriminator}"
                )
        except IndexError:
            em.add_field(
                name="Uh-oh!",
                value="This role has no members!"
            )
        await ctx.send(embed=em)

    @commands.command(
        name="msgrole",
        aliases=["mr", "msgr"],
        brief="Messages all members of a tagged role.",
        usage="@role"
    )
    @is_admin()
    async def message_role(self, ctx, *args):
        # Check if there's a mentioned role. If not, string match.
        if len(ctx.message.role_mentions) < 1:
            found_name = process.extractOne(
                args[0], [role.name for role in ctx.message.guild.roles]
            )
            found_role = discord.utils.find(
                lambda m: m.name == found_name[0], ctx.message.guild.roles
            )  # Do search on guild roles.
            if found_role is None:
                raise UserWarning("You must mention one role.")
        else:
            found_role = ctx.message.role_mentions[0]

        # If the set role has no members, throw error.
        if len(found_role.members) == 0:
            raise UserWarning("That role has no members!")

        # Embed setup
        em = discord.Embed(
            title="Sending messages...",
            description="Sending requested messages!",
            color=COL_MESSAGE
        )
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        for member in found_role.members:
            try:
                em_sent = discord.Embed(
                    title=f"Role message from {ctx.message.author.name}",
                    description=f"{ctx.message.clean_content}",
                    color=COL_MESSAGE
                )
                em_sent.set_footer(text=f"Sent from: {ctx.guild.name}")
                em_sent.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                await member.send(embed=em_sent)
            except Exception as e:
                em.add_field(
                    name=f"Failed to send message to {member.name}",
                    value=f"`{type(e).__name__}: {e}`"
                )
                pass
        await ctx.send(embed=em)


# Extension setup
def setup(client):
    client.add_cog(MemberManagement(client))
