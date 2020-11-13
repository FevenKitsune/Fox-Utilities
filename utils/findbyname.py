"""
Fox Utilities > findbyname.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from unicodedata import normalize

from discord.utils import find
from fuzzywuzzy.process import extract


def extract_conflicting_scores(extract_list):
    """Isolates objects in an array with matching fuzzywuzzy scores"""
    list_builder = []
    for i in extract_list:
        if i[1] == extract_list[0][1]:
            list_builder.append(i)

    return list_builder


def build_conflicting_scores_string(conflicting_scores):
    """Builds a printable string from a conflicting scores list"""
    string_builder = ""
    for i in conflicting_scores:
        string_builder += f"\n\"{i[0].name}\" match score: {i[1]}"

    return string_builder


async def find_by_name(name, search_in):
    """Performs a fuzzy search with unicode-font conversions."""
    found_name = extract(normalize("NFKC", name), [normalize("NFKC", item.name) for item in search_in])
    found_items = [[find(lambda m: normalize("NFKC", m.name) == found[0], search_in), found[1]] for found in found_name]

    # Check for match conflicts
    if (
            len(found_items) > 1
            and found_items[0][1] == found_items[1][1]
    ):
        # Create a warning string that tells the user what conflicts there are.
        raise UserWarning(
            f"Conflicting lookup found! Please provide more detail in your search.\n"
            f"Conflicts:{build_conflicting_scores_string(extract_conflicting_scores(found_items))}"
        )

    # If there is no conflict, return the highest ranked item
    return found_items[0][0]
