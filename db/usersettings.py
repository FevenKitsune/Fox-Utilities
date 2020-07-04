from sqlalchemy import Column, Integer, String
from .base import Base


class UserSettings(Base):
    __tablename__ = 'usersettings'

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, index=True)
    msgrole_block = Column(String)
    settings_json = Column(String)