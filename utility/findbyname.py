"""
Fox Utilities > findbyname.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from discord.utils import find
from difflib import get_close_matches
from unicodedata import normalize


async def find_by_name(name, search_in):
    """Performs a fuzzy search with unicode-font conversions."""
    # found_name = process.extractOne(normalize("NFKC", name), [normalize("NFKC", item.name) for item in search_in])
    # TODO SET THIS BACK TO NORMAL
    found_name = get_close_matches(normalize("NFKC", name), [normalize("NFKC", item.name) for item in search_in], n=3, cutoff=0.0)
    # found_item = find(lambda m: normalize("NFKC", m.name) == found_name[0], search_in)
    found_item = [find(lambda m: normalize("NFKC", m.name) == found, search_in) for found in found_name]
    return found_item
