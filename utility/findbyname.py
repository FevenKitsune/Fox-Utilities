"""
Fox Utilities > findbyname.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord.utils import find
from fuzzywuzzy.process import extract
from unicodedata import normalize


async def find_by_name(name, search_in):
    """Performs a fuzzy search with unicode-font conversions."""
    # found_name = process.extractOne(normalize("NFKC", name), [normalize("NFKC", item.name) for item in search_in])
    found_name = extract(normalize("NFKC", name), [normalize("NFKC", item.name) for item in search_in])
    # found_item = find(lambda m: normalize("NFKC", m.name) == found_name[0], search_in)
    found_items = [[find(lambda m: normalize("NFKC", m.name) == found[0], search_in), found[1]] for found in found_name]

    # Check for conflicts
    if (
            len(found_items) > 1
            and found_items[0][1] == found_items[1][1]
    ):
        raise UserWarning("Conflict!")

    return found_items
