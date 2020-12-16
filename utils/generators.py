from config.globals import developer_id, bot_footer_prefix


def generate_footer(ctx):
    """Generates the text at the bottom of every embed."""
    if ctx.author.id == developer_id:
        return f"{bot_footer_prefix}The Developer"
    return f"{bot_footer_prefix}{ctx.author.name}"
