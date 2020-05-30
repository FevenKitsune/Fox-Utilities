"""
Fox Utilities > invitetools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from utility.checks import *
from utility.generators import generate_footer


class InviteTools(commands.Cog):
    """
    InviteTools class

    Commands for tracking personal server invites.
    """

    # Constructor
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="invites",
        aliases=["myinvites"],
        brief="Display your own or a mentioned user's server invites.",
        usage="@user"
    )
    async def invites(self, ctx, *args):
        # Command
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.author
        # Embed setup
        em = discord.Embed(
            title="**{}\'s Invites**".format(user.name),
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))
        # Command
        if not ctx.message.guild:
            raise UserWarning("This is a DM channel!")
        for inv in await ctx.message.guild.invites():
            if inv.inviter == user:
                time_formatter = "%b %-d, %Y at %-l:%M%p"
                em.add_field(
                    name="Invite code: ####{}".format(str(inv.code)[4:]),
                    value=f"Uses: {inv.uses}\nCreated at: {inv.created_at.strftime(time_formatter)}"
                )
        # Send message
        await ctx.send(embed=em)


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(InviteTools(client))
