def chunklist(inlist: list, chunksize: int) -> list:
    """Split a list into chucks of determined size.

    Keyword arguments:
    inList -- list to chunk
    chunkSize -- number of elements in each chunk
    """

    if not isinstance(inlist, list):
        raise TypeError

    def __chunkyield() -> list:
        # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
        for i in range(0, len(inlist), chunksize):
            yield inlist[i:i + chunksize]

    return list(__chunkyield())
