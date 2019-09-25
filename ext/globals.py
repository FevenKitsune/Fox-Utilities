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
COL_MESSAGE = 0xFFB600 # Color of the message embeds.
COL_ERROR = 0xFF0000 # Color of errors
DEV_ID = 276531286443556865 # ID of the developer (FevenKitsune)
BOT_KEY = os.environ['FU_KEY'] # Environment variable name
BOT_INVITE = "https://discordapp.com/oauth2/authorize?client_id=476166340328161280&scope=bot&permissions=1543761142" # Link to invite the bot
BOT_DEVSERVER = "https://discord.gg/ZVJasmz" # Link to the bot Development Server
BOT_SOURCE = "https://github.com/FevenKitsune/Fox-Utilities" # Link to the bot Github
BOT_DESCRIPTION = "Fox Utilities" # Discord.Bot description input

# Config Variables
BOT_PREFIX = "f." # Default prefix
BOT_DEFAULT_STATUS = "with code." # Default status

# Snipe Dict
snipe_db = {} # Active storage for snipes