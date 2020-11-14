"""
Fox Utilities > guildmail.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import json
from typing import List, Tuple

import discord
from discord import Status
from discord.ext.commands import Cog, command, guild_only, dm_only

from config.globals import message_color, testing_client_id, developer_id
from db import session, UserSettings
from utils.checks import is_admin
from utils.exceptions import GuildBlocked
from utils.findbyname import find_by_name
from utils.generators import generate_footer, generate_clean_guild_mail


class GuildMail(Cog):
    category = "guildmail"
    """
    GuildMail class

    Guild mailing lists.
    """

    # Constructor
    def __init__(self, client):
        self.client = client

    @staticmethod
    def sieve_out_args(args: List[str]) -> str:
        """
        Find the first argument that isn't a filter argument.

        :param args: A list of strings provided by discord.ext.commands.command
        :return: The first string in the list that doesn't start with -
        """
        # Finds the first string in args that doesn't start with -
        for arg in args:
            if arg[0] != '-':
                return arg

    @staticmethod
    def extract_args(args: List[str]) -> List[str]:
        """
        Get filter arguments from guild mail.

        :param args: A list of strings provided by discord.ext.commands.command
        :return: Every letter prefixed with a - before the first occurrence of a word that doesn't start with -

        Example:
        args = ["-a", "-b", "user", "-c"]
        return = ["a", "b"]
        -c is not returned to allow text prefixed with a - in the body of the message.
        """
        flags = []
        for arg in args:
            if arg[:1] == '-' and len(arg) > 1:
                for flag in arg[1:]:
                    flags.append(flag)
            else:
                break
        return flags

    async def extract_mail_target(
            self,
            ctx: discord.ext.commands.Context,
            args,
            target_type
    ) -> Tuple[List[discord.Member], discord.Role]:
        """
        Abstracts finding the desired list of recipients by taking a target type and performing the appropriate search.

        :param ctx: The discord.ext.commands.Context provided by discord.ext.commands.command.
        :param args: A list of strings provided by discord.ext.commands.command.
        :param target_type: Can be a string, discord.Role, or discord.Member.
        :return: A tuple containing the unfiltered list of targets. If target_type = discord.Role, the role identified
        will be returned as the second object in the tuple.
        """
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

    async def extract_mail_filter(
            self,
            ctx: discord.ext.commands.Context,
            args,
            target: List[discord.Member]
    ) -> List[discord.Member]:
        """
        Searches through a given list of members and picks ones based on arguments extracted from extract_args(args)

        :param ctx: The discord.ext.commands.Context provided by discord.ext.commands.command.
        :param args: A list of strings provided by discord.ext.commands.command.
        :param target: A list of pre-filtered targets.
        :return: A filtered list of targets.

        Filter Options:
        o = Include Online, Away, Do Not Disturb
        f = Include Offline
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

    async def extract_mail_intent(
            self,
            ctx: discord.ext.commands.Context,
            args,
            target_type
    ) -> Tuple[List[discord.Member], discord.Role]:
        """
        The interface for target extraction as well as filter handling.

        :param ctx: The discord.ext.commands.Context provided by discord.ext.commands.command.
        :param args: A list of strings provided by discord.ext.commands.command.
        :param target_type: Can be a string, discord.Role, or discord.Member.
        :return: A tuple containing the list of targets. If target_type = discord.Role, the role identified will be
        returned as the second object in the tuple.
        """
        target, role = await self.extract_mail_target(ctx, args, target_type)

        if not target:
            raise UserWarning("Mail recipient could not be determined")
        # Run target list through filter.
        filtered_targets = await self.extract_mail_filter(ctx, args, target)
        # Return tuple containing targets and a targeted role if applicable.
        return filtered_targets, role

    async def mail_targets(
            self,
            ctx: discord.ext.commands.Context,
            targets: List[discord.Member],
            args,
            no_role=False,
            test_message=False
    ) -> List[Tuple[discord.Member, Exception]]:
        """
        Generalized message sender for guild mail. Sends a guild mail to all targets.

        :param ctx: The discord.ext.commands.Context provided by discord.ext.commands.command.
        :param targets: A list of discord.Member to send the guildmail to.
        :param args: A list of strings provided by discord.ext.commands.command.
        :param no_role: Bypasses the removal of the role indicator. Otherwise will cause generate_clean_guildmail() to
        begin removing message text.
        :param test_message: Bypasses sending the final message. Good for testing.
        :return: A list of tuples containing who and why a message failed to send. Returns [] if there were no errors.
        """
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
                            raise GuildBlocked("Blocked")

                if not test_message:
                    # This is not a test. Send embedded guild mail.
                    em_sent = discord.Embed(
                        title=f"Guild mail from {ctx.message.author.name}",
                        description=generate_clean_guild_mail(
                            ctx,
                            self.sieve_out_args(args) if not no_role else ''
                        ),
                        color=message_color
                    )
                    em_sent.set_footer(
                        text=f"Sent from: {ctx.guild.name}\n"
                             f"Use f.block {ctx.guild.id} if you no longer wish to receive messages from this guild."
                    )
                    em_sent.set_author(
                        name=ctx.guild.name,
                        icon_url=ctx.guild.icon_url
                    )
                    await target.send(embed=em_sent)
                else:
                    # This is a test. Do not actually send messages.
                    if target.id == developer_id:
                        # Send a message only to the developer.
                        em_sent = discord.Embed(
                            title=f"Guild mail from {ctx.message.author.name}",
                            description=generate_clean_guild_mail(
                                ctx,
                                self.sieve_out_args(args) if not no_role else ''
                            ),
                            color=message_color
                        )
                        em_sent.set_footer(
                            text=f"Sent from: {ctx.guild.name}\n"
                                 f"Use f.block {ctx.guild.id} if you no longer wish to receive messages from this guild."
                        )
                        em_sent.set_author(
                            name=ctx.guild.name,
                            icon_url=ctx.guild.icon_url
                        )
                        await target.send(embed=em_sent)
            except Exception as e:
                failed_messages.append((target, e))
        return failed_messages

    @command(
        name="mailrole",
        aliases=["msgrole", "mr", "msgr"],
        brief="Mails all members of a given role.",
        usage="[-f] [-o] @role_tag/\"role_name\" message",
        help="The mailrole command can be used to send a message to all members of a given role.\n\n"
             "**Usage Information**\n"
             "*-f*: Filters members to message offline users.\n"
             "*-o*: Filters members to message online users.\n"
             "*@role_tag/\"role_name\"*: The desired role can be targeted by either tagging the role, or typing the "
             "name of the role in quotation marks. Roles using 𝓯𝓪𝓷𝓬𝔂 𝓽𝓮𝔁𝓽 will automatically be interpreted as "
             "standard QWERTY letters.\n"
             "*message*: The remainder of the command should contain the message you wish to send. All text before "
             "this point will be removed from the message."
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
        # Add wait field
        em.add_field(
            name=":timer: Please wait...",
            value="Please wait while I send the requested messages..."
        )
        awaiting_message = await ctx.send(embed=em)
        # Once the message is sent, clear the fields and begin processing...
        em.clear_fields()

        # Send mail to determined targets and return a list of tuples containing any errors.
        if self.client.user.id != testing_client_id:
            failed_messages = await self.mail_targets(ctx, targets, args)
        else:
            failed_messages = await self.mail_targets(ctx, targets, args, test_message=True)
        # List of str for creating a formatted log of failed messages.
        failed_messages_log = []

        for member, error in failed_messages:
            failed_messages_log.append(
                f":negative_squared_cross_mark: {member.name}: `{type(error).__name__}: {error}`")

        str_failed_messages = '\n'.join(failed_messages_log) if failed_messages_log else "No failed messages detected."
        if len(str_failed_messages) > 1024:
            str_failed_messages = f":negative_squared_cross_mark: Failed to send messages to " \
                                  f"{len(failed_messages_log)} members."
        em.add_field(
            name="Failed Messages:",
            value=str_failed_messages
        )
        # Edit existing message with success/fail list back to guild.
        await awaiting_message.edit(embed=em)

    @command(
        name="mailnorole",
        aliases=["msgnorole", "mnr", "msgnr", "mail"],
        brief="Mails all members that have no role.",
        usage="[-f] [-o] message",
        help="The mailnorole command can be used to send a message to all members that have no role.\n\n"
             "**Usage Information**\n"
             "*-f*: Filters members to message offline users.\n"
             "*-o*: Filters members to message online users.\n"
             "*message*: The remainder of the command should contain the message you wish to send. All text before "
             "this point will be removed from the message."
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
        # Add wait field
        em.add_field(
            name=":timer: Please wait...",
            value="Please wait while I send the requested messages..."
        )
        awaiting_message = await ctx.send(embed=em)
        # Once the message is sent, clear the fields and begin processing...
        em.clear_fields()

        # Send mail to determined targets and return a list of tuples containing any errors.
        if self.client.user.id != testing_client_id:
            failed_messages = await self.mail_targets(ctx, targets, args, no_role=True)
        else:
            failed_messages = await self.mail_targets(ctx, targets, args, no_role=True, test_message=True)
        # List of str for creating a formatted log of failed messages.
        failed_messages_log = []

        for member, error in failed_messages:
            failed_messages_log.append(
                f":negative_squared_cross_mark: {member.name}: `{type(error).__name__}: {error}`"
            )

        str_failed_messages = '\n'.join(failed_messages_log) if failed_messages_log else "No failed messages detected."
        if len(str_failed_messages) > 1024:
            str_failed_messages = f":negative_squared_cross_mark: Failed to send messages to " \
                                  f"{len(failed_messages_log)} members."
        em.add_field(
            name="Failed Messages:",
            value=str_failed_messages
        )
        # Send success/fail list back to guild.
        await awaiting_message.edit(embed=em)

    @command(
        name="block",
        brief="Blocks guild mail from a given guild.",
        usage="guild_id",
        help="The block command can be used to block a guild from sending you guild mail.\n\n"
             "**Usage Information**\n"
             "*guild_id*: The ID of the guild you wish to block. This can be found at the bottom of every guild mail."
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
            to_set = UserSettings(
                discord_id=ctx.message.author.id,
                msgrole_block=json.dumps([int(args)])
            )
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

    @command(
        name="unblock",
        brief="Unblocks guild mail from a given guild.",
        usage="guild_id",
        help="The unblock command can be used to unblock a guild from sending you guild mail.\n\n"
             "**Usage Information**\n"
             "*guild_id*: The ID of the guild you wish to unblock. This can be found using f.blocklist."
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

    @command(
        name="unblockall",
        brief="Erases all entries in server mail block list.",
        usage="",
        help="The unblockall command can be used to unblock all guilds from sending you guild mail."
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

    @command(
        name="blocklist",
        brief="Lists your current blocks.",
        usage="",
        help="The blocklist command can be used to see the name and ID of all guild's you've blocked."
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
