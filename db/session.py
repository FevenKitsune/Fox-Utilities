"""
Fox Utilities > db > session.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from sqlalchemy.orm import sessionmaker

from .engine import engine

Session = sessionmaker(bind=engine)

session = Session()