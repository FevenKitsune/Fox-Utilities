"""
foxlib > __init__.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a This work is licensed under a Creative Commons Attribution 4.0 International License.
"""

# https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

__version__ = "0.0.2"
