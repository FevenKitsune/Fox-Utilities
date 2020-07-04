"""
Fox Utilities > membertools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord.ext.commands import guild_only, dm_only
from utility.checks import *
from config.globals import *
from fuzzywuzzy import process
from utility.generators import generate_footer
from foxlib.listtools import chunklist
from db import session, UserSettings
import unicodedata
import json


class MemberTools(commands.Cog):
    """
    MemberTools class

    Server administration and utility commands.
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
    @guild_only()
    async def member_list(self, ctx, *args):
        # Error checking
        if len(args) < 1:
            raise UserWarning(
                "You must mention or name one role for this command")

        if isinstance(ctx.message.channel, discord.DMChannel):
            raise UserWarning(
                "This command cannot be run in a DM channel!"
            )

        if len(ctx.message.role_mentions) < 1:  # If no mentions, do search.
            found_name = process.extractOne(
                unicodedata.normalize("NFKC", args[0]),
                [unicodedata.normalize("NFKC", role.name) for role in ctx.message.guild.roles]
            )  # This is terrible
            found_role = discord.utils.find(
                lambda m: unicodedata.normalize("NFKC", m.name) == found_name[0], ctx.message.guild.roles
            )  # Do search on guild roles...
            if found_role is None:  # If no roles found, error.
                raise UserWarning(
                    f"You must mention or name one role for this command.")
        else:
            found_role = ctx.message.role_mentions[0]

        # Page argument
        page_count = 1 if (len(args) < 2) else int(args[1])  # Default to 1st page

        # Generates a list containing n sized chunks of found_role.members
        chunked_members = chunklist(found_role.members, bot_member_page_size)

        # Embed setup
        em = discord.Embed(
            title=f":memo: {found_role.name} Member List",
            color=message_color
        )
        em.set_footer(
            text=f"Page {page_count}/{str(len(chunked_members))} "
                 f"| {generate_footer(ctx)}"
        )

        # Command logic
        try:
            for member in chunked_members[page_count - 1]:
                em.add_field(
                    name=f":top: {member.top_role}",
                    value=f"`User`: {member.mention}\n"
                          f"`Tag`: {member.name}#{member.discriminator}"
                )
        except IndexError:
            # Find cause of IndexError
            if page_count > len(chunked_members) and len(chunked_members) != 0:
                raise UserWarning("There are no more pages for this role!")
            elif len(chunked_members) == 0:
                raise UserWarning("This role has no members!")
            else:
                raise UserWarning("An unknown IndexError has occured!")
        await ctx.send(embed=em)

    @commands.command(
        name="msgrole",
        aliases=["mr", "msgr"],
        brief="Messages all members of a tagged role.",
        usage="@role"
    )
    @is_admin()
    @guild_only()
    async def message_role(self, ctx, *args):
        # Check if running in a DM channel
        if isinstance(ctx.message.channel, discord.DMChannel):
            raise UserWarning(
                "This command cannot be run in a DM channel!"
            )

        # Check if there's a mentioned role. If not, string match.
        if len(ctx.message.role_mentions) < 1:
            found_name = process.extractOne(
                unicodedata.normalize("NFKC", args[0]),
                [unicodedata.normalize("NFKC", role.name) for role in ctx.message.guild.roles]
            )
            found_role = discord.utils.find(
                lambda m: unicodedata.normalize("NFKC", m.name) == found_name[0], ctx.message.guild.roles
            )  # Do search on guild roles...
            if found_role is None:
                raise UserWarning("You must mention one role.")
        else:
            found_role = ctx.message.role_mentions[0]

        # If the set role has no members, throw error.
        if len(found_role.members) == 0:
            raise UserWarning("That role has no members!")

        # Embed setup
        em = discord.Embed(
            title=":mega: Sending messages...",
            description=f"Sending requested messages to {found_role.mention}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Command
        for member in found_role.members:
            try:
                # Command
                query = session.query(UserSettings)
                block_pref = query.filter(UserSettings.discord_id == member.id).first()
                if ctx.guild.id in block_pref.msgrole_block:
                    raise UserWarning("This user has blocked msgrole.")
                em_sent = discord.Embed(
                    title=f"Role message from {ctx.message.author.name}",
                    description=f"{ctx.message.clean_content}",
                    color=message_color
                )
                em_sent.set_footer(
                    text=f"Sent from: {ctx.guild.name} | Use f.block {ctx.guild.id} if you no longer wish to recieve messages from this guild.")
                em_sent.set_author(name=ctx.guild.name,
                                   icon_url=ctx.guild.icon_url)
                await member.send(embed=em_sent)
            except Exception as e:
                em.add_field(
                    name=f"Failed to send message to {member.name}",
                    value=f"`{type(e).__name__}: {e}`"
                )
                pass
        await ctx.send(embed=em)

    @commands.command(
        name="block",
        brief="Blocks msgrole from a given guild.",
        usage="guild_id"
    )
    @dm_only()
    async def block_msgrole(self, ctx, args):
        """Push block settings to database."""
        # Command
        query = session.query(UserSettings)
        to_set = query.filter(UserSettings.discord_id == ctx.message.author.id).first()

        if to_set is None:
            to_set = UserSettings(discord_id=ctx.message.author.id,
                                  msgrole_block=json.dumps([int(args)])
                                  )
            session.add(to_set)
        else:
            block_list = json.loads(to_set.msgrole_block)
            block_list.append(int(args))
            to_set.msgrole_block = json.dumps(block_list)

        session.commit()

        em = discord.Embed(
            title="Msgrole Blocked",
            description=f"You have successfully blocked ID {args}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        for guild_id in block_list:
            em.add_field(
                name=f"{self.client.get_guild(guild_id)}",
                value=f"`ID`: {guild_id}"
            )

        await ctx.send(embed=em)


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(MemberTools(client))
