"""
Fox Utilities > generators.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from config.globals import developer_id, bot_footer_prefix


def generate_footer(ctx):
    """Generates the text at the bottom of every embed."""
    if ctx.author.id == developer_id:
        return f"{bot_footer_prefix}The Developer"
    return f"{bot_footer_prefix}{ctx.author.name}"


def generate_clean_guild_mail(ctx, sieved_args):
    """Parse string to remove the arguments from a guild mail string."""
    # split out the command.
    text = ctx.message.content.split(' ', 1)[1]

    # split out any flag arguments
    while text[0] == '-':
        text = text.split(' ', 1)[1]

    # figure out how the role is defined
    if len(ctx.message.role_mentions) < 1:
        # if no mentions, then message was matched with args. remove the match term from the string.
        text = text.replace(sieved_args, "", 1)
        # if there are two quotes at the start then remove those too.
        while text[0] and (text[0] == "'" or text[0] == "\""):
            if len(text) == 1:
                raise UserWarning("String decomposes into empty. No message given!")
            else:
                text = text[1:]
    else:
        # role was called with a mention, remove next mention using the same method to remove command.
        try:
            text = text.split(' ', 1)[1]
        except IndexError:
            raise UserWarning("String failed to split. No message given!")

    return text
