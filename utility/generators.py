"""
Fox Utilities > generators.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
"""


from config.globals import *

def generate_footer(ctx):
    if ctx.author.id == developer_id:
        return f"{bot_footer_prefix}The Developer"
    return f"{bot_footer_prefix}{ctx.author.name}"