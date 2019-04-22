"""
Fox Utilities > botcommands.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import discord
from discord.ext import commands
from ext.globals import *


class BotCommands(commands.Cog):
    """
    BotCommands class

    Bot status and operation commands.
    """

    # Constructor
    def __init__(self, client):
        self.client = client

    # Server Count
    @commands.command(
        name="servercount",
        aliases=["scount", "servers"],
        brief="Displays the number of servers the bot is currently connected to.",
        usage="")
    async def server_count(self, ctx):
        # Embed setup
        em_servercount = discord.Embed(color=COL_MESSAGE)
        em_servercount.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        # Command logic
        em_servercount.add_field(name="Server Count", value=f"I am currently connected to {len(self.client.guilds):,} servers.")
        # Send message
        await ctx.send(embed=em_servercount)

    # User Count
    @commands.command(
        name="usercount",
        aliases=["ucount", "memcount", "membercount", "users"],
        brief="Displays the number of users the bot sees.",
        usage="")
    async def user_count(self, ctx):
        # Embed setup
        em_usercount = discord.Embed(color=COL_MESSAGE)
        em_usercount.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        # Command logic
        em_usercount.add_field(name="User Count", value=f"I can see a total of {len(ctx.bot.users):,} users!")
        await ctx.send(embed=em_usercount)

    # Ping command
    @commands.command(
        name="ping",
        aliases=["pong"],
        brief="A simple command to see if the bot is running.",
        usage="")
    async def ping_bot(self, ctx):
        # Embed setup
        em_ping = discord.Embed(color=COL_MESSAGE)
        em_ping.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        em_ping.add_field(name="Pong!", value="Hello! Everything seems to be operational.")
        # Send message
        await ctx.send(embed=em_ping)

    # Invite command
    @commands.command(
        name="invite",
        brief="Invite this bot to your server.",
        usage="")
    async def invite_bot(self, ctx):
        # Embed setup
        em_invite = discord.Embed(color=COL_MESSAGE)
        em_invite.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        em_invite.add_field(name="Invite me!", value="[Invite link!](https://discordapp.com/oauth2/authorize?client_id=476166340328161280&scope=bot&permissions=1543761142)\n[Development server!](https://discord.gg/ZVJasmz)")
        # Send message
        await ctx.send(embed=em_invite)

    # Privacy Information command
    @commands.command(
        name="privacy",
        brief="Information about our bot's privacy.",
        usage="")
    async def privacy_information(self, ctx):
        # Embed setup
        em_privacy = discord.Embed(color=COL_MESSAGE)
        em_privacy.set_footer(text=f"Invoked by: {ctx.message.author.name}")
        em_privacy.add_field(name="Privacy Information", value="Privacy is important to everyone, so we put a quick not-legally-rigorous overview of the data we have stored.\n\n**1)** If a command returns an error, the contents of the command will be logged for debug purposes. The name of the sender and the server it was sent on is **not** logged.\n\n**2)** We do not store data persistently! All logs are cleared on system reboot to ensure privacy.\n\n**3)** We do not, nor will we ever use the bot to access information not specified by this privacy notice.\n\n- The FoxUtils Team")
        # Send message
        await ctx.author.send(embed=em_privacy)


# Extension setup
def setup(client):
    client.add_cog(BotCommands(client))
