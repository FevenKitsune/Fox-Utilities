"""
Fox Utilities > log.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""

import logging

# Set up logger called "discord". Log level is set to INFO.
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
