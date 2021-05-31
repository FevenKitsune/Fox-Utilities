from discord.ext.commands import Cog
from db.dictionaries import snipe_dictionary


class CaptureSnipe(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener("on_message")
    async def capture_snipe(self, message):
        for member in message.mentions:
            snipe_dictionary.update({
                f"{member.id}": {
                    f"{message.channel.id}": {
                        "author_id": str(message.author.id),
                        "content": str(message.content)
                    }
                }
            })


def setup(client):
    client.add_cog(CaptureSnipe(client))
