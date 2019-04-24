"""
Fox Utilities > botcommands.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import discord
from discord.ext import commands
from ext.globals import *
from ext.checks import *


class BotCommands(commands.Cog):
    """
    BotCommands class

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
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        em.add_field(
            name="Server Count",
            value=f"I am currently connected to {len(self.client.guilds):,} servers."
        )
        await ctx.send(embed=em)

    @commands.command(
        name="usercount",
        aliases=["ucount", "membercount", "mcount", "users"],
        brief="Displays the number of users the bot sees.",
        usage=""
    )
    async def user_count(self, ctx):
        # Embed setup
        em = discord.Embed(color=COL_MESSAGE)
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
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        em.add_field(
            name="Pong!",
            value="Hello! Everything seems to be operational."
        )
        await ctx.send(embed=em)

    @commands.command(
        name="invite",
        brief="Invite this bot to your server.",
        usage=""
    )
    async def invite_bot(self, ctx):
        # Embed setup
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        em.add_field(
            name="Invite me!",
            value=f"[Invite link!]({BOT_INVITE})\n[Development server!]({BOT_DEVSERVER})"
        )
        await ctx.send(embed=em)

    @commands.command(
        name="privacy",
        brief="Information about our bot's privacy.",
        usage=""
    )
    async def privacy_information(self, ctx):
        # Embed setup
        em = discord.Embed(color=COL_MESSAGE)
        em.set_footer(text=f"Invoked by: {ctx.message.author.name}")

        # Command
        em.add_field(
            name="Privacy Information",
            value="Privacy is important to everyone, so we put a quick "
            "not-legally-rigorous overview of the data we have stored.\n\n"
            "**1)** If a command returns an error, the contents of the "
            "command will be logged for debug purposes. The name of the "
            "sender and the server it was sent on is **not** logged.\n\n"
            "**2)** We do not store data persistently! All logs are cleared "
            "on system reboot to ensure privacy.\n\n**3)** We do not, nor "
            "will we ever use the bot to access information not specified "
            "by this privacy notice.\n\n- The Fox Utilities Team")
        await ctx.author.send(embed=em)


# Extension setup
def setup(client):
    client.add_cog(BotCommands(client))
