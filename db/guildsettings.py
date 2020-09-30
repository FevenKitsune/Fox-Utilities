"""
Fox Utilities > db > guildsettings.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from sqlalchemy import Column, Integer, JSON

from .base import Base


class GuildSettings(Base):
    """ORM object for configuration settings. Settings are stored in a json file."""
    __tablename__ = 'guildsettings'

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, index=True)
    data = Column(JSON)
