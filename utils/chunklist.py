def chunklist(inlist: list, chunksize: int) -> list:
    """Splits a list into equal chunks determined by chunksize.

    Args:
        inlist: The list to chunk.
        chunksize: The number of elements in each chunk.

    Returns:
        Returns a list of lists, with each list containing chunksize number of elements each.
    """
    if not isinstance(inlist, list):
        raise TypeError

    def __chunkyield() -> list:
        # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
        for i in range(0, len(inlist), chunksize):
            yield inlist[i:i + chunksize]

    return list(__chunkyield())
