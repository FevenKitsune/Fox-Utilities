"""
Fox Utilities > listeners > setdefaultstatus.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord.ext.commands import Cog

from db.dict import snipe_dict


class CaptureSnipe(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener("on_message")
    async def capture_snipe(self, message):
        for member in message.mentions:
            snipe_dict.update({
                f"{member.id}": {
                    f"{message.channel.id}": {
                        "author_id": str(message.author.id),
                        "content": str(message.content)
                    }
                }
            })


def setup(client):
    client.add_cog(CaptureSnipe(client))
