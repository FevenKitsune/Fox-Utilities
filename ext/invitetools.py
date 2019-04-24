"""
Fox Utilities > invitetools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import discord
from discord.ext import commands
from ext.globals import *
from ext.checks import *

import datetime


class InviteTools(commands.Cog):
    """
    InviteTools class

    Commands for tracking personal server invites.
    """

    # Constructor
    def __init__(self, client):
        self.client = client

    # My invite counts
    @commands.command(
        name="invites",
        aliases=["myinvites"],
        brief="Display your own or a mentioned user's server invites.",
        usage="@user"
    )
    async def invites(self, ctx, *args):
        # Command setup
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.author
        # Embed setup
        em = discord.Embed(title="**{}\'s Invites**".format(user.name), color=COL_MESSAGE)
        em.set_footer(text="Invoked by: {}".format(ctx.author.name))
        # Command logic
        if not ctx.message.guild:
            raise UserWarning("This is a DM channel!")
        for inv in await ctx.message.guild.invites():
            if inv.inviter == user:
                STRFTIME_FORMATTER = "%b %-d, %Y at %-l:%M%p"
                em.add_field(
                    name="Invite code: ####{}".format(str(inv.code)[4:]),
                    value=f"Uses: {inv.uses}\nCreated at: {inv.created_at.strftime(STRFTIME_FORMATTER)}"
                )
        # Send message
        await ctx.send(embed=em)


# Extension setup
def setup(client):
    client.add_cog(InviteTools(client))
