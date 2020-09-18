"""
Fox Utilities > globals.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import os

# Globally accessible list of extensions.
extensions = [
    "cogs.coretools",
    "cogs.developertools",
    "cogs.guildmail",
    "cogs.help",
    "cogs.membertools",
    "cogs.bottools",
    "cogs.invitetools",
    "cogs.systemtools",
    "cogs.snipetools",
    "cogs.misctools"
]

# Global variables
message_color = 0xFFB600  # Color of the message embeds.
error_color = 0xFF0000  # Color of errors
developer_id = 276531286443556865  # ID of the developer (FevenKitsune)
stable_client_id = 476166340328161280
testing_client_id = 728052111593570304

# Bot Links
bot_invite = "https://discordapp.com/api/oauth2/authorize?client_id=476166340328161280&permissions=8&scope=bot"
bot_development_server = "https://discord.gg/ZVJasmz"
bot_source = "https://github.com/FevenKitsune/Fox-Utilities"
bot_wiki = "https://github.com/FevenKitsune/Fox-Utilities/wiki"

# Config Variables
bot_prefix = "f."  # Default prefix
testing_bot_prefix = "f!"
bot_default_status = "with code. | f.help"  # Default status
bot_description = "Fox Utilities is a utility bot covering a selection of niche functions to assist in server administration."  # Discord.Bot description input
bot_footer_prefix = "Invoked by: "
bot_member_page_size = 25

# Snipe Dict
snipe_db = {}  # Active storage for snipes

""" 
Bot Key
There are multiple options here, if you don't want to mess around with environment variables, then comment out the 
Environment Variable option and uncomment the key option. Make sure you keep your key safe! The developer will never
ask for your key.
"""
bot_key = os.environ['FU_KEY']  # Environment Variable option
# bot_key = "KEY_HERE"
