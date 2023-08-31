from typing import Iterator, Any


def chunked(list: list, chunk_size: int) -> Iterator[list]:
    """Creates chunks from a list.

    Args:
        list (list): _description_
        chunk_size (int): _description_

    Raises:
        AttributeError: _description_

    Yields:
        Iterator[list]: _description_
    """
    if chunk_size <= 0:
        raise AttributeError(f"chunk_size can't be lower than 1. chunk_size was {chunk_size}")
    
    max_chunk_size = min(len(list)+1, chunk_size)

    for i in range(0, len(list), max_chunk_size):
        yield list[i:i + max_chunk_size]
