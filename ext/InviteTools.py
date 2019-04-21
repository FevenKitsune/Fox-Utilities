"""
Fox Utilities > InviteTools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
Do not redistribute!
"""

# Imports
from discord.ext import commands
import discord
import datetime

# Colors
COL_MESSAGE = 0xFFB600


# InviteTools extension class
class InviteTools(commands.Cog):

    # Constructor
    def __init__(self, client):
        self.client = client

    # My invite counts
    @commands.command(
        name="invites",
        aliases=["myinvites"],
        brief="Display your own or a mentioned user's server invites.",
        usage="@user")
    async def invites(self, ctx, *args):
        # Command setup
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.author
        # Embed setup
        em_invites = discord.Embed(title="**{}\'s Invites**".format(user.name), color=COL_MESSAGE)
        em_invites.set_footer(text="Invoked by: {}".format(ctx.author.name))
        # Command logic
        if not ctx.message.guild:
            raise UserWarning("This is a DM channel!")
        for inv in await ctx.message.guild.invites():
            if inv.inviter == user:
                em_invites.add_field(name="Invite code: \#\#\#\#{}".format(str(inv.code)[4:]), value="Uses: {}\nCreated at: {}".format(inv.uses, inv.created_at.strftime("%b %-d, %Y at %-l:%M%p")))
        # Send message
        await ctx.send(embed=em_invites)

# Extension setup
def setup(client):
    client.add_cog(InviteTools(client))
