"""
Fox Utilities > db > usersettings.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from sqlalchemy import Column, Integer, String
from .base import Base


class UserSettings(Base):
    """ORM object for configuration settings. Settings are stored in a json file."""
    __tablename__ = 'usersettings'

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, index=True)
    msgrole_block = Column(String)
    settings_json = Column(String)