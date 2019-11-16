"""
Fox Utilities > globals.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

# Imports
import os

# Globally accessible list of extensions.
extensions = [
    "ext.coretools",
    "ext.developertools",
    "ext.membertools",
    "ext.bottools",
    "ext.invitetools",
    "ext.systemtools",
    "ext.snipetools",
    "ext.misctools"
]

# Global variables
message_color = 0xFFB600  # Color of the message embeds.
error_color = 0xFF0000  # Color of errors
developer_id = 276531286443556865  # ID of the developer (FevenKitsune)
bot_key = os.environ['FU_KEY']  # Environment variable name

# Bot Links
bot_invite = "https://discordapp.com/api/oauth2/authorize?client_id=476166340328161280&permissions=8&scope=bot"
bot_development_server = "https://discord.gg/ZVJasmz"
bot_source = "https://github.com/FevenKitsune/Fox-Utilities"

# Config Variables
bot_prefix = "f."  # Default prefix
bot_default_status = "with code."  # Default status
bot_description = "Fox Utilities is a utility bot covering a selection of niche functions to assist in server administration."  # Discord.Bot description input

# Snipe Dict
snipe_db = {}  # Active storage for snipes
