"""
Fox Utilities > membertools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord.ext.commands import guild_only, dm_only
from utility.checks import *
from utility.findbyname import find_by_name
from config.globals import *
from utility.generators import generate_footer
from foxlib.listtools import chunklist
from db import session, UserSettings
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

        if len(ctx.message.role_mentions) < 1:  # If no mentions, do search.
            found_role = await find_by_name(args[0], ctx.message.guild.roles)
            if found_role is None:  # If no roles found, error.
                raise UserWarning("You must mention or name one role for this command.")
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
        usage="@role/\"role_name\""
    )
    @is_admin()
    @guild_only()
    async def message_role(self, ctx, *args):
        # Check if there's a mentioned role. If not, string match.
        if len(ctx.message.role_mentions) < 1:
            found_role = await find_by_name(args[0], ctx.message.guild.roles)
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
                # Query database to get member preferences.
                query = session.query(UserSettings)
                block_pref = query.filter(UserSettings.discord_id == member.id).first()

                if block_pref is not None:  # Ensure query returned something.
                    if isinstance(block_pref.msgrole_block, str):  # Check that their blocklist is populated.
                        if ctx.guild.id in json.loads(block_pref.msgrole_block):  # Check if guild id is in blocklist.
                            raise UserWarning("This user has blocked msgrole.")  # If so, raise exception.

                # Send embedded msgrole.
                em_sent = discord.Embed(
                    title=f"Role message from {ctx.message.author.name}",
                    description=f"{ctx.message.clean_content}",
                    color=message_color
                )
                em_sent.set_footer(
                    text=f"Sent from: {ctx.guild.name}\n"
                         f"Use f.block {ctx.guild.id} if you no longer wish to receive messages from this guild.")
                em_sent.set_author(name=ctx.guild.name,
                                   icon_url=ctx.guild.icon_url)
                await member.send(embed=em_sent)
            except Exception as e:
                # If sending dm failed, add entry to list.
                em.add_field(
                    name=f"Failed to send message to {member.name}",
                    value=f"`{type(e).__name__}: {e}`"
                )
                pass
        # Send success/fail list back to guild.
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

        # Check that a valid ID was passed.
        try:
            int(args)
        except ValueError:
            raise UserWarning("ID given was not a valid ID.")

        if len(args) != 18:
            raise UserWarning("ID given is the incorrect length.")

        # If user is not in database, create new entry.
        if to_set is None:
            to_set = UserSettings(discord_id=ctx.message.author.id,
                                  msgrole_block=json.dumps([int(args)])
                                  )
            session.add(to_set)
        else:
            # Load in blocklist and append requested guild.
            block_list = json.loads(to_set.msgrole_block)
            if int(args) in block_list:
                raise UserWarning("This guild is already blocked!")
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
            guild = self.client.get_guild(guild_id)
            em.add_field(
                name=f"{guild if guild else 'No longer in this guild.'}",
                value=f"`ID`: {guild_id}"
            )

        await ctx.send(embed=em)

    @commands.command(
        name="unblock",
        brief="Unblocks msgrole from a given guild.",
        usage="guild_id"
    )
    @dm_only()
    async def unblock_msgrole(self, ctx, args):
        """Push unblock settings to database."""
        # Command
        query = session.query(UserSettings)
        to_set = query.filter(UserSettings.discord_id == ctx.message.author.id).first()

        # Check that a valid ID was passed.
        try:
            int(args)
        except ValueError:
            raise UserWarning("ID given was not a valid ID.")

        if len(args) != 18:
            raise UserWarning("ID given is the incorrect length.")

        # If user is not in database, ignore request.
        if to_set is None:
            raise UserWarning("You have no guilds blocked!")
        else:
            # Load in blocklist and remove requested guild.
            block_list = json.loads(to_set.msgrole_block)
            if int(args) not in block_list:
                raise UserWarning("This guild is not blocked!")
            block_list.remove(int(args))
            to_set.msgrole_block = json.dumps(block_list)

        session.commit()

        em = discord.Embed(
            title="Msgrole Unblocked",
            description=f"You have successfully unblocked ID {args}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        for guild_id in block_list:
            guild = self.client.get_guild(guild_id)
            em.add_field(
                name=f"{guild if guild else 'No longer in this guild.'}",
                value=f"`ID`: {guild_id}"
            )

        await ctx.send(embed=em)

    @commands.command(
        name="purgeblock",
        brief="Erases all entries in block list.",
        usage=""
    )
    @dm_only()
    async def purge_block_msgrole(self, ctx):
        """Push unblock settings to database."""
        # Command
        query = session.query(UserSettings)
        to_set = query.filter(UserSettings.discord_id == ctx.message.author.id).first()

        if to_set is None:
            raise UserWarning("You have no guilds blocked!")
        else:
            to_set.msgrole_block = json.dumps([])

        session.commit()

        em = discord.Embed(
            title="Msgrole Purged",
            description=f"You have successfully erased your block list.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)

    @commands.command(
        name="blocklist",
        brief="Lists your current blocks.",
        usage=""
    )
    @dm_only()
    async def block_list_msgrole(self, ctx):
        """Push unblock settings to database."""
        # Command
        query = session.query(UserSettings)
        to_set = query.filter(UserSettings.discord_id == ctx.message.author.id).first()

        if to_set is None:
            raise UserWarning("You have no guilds blocked!")
        else:
            block_list = json.loads(to_set.msgrole_block)
            if not block_list:
                raise UserWarning("You have no guilds blocked!")

        em = discord.Embed(
            title="Msgrole Block List",
            description=f"Guilds that you have blocked.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        for guild_id in block_list:
            guild = self.client.get_guild(guild_id)
            em.add_field(
                name=f"{guild if guild else 'No longer in this guild.'}",  # Client can only see names of guilds it's in
                value=f"`ID`: {guild_id}"
            )

        await ctx.send(embed=em)


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(MemberTools(client))
