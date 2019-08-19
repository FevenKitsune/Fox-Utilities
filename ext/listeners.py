"""
Fox Utilities > listeners.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from main import client
from ext.checks import get_prefix

async def is_mentioned(message):
    if message.mentions is None or message.mentions[0] != client.user:
        return
    
    await message.channel.send(await get_prefix(client, message))