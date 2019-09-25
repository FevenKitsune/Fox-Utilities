"""
Fox Utilities > globals.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import os

# Globally accessible list of extensions.
extensions = [
    "ext.coreutilities",
    "ext.developertools",
    "ext.membermanagement",
    "ext.botcommands",
    "ext.invitetools",
    "ext.systemtools",
    "ext.snipetools"
]

# Global variables
message_color = 0xFFB600  # Color of the message embeds.
error_color = 0xFF0000  # Color of errors
developer_id = 276531286443556865  # ID of the developer (FevenKitsune)
bot_key = os.environ['FU_KEY']  # Environment variable name
# Link to invite the bot
bot_invite = "https://discordapp.com/oauth2/authorize?client_id=476166340328161280&scope=bot&permissions=1543761142"
# Link to the bot Development Server
bot_development_server = "https://discord.gg/ZVJasmz"
bot_source = "https://github.com/FevenKitsune/Fox-Utilities"  # Link to the bot Github
bot_description = "Fox Utilities"  # Discord.Bot description input

# Config Variables
bot_prefix = "f."  # Default prefix
bot_default_status = "with code."  # Default status

# Snipe Dict
snipe_db = {}  # Active storage for snipes
