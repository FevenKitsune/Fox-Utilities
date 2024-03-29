def make_renderable(data: str) -> str:
    """Modify a given string to allow it to display in Discord.

    Args:
        data: The string with markdown characters.

    Returns:
        The string with the appropriate escape characters to render string correctly.
    """
    markup_characters = {
        "_": "\\_",
        "*": "\\*",
        "~": "\\~",
        "|": "\\|"
    }

    for key, replacement in markup_characters.items():
        data = data.replace(key, replacement)

    return data
