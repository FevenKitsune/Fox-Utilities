"""
Fox Utilities > exceptions.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class GuildBlocked(Error):
    """Called when a user has a guild blocked."""
    pass
