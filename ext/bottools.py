"""
Fox Utilities > bottools.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
from ext.checks import *


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
        # Embed setup
        em = discord.Embed(
            title="Server Count",
            description=f"I am currently connected to {len(self.client.guilds):,} servers.",
            color=message_color
        )
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        await ctx.send(embed=em)

    @commands.command(
        name="usercount",
        aliases=["ucount", "membercount", "mcount", "users"],
        brief="Displays the number of users the bot sees.",
        usage=""
    )
    async def user_count(self, ctx):
        # Embed setup
        em = discord.Embed(color=message_color)
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        em.add_field(
            name="User Count",
            value=f"I can see a total of {len(ctx.bot.users):,} users!"
        )
        await ctx.send(embed=em)

    @commands.command(
        name="ping",
        aliases=["pong"],
        brief="A simple command to see if the bot is running.",
        usage=""
    )
    async def ping_bot(self, ctx):
        # Embed setup
        em = discord.Embed(
            title="Pong!",
            description="Hello! Everything seems to be operational.",
            color=message_color
        )
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        
        await ctx.send(embed=em)

    @commands.command(
        name="invite",
        aliases=["source", "code"],
        brief="Invite this bot to your server.",
        usage=""
    )
    async def invite_bot(self, ctx):
        # Embed setup
        em = discord.Embed(
            title="Invite me!",
            description=f"[Invite link!]({bot_invite})\n[Development server!]({bot_development_server})\n[GitHub!]({bot_source})",
            color=message_color
        )
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        
        await ctx.send(embed=em)

    @commands.command(
        name="privacy",
        brief="Information about our bot's privacy.",
        usage=""
    )
    async def privacy_information(self, ctx):
        # Embed setup
        em = discord.Embed(
            title="Privacy Information",
            description="Privacy is important to everyone, so this is a quick overview of the data we have stored.",
            color=message_color
        )
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        em.add_field(
            name="Error Logging",
            value="If a command returns an error, the contents of the command will be logged for debugging purposes. Neither the name of the sender nor the name of the server will be logged."
        )

        em.add_field(
            name="Data Persistence",
            value="Besides error logging, all data (Ex: snipe tool) is stored in memory, meaning it is wiped as soon as the bot stops running."
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


# Extension setup
def setup(client):
    """Register class with client object."""
    client.add_cog(BotTools(client))
