import discord
from discord import ApplicationContext

from discord.ext.commands import Cog, message_command


class CountCharacters(Cog):
    category = "stats"

    def __init__(self, client):
        self.client = client

    @message_command(
        name="Count Characters",
        description="A silly little test command."
    )
    async def count_characters(
            self,
            ctx: ApplicationContext,
            message: discord.Message
    ):
        """A message command that can be accessed via an in-application menu. Counts the number of unique characters
        and their occurrences.

        Args:
            ctx: ApplicationContext represents a Discord application command interaction context.
            message: The discord.Message the message_command() was invoked upon.

        Disabled by default, produces spam.
        """
        character_breakdown = {}
        for character in message.content:
            if str(character) not in character_breakdown:
                character_breakdown[str(character)] = 1
            else:
                character_breakdown[str(character)] += 1

        string_factory = "```\n"
        for key, value in character_breakdown.items():
            string_factory += f"{key}: {value}\n"
        string_factory += "```"

        await ctx.respond(string_factory)


def setup(client):
    client.add_cog(CountCharacters(client))
