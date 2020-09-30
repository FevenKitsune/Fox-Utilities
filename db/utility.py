"""
Fox Utilities > db > utils.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from .base import Base
from .engine import engine


def create_all():
    Base.metadata.create_all(engine)
