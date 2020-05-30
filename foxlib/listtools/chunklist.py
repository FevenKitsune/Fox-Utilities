"""
foxlib > ListTools > chunklist.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a This work is licensed under a Creative Commons Attribution 4.0 International License.
"""


def chunklist(inlist: list, chunksize: int):
    """Split a list into chucks of determined size.

    Keyword arguments:
    inList -- list to chunk
    chunkSize -- number of elements in each chunk
    """

    def __chunkyield():
        # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
        for i in range(0, len(inlist), chunksize):
            yield inlist[i:i + chunksize]

    return list(__chunkyield())
