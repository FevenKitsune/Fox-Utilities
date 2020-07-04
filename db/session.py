"""
Fox Utilities > db > session.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from .engine import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()