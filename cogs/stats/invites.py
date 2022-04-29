from discord import Embed, ApplicationContext, User
from discord.commands import Option
from discord.ext.commands import Cog, slash_command, guild_only
from config.globals import message_color, developer_guild_id
from utils.generators import generate_footer


class Invites(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @slash_command(
        name="invites",
        description="Display your own or a mentioned user's server invites.",
        guild_ids=[developer_guild_id]
    )
    @guild_only()
    async def invites(
            self,
            ctx: ApplicationContext,
            user: Option(User, description="Optional user to look up.", required=False)
    ):
        """Get a list of invite codes and the number of uses for a given user."""
        # If no one was mentioned, assume author is target.
        if not user:
            user = ctx.interaction.user

        em = Embed(
            title=f"{user.name}'s Invites",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Iterate through the guild invites and parse invites by the targeted user.
        for inv in await ctx.interaction.guild.invites():
            if inv.inviter == user:
                time_formatter = "%b %d, %Y at %I:%M%p"
                em.add_field(
                    name=f"Invite code: ####{str(inv.code)[4:]}",
                    value=f"`Uses` {inv.uses}\n"
                          f"`Created at` {inv.created_at.strftime(time_formatter)}"
                )

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Invites(client))
