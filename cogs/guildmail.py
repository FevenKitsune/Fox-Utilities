"""
Fox Utilities > guildmail.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import discord
from discord.ext.commands import guild_only, dm_only
from utility.checks import *
from utility.findbyname import find_by_name
from config.globals import *
from utility.generators import generate_footer, generate_clean_guild_mail
from db import session, UserSettings
import json
from typing import List, Tuple
from discord import Status


class GuildMail(commands.Cog):
    """
    GuildMail class

    Guild mailing lists.
    """

    # Constructor
    def __init__(self, client):
        self.client = client

    @staticmethod
    def sieve_out_args(args):
        # Finds the first string in args that doesn't start with -
        for arg in args:
            if arg[0] != '-':
                return arg

    @staticmethod
    def extract_args(args):
        # Combines all flags from args
        flags = []
        for arg in args:
            if arg[:1] == '-' and len(arg) > 1:
                for flag in arg[1:]:
                    flags.append(flag)
            else:
                break
        return flags

    async def extract_mail_target(self, ctx, args, target_type) -> Tuple[List[discord.Member], discord.Role]:
        target = None
        role_data = None

        # Run different operations depending on what targets should be found.
        if target_type == discord.Role:
            # Target is a role. Message all members of a targeted role.
            if ctx.message.role_mentions:
                # Check if the targeted role is simply a mention.
                role_data = ctx.message.role_mentions[0]
                target = role_data.members
            else:
                # Filter out flag arguments and get the first non-flag argument.
                sieved_args = self.sieve_out_args(args)
                if sieved_args is not None:
                    # If a non-flag argument was found, try to find a matching role.
                    found_role = await find_by_name(sieved_args, ctx.message.guild.roles)
                    if found_role is not None:
                        role_data = found_role
                        target = role_data.members
        elif target_type == discord.Member:
            # Target is one member. Message that one member.
            target = None  # TODO: Add find_by_name for members too
        elif target_type == "nr":
            # Target is anyone with no roles
            target = []
            for member in ctx.message.guild.members:
                # Everyone has the @everyone role.
                if len(member.roles) <= 1:
                    target.append(member)
        return target, role_data

    async def extract_mail_filter(self, ctx, args, target) -> List[discord.Member]:
        """
        Filter Options:
        o = Online Only
        f = Offline Only
        """
        filters = self.extract_args(args)
        filtered_targets = []
        if not filters:
            filtered_targets = target

        # For each target, test the determined filters and add them to the filtered list if
        # they qualify for any of them. OR style filtering.

        for t in target:
            if 'o' in filters:
                if t.status != Status.offline:
                    filtered_targets.append(t)
            if 'f' in filters:
                if t.status == Status.offline:
                    filtered_targets.append(t)

        return filtered_targets

    async def extract_mail_intent(self, ctx, args, target_type) -> Tuple[List[discord.Member], discord.Role]:
        # Extracts flags and targets from mail.
        # Target type should be discord.Role, discord.Member, or a flag
        target, role = await self.extract_mail_target(ctx, args, target_type)

        if not target:
            raise UserWarning("Mail recipient could not be determined")
        # Run target list through filter.
        filtered_targets = await self.extract_mail_filter(ctx, args, target)
        # Return tuple containing targets and a targeted role if applicable.
        return filtered_targets, role

    async def mail_targets(self, ctx, targets, args, no_role=False) -> List[Tuple[discord.Member, Exception]]:
        # Send message to all targeted users.
        failed_messages = []
        for target in targets:
            try:
                # Query database to get member preferences.
                query = session.query(UserSettings)
                block_pref = query.filter(UserSettings.discord_id == target.id).first()

                # Ensure query returned something.
                if block_pref is not None:
                    # Check that their block list is populated.
                    if isinstance(block_pref.msgrole_block, str):
                        # Check if guild id is in block list.
                        if ctx.guild.id in json.loads(block_pref.msgrole_block):
                            # If so, raise exception.
                            raise UserWarning("This user has blocked guild mail.")

                # Send embedded guild mail.
                em_sent = discord.Embed(
                    title=f"Guild mail from {ctx.message.author.name}",
                    description=generate_clean_guild_mail(ctx, self.sieve_out_args(args) if not no_role else ''),
                    color=message_color
                )
                em_sent.set_footer(
                    text=f"Sent from: {ctx.guild.name}\n"
                         f"Use f.block {ctx.guild.id} if you no longer wish to receive messages from this guild.")
                em_sent.set_author(name=ctx.guild.name,
                                   icon_url=ctx.guild.icon_url)
                await target.send(embed=em_sent)
            except Exception as e:
                failed_messages.append((target, e))
        return failed_messages

    @commands.command(
        name="mailrole",
        aliases=["msgrole", "mr", "msgr"],
        brief="Mails all members of a tagged role.",
        usage="<-f/o> @role/\"role_name\""
    )
    @is_admin()
    @guild_only()
    async def mail_role(self, ctx, *args):
        # Determine list of members who should receive the message.
        targets, role = await self.extract_mail_intent(ctx, args, discord.Role)

        em = discord.Embed(
            title=":mega: Sending messages...",
            description=f"Sending {len(targets)} requested messages to {role.mention}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Send mail to determined targets and return a list of tuples containing any errors.
        failed_messages = await self.mail_targets(ctx, targets, args)
        # List of str for creating a formatted log of failed messages.
        failed_messages_log = []

        for member, error in failed_messages:
            failed_messages_log.append(f"Failed to send message to {member.name}: `{type(error).__name__}: {error}`")

        em.add_field(
            name="Failed Messages:",
            value='\n'.join(failed_messages_log) if failed_messages_log else "No failed messages detected."
        )
        # Send success/fail list back to guild.
        await ctx.send(embed=em)

    @commands.command(
        name="mailnorole",
        aliases=["msgnorole", "mnr", "msgnr"],
        brief="Mails all members that have no role.",
        usage="<-f/o>"
    )
    @is_admin()
    @guild_only()
    async def mail_no_role(self, ctx, *args):
        # Determine list of members who should receive the message.
        targets, role = await self.extract_mail_intent(ctx, args, "nr")
        em = discord.Embed(
            title=":mega: Sending messages...",
            description=f"Sending {len(targets)} requested messages.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Send mail to determined targets and return a list of tuples containing any errors.
        failed_messages = await self.mail_targets(ctx, targets, args, no_role=True)
        # List of str for creating a formatted log of failed messages.
        failed_messages_log = []

        for member, error in failed_messages:
            failed_messages_log.append(f"Failed to send message to {member.name}: `{type(error).__name__}: {error}`")

        em.add_field(
            name="Failed Messages:",
            value='\n'.join(failed_messages_log) if failed_messages_log else "No failed messages detected."
        )
        # Send success/fail list back to guild.
        await ctx.send(embed=em)

    @commands.command(
        name="block",
        brief="Blocks guild mail from a given guild.",
        usage="guild_id"
    )
    @dm_only()
    async def block_guild_mail(self, ctx, args):
        """Push block settings to database."""
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
            to_set = UserSettings(discord_id=ctx.message.author.id, msgrole_block=json.dumps([int(args)]))
            session.add(to_set)
            # Load block_list for posting in msg
            block_list = json.loads(to_set.msgrole_block)
        else:
            # Load in block_list and append requested guild.
            block_list = json.loads(to_set.msgrole_block)
            if int(args) in block_list:
                raise UserWarning("This guild is already blocked!")
            block_list.append(int(args))
            to_set.msgrole_block = json.dumps(block_list)

        session.commit()

        em = discord.Embed(
            title="Guild Mail Blocked",
            description=f"You have successfully blocked ID {args}",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Add fields for all guild's blocked.
        for guild_id in block_list:
            guild = self.client.get_guild(guild_id)
            em.add_field(
                name=f"{guild if guild else 'No longer in this guild.'}",
                value=f"`ID`: {guild_id}"
            )

        await ctx.send(embed=em)

    @commands.command(
        name="unblock",
        brief="Unblocks guild mail from a given guild.",
        usage="guild_id"
    )
    @dm_only()
    async def unblock_guild_mail(self, ctx, args):
        """Push unblock settings to database."""
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
            # Load in block_list and remove requested guild.
            block_list = json.loads(to_set.msgrole_block)
            if int(args) not in block_list:
                raise UserWarning("This guild is not blocked!")
            block_list.remove(int(args))
            to_set.msgrole_block = json.dumps(block_list)

        session.commit()

        em = discord.Embed(
            title="Guild Mail Unblocked",
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
        name="unblockall",
        brief="Erases all entries in server mail block list.",
        usage=""
    )
    @dm_only()
    async def unblock_all_guild_mail(self, ctx):
        """Delete all block_list entries from database."""
        query = session.query(UserSettings)
        to_set = query.filter(UserSettings.discord_id == ctx.message.author.id).first()

        if to_set is None:
            raise UserWarning("You have no guilds blocked!")
        else:
            to_set.msgrole_block = json.dumps([])

        session.commit()

        em = discord.Embed(
            title="Guild Mail Block List Purged",
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
    async def block_list_guild_mail(self, ctx):
        """List all block_list entries in database."""
        query = session.query(UserSettings)
        to_set = query.filter(UserSettings.discord_id == ctx.message.author.id).first()

        if to_set is None:
            raise UserWarning("You have no guilds blocked!")
        else:
            block_list = json.loads(to_set.msgrole_block)
            if not block_list:
                raise UserWarning("You have no guilds blocked!")

        em = discord.Embed(
            title="Guild Mail Block List",
            description=f"Guilds that you have blocked.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        for guild_id in block_list:
            guild = self.client.get_guild(guild_id)
            em.add_field(
                # Client can only see names of guilds it's in. Placeholder if it can't find the name.
                name=f"{guild if guild else 'No longer in this guild.'}",
                value=f"`ID`: {guild_id}"
            )

        await ctx.send(embed=em)


def setup(client):
    """Register class with client object."""
    client.add_cog(GuildMail(client))