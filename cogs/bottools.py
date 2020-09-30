"""
Fox Utilities > bottools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import discord
from discord.ext import commands

from config.globals import message_color, bot_invite, bot_development_server, bot_source, bot_wiki
from utils.generators import generate_footer


class BotTools(commands.Cog):
    """
    BotTools class

    Bot status and operation commands.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="servercount",
        aliases=["scount", "servers"],
        brief="Displays the number of servers the bot is currently connected to.",
        usage=""
    )
    async def server_count(self, ctx):
        """Counts the number of servers the bot is connected to."""
        em = discord.Embed(
            title="Server Count",
            description=f"I am currently connected to {len(self.client.guilds):,} servers.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)

    @commands.command(
        name="usercount",
        aliases=["ucount", "membercount", "mcount", "users", "memcount"],
        brief="Displays the number of users the bot sees.",
        usage=""
    )
    async def user_count(self, ctx):
        """Counts the number of unique users the bot is connected to."""
        em = discord.Embed(
            title="User Count",
            description=f"I can see a total of {len(ctx.bot.users):,} users!",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)

    @commands.command(
        name="ping",
        aliases=["pong"],
        brief="A simple command to see if the bot is running.",
        usage=""
    )
    async def ping_bot(self, ctx):
        """Basic call and response command"""
        em = discord.Embed(
            title="Pong!",
            description="Hello! Everything seems to be operational.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)

    @commands.command(
        name="invite",
        aliases=["source", "code"],
        brief="Invite this bot to your guild.",
        usage="",
        help="The invite command can be used to get information on how to invite the bot to your guild. It also "
             "contains links to the development server, GitHub page, and Wiki."
    )
    async def invite_bot(self, ctx):
        """Sends information on the development server, the GitHub, and the invite link."""
        em = discord.Embed(
            title="Invite me!",
            description=f"[Invite link!]({bot_invite})\n"
                        f"[Development server!]({bot_development_server})\n"
                        f"[GitHub!]({bot_source})\n"
                        f"[Wiki!]({bot_wiki})",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        await ctx.send(embed=em)

    @commands.command(
        name="privacy",
        brief="Information about our bots privacy.",
        usage="",
        help="The privacy command can be used to get information on how we store and process user data."
    )
    async def privacy_information(self, ctx):
        """Sends information on what data this bot collects and how we use it."""
        em = discord.Embed(
            title="Privacy Information",
            description="Privacy is important to everyone, so this is a quick overview of the data we have stored.",
            color=message_color
        )
        em.set_footer(text=generate_footer(ctx))

        # Command
        em.add_field(
            name="Error Logging",
            value="If a command returns an error, the contents of the command will be logged for debugging purposes. "
                  "Neither the name of the sender nor the name of the server will be logged."
        )

        em.add_field(
            name="Data Persistence",
            value="Snipe tool data: the contents of your last mention is stored in "
                  "memory, meaning it is wiped as soon as the bot stops running.\n"
                  "User preferences: the user ID and guild ID (where applicable) is stored in a local database."
        )

        em.add_field(
            name="Misuse Policy",
            value="We do not, nor will we ever use the bot to access information not specified by this privacy notice."
        )

        em.add_field(
            name="Questions?",
            value="Feel free to ask questions in the Development Server!"
        )

        await ctx.author.send(embed=em)


def setup(client):
    """Register class with client object."""
    client.add_cog(BotTools(client))
