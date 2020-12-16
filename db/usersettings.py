from sqlalchemy import Column, Integer, JSON

from .base import Base


class UserSettings(Base):
    """ORM object for configuration settings. Settings are stored in a json file."""
    __tablename__ = 'usersettings'

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, index=True)
    data = Column(JSON)
