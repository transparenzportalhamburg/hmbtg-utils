import pytest
from hmbtg_utils import collections as c

TEST_LIST = [i for i in range(4)]


def test_chuncked_simple():
    result = list(c.chuncked(TEST_LIST, 2))

    assert [[0, 1], [2, 3]] == result


def test_chuncked_empty_list():
    result = list(c.chuncked([], 2))

    assert [] == result


def test_chuncked_list_and_chunck_same_size():
    result = list(c.chuncked(TEST_LIST, 4))

    assert [[0, 1, 2, 3]] == result


def test_chuncked_uneven_split():
    result = list(c.chuncked(TEST_LIST, 3))

    assert [[0, 1, 2], [3]] == result


def test_chuncked_chunk_bigger_than_list():
    result = list(c.chuncked(TEST_LIST, 5))

    assert [[0, 1, 2, 3]] == result


def test_chuncked_chunk_size_zero():
    exception_flag = False
    try:
        list(c.chuncked([], 0))
    except AttributeError as e:
        exception_flag = True

    assert exception_flag


def test_chuncked_chunk_size_negative():
    exception_flag = False
    try:
        result = list(c.chuncked([], -2))
    except AttributeError as e:
        exception_flag = True

    assert exception_flag
