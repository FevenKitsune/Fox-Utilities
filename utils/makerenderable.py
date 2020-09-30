"""
foxlib > makerenderable.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a This work is licensed under a Creative Commons Attribution 4.0 International License.
"""


def make_renderable(data: str) -> str:
    """
    Modify a given string to allow it to display in Discord.

    :param data: String with formatting characters.
    :return: String with the appropriate escape characters to render string correctly.
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
