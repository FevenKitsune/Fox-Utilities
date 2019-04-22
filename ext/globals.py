"""
Fox Utilities > globals.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import os

# Globally accessible list of extensions.
extensions = [
    "ext.coreutilities",
    "ext.developertools",
    "ext.membermanagement",
    "ext.botcommands",
    "ext.invitetools"
    ]

# Global variables
COL_MESSAGE = 0xFFB600
COL_ERROR = 0xFF0000
DEV_ID = 276531286443556865
BOT_KEY = os.environ['FU_KEY']

# Config Variables
BOT_PREFIX = "f."
BOT_DEFAULT_STATUS = "with code."