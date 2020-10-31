"""
Fox Utilities > stats > invites.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord import Embed
from discord.ext.commands import Cog, command, guild_only

from config.globals import message_color
from utils.generators import generate_footer


class Invites(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @command(
        name="invites",
        aliases=["myinvites"],
        brief="Display your own or a mentioned user's server invites.",
        usage="[@user]",
        help="The invites command can be used to see how many invites a user has generated.\n\n"
             "**Usage Information**\n"
             "*@user*: A user can be targeted by tagging them. If no user is given, the sender will be used."
    )
    @guild_only()
    async def invites(self, ctx):
        """Get a list of invite codes and the number of uses for a given user."""
        # If no one was mentioned, assume author is target.
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.author

        em = Embed(
            title="**{}\'s Invites**".format(user.name),
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Iterate through the guild invites and parse invites by the targeted user.
        for inv in await ctx.message.guild.invites():
            if inv.inviter == user:
                time_formatter = "%b %-d, %Y at %-l:%M%p"
                em.add_field(
                    name="Invite code: ####{}".format(str(inv.code)[4:]),
                    value=f"Uses: {inv.uses}\nCreated at: {inv.created_at.strftime(time_formatter)}"
                )

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Invites(client))
