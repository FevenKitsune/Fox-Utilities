"""
Fox Utilities > db > engine.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

from sqlalchemy import create_engine

# Create database in root folder outside of Git repository.
engine = create_engine('sqlite:////usr/src/app/db/db.db')
