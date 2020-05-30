"""
ArrayTools > chunklist.py
Author: Feven Kitsune <fevenkitsune@gmail.com>
This work is licensed under a This work is licensed under a Creative Commons Attribution 4.0 International License.
"""


def chunklist(inList: list, chunkSize: int):
    """Split a list into chucks of determined size.

    Keyword arguments:
    inList -- list to chunk
    chunkSize -- number of elements in each chunk
    """

    def __chunkyield(inList: list, chunkSize: int):
        # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
        for i in range(0, len(inList), chunkSize):
            yield inList[i:i+chunkSize]
    return list(__chunkyield(inList, chunkSize))
