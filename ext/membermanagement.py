"""
Fox Utilities > membermanagement.py
Author: Feven Kitsune <fevenkitsune@gmail.com>

"""

# Imports
import discord
from discord.ext import commands
from ext.globals import *


class MemberManagement(commands.Cog):
    """
    MemberManagement class

    filler
    """

    # Constructor
    def __init__(self, client):
        self.client = client

    # Member command
    @commands.command(
        name="members",
        aliases=["member", "memlist"],
        brief="Lists all members in a mentioned role.",
        usage="@role/\"role_name\" <page #>")
    async def member_list(self, ctx, *args):
        # Error checking
        if len(args) < 1:
            raise UserWarning("You must mention or name one role for this command")
        if len(ctx.message.role_mentions) < 1:
            found_role = discord.utils.find(lambda m: m.name.lower() == str(args[0]).lower(), ctx.message.guild.roles)
            if found_role is None:
                raise UserWarning("You must mention or name one role for this command.")
        else:
            found_role = ctx.message.role_mentions[0]

        # Page argument
        page_count = 1 # Default to 1st page
        if (len(args) == 2):
            page_count = int(args[1])

        # Generates a list containing n sized chunks of found_role.members
        n = 25 # Page size
        chunked_members = [found_role.members[i * n:(i + 1) * n] for i in range((len(found_role.members) + n - 1) // n)] # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/

        # Embed setup
        em_member = discord.Embed(color=COL_MESSAGE)
        em_member.set_footer(text=f"Page {page_count}/{str(len(chunked_members))} | Invoked by: {ctx.author.name}")

        # Command logic
        for mem in chunked_members[page_count-1]:
            em_member.add_field(name=mem.top_role, value=f"`User`: {mem.mention}\n`Tag`:{mem.name}")

        # Send message
        await ctx.send(embed=em_member)

    # Message Role command
    @commands.command(
        name="msgrole",
        aliases=["mr", "msgr"],
        brief="Messages all members of a tagged role.",
        usage="@role")
    async def message_role(self, ctx, *args):
        # Error checking
        if not ctx.message.channel.permissions_for(ctx.message.author).administrator and not (ctx.author.id == 276531286443556865):
            raise UserWarning("You are not administrator!")

        # Check if there's a mentioned role. If not, string match.
        if len(ctx.message.role_mentions) < 1:
            found_role = discord.utils.find(lambda m: m.name.lower() == str(args[0]).lower(), ctx.message.guild.roles)
            if found_role is None:
                raise UserWarning("You must mention one role.")
        else:
            found_role = ctx.message.role_mentions[0]

        # If the set role has no members, throw error.
        if len(found_role.members) == 0:
            raise UserWarning("That role has no members!")

        # Embed setup
        em_msgrole = discord.Embed(color=COL_MESSAGE)
        em_msgrole.set_footer(text="Invoked by: {}".format(ctx.message.author.name))
        em_msgrole.add_field(name="Sending messages...", value="Sending requested messages!")

        # Command logic
        for mem in found_role.members:
            try:
                em_sentmsg = discord.Embed(color=COL_MESSAGE)
                em_sentmsg.set_footer(text="Sent from: {}".format(ctx.guild.name))
                em_sentmsg.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                em_sentmsg.add_field(name="Role message from {}".format(ctx.message.author.name), value="{}".format(ctx.message.clean_content))
                await mem.send(embed=em_sentmsg)
            except Exception as e:
                em_msgrole.add_field(name="Failed to send message to {}".format(mem.name), value="{}: {}".format(type(e).__name__, e))
                pass

        # Send message
        await ctx.send(embed=em_msgrole)


# Extension setup
def setup(client):
    client.add_cog(MemberManagement(client))
