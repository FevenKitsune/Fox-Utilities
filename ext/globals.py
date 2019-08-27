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
COL_MESSAGE = 0xFFB600
COL_ERROR = 0xFF0000
DEV_ID = 276531286443556865
BOT_KEY = os.environ['FU_KEY']
BOT_INVITE = "https://discordapp.com/oauth2/authorize?client_id=476166340328161280&scope=bot&permissions=1543761142"
BOT_DEVSERVER = "https://discord.gg/ZVJasmz"
BOT_SOURCE = "https://github.com/FevenKitsune/Fox-Utilities"
BOT_DESCRIPTION = "Fox Utilities"

# Config Variables
BOT_PREFIX = "f."
BOT_DEFAULT_STATUS = "with code."

# Snipe Dict
snipe_db = {}