# TODO: This should probably be a JSON file...
import os

# Globally accessible list of extensions.
extensions = [
    "cogs.config.changebotstatus",
    "cogs.info.about",
    "cogs.info.privacy",
    "cogs.info.report",
    "cogs.stats.invites",
    "cogs.stats.members",
    "cogs.stats.stats",
    "cogs.system.pull",
    "cogs.system.reboot",
    "cogs.system.reload",
    "cogs.system.stop",
    "cogs.utils.testexception",
    "cogs.docs",
    "listeners.setdefaultstatus"
]

# Global variables
message_color = 0xFFB600  # Color of the message embeds.
error_color = 0xFF0000  # Color of errors
developer_id = 276531286443556865  # ID of the developer (FevenKitsune)
developer_guild_id = 385059238231408651
stable_client_id = 476166340328161280
testing_client_id = 728052111593570304

# Bot Links
bot_development_server = "https://discord.gg/ZVJasmz"
bot_source = "https://github.com/FevenKitsune/Fox-Utilities"
bot_wiki = "https://github.com/FevenKitsune/Fox-Utilities/wiki"

# Config Variables
bot_default_status = "with Slash Commands!"  # Default status
bot_description = "Fox Utilities is a utils bot covering a selection of niche functions to assist in server administration."  # Discord.Bot description input
bot_footer_prefix = "Invoked by: "
bot_member_page_size = 21

""" 
Bot Key
There are multiple options here, if you don't want to mess around with environment variables, then comment out the 
Environment Variable option and uncomment the key option. Make sure you keep your key safe! The developer will never
ask for your key.
"""
bot_key = os.environ['FOXKEY']  # Environment Variable option
# bot_key = "KEY_HERE"
