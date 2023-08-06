from collections import Counter
from functools import wraps
from psutil import Process
from time import time
from typing import Dict, List, Literal, Set, Tuple, Union
import itertools
import logging

from .constants import SUPPORTED_ITEM_TYPES, SUPPORTED_KEY_TYPES


def default_checker(item_1: SUPPORTED_ITEM_TYPES, item_2: SUPPORTED_ITEM_TYPES) -> Tuple[bool, Union[float, int]]:
    f"""
    Check if two items match, and return a tuple with two values. The first value is a boolean indicating
    whether the items match or not. The second value is a float or an integer, representing a percentage match between 
    the items if they are strings and have a match percentage of more than 50%, or None otherwise.
    
    Args:
    - item_1 ({SUPPORTED_ITEM_TYPES}): An object of a supported type
    - item_2 ({SUPPORTED_ITEM_TYPES}): An object of a supported type
    
    Returns:
    A tuple containing a boolean indicating if the items match, and a float or integer percentage match if the items are
    strings and have a match percentage of more than 50%, or None otherwise.
    """

    if item_1 == item_2:
        return (True, 1)

    if type(item_1) is str and type(item_2) is str and (len(item_1) > 1 or len(item_2) > 1):
        char_counts, combined_chars = char_count([item_1, item_2])

        unconsumed_chars = 0
        total_chars = 0

        for char in combined_chars:
            count_in_item_1 = char_counts[0][char] if char in char_counts[0] else 0
            count_in_item_2 = char_counts[1][char] if char in char_counts[1] else 0

            combined_count = count_in_item_1 + count_in_item_2

            unconsumed_chars += abs(count_in_item_1 - count_in_item_2)
            total_chars += combined_count

        percentage_match = 1 - (unconsumed_chars / max(len(item_1), len(item_2)))
        if percentage_match > 0.5:
            return (True, round(percentage_match, 1))

    return (False, None)


def char_count(items: List[str]) -> Tuple[List[Dict[str, int]], Set[str]]:
    """
    Returns a dictionary mapping each character in a string to the number of times it appears.

    Args:
        s (str): Input string.

    Returns:
        dict: Dictionary mapping each character to the number of times it appears.
    """

    results = []
    combined_chars = set()

    for item in items:
        char_dict = {}
        for char, count in Counter(itertools.chain.from_iterable(item)).items():
            char_dict[char] = count
            combined_chars.add(char)

        results.append(char_dict)

    return (results, combined_chars)


def cleanup_string(s: str) -> str:
    """
    Cleans up a string by removing any leading or trailing white space characters.
    
    Args:
        s (str): The string to be cleaned up.
        
    Returns:
        str: A new string with no leading or trailing white space characters.
    """

    return s.strip()


def get_comparable_from_item(item: SUPPORTED_ITEM_TYPES, key: SUPPORTED_KEY_TYPES):
    if type(item) is dict:
        item = item[key]

    return item


def heap_sort(size: int, items: List[SUPPORTED_ITEM_TYPES], order: Union[Literal['ASC'], Literal['DESC']], key: SUPPORTED_KEY_TYPES = None) -> None:
    frequencies_and_indices = {}
    for index, item in enumerate(items):
        item = get_comparable_from_item(item, key)
        data = frequencies_and_indices.get(item, [0, []])
        data[1].append(index)
        data[0] += 1
        frequencies_and_indices[item] = data

    return sorted(
        frequencies_and_indices.items(),
        key=lambda x: x[1][0],
        reverse=(order == 'DESC')
    )[:size]


def log_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = Process()
        
        start_time = time()
        start_mem = process.memory_info().rss
        
        result = func(*args, **kwargs)
        
        end_time = time()
        end_mem = process.memory_info().rss
        
        elapsed_time = end_time - start_time
        consumed_mem = end_mem - start_mem
        
        logging.debug(f"{func.__name__} took {elapsed_time:.6f} seconds and consumed {consumed_mem / 1024:.6f} KB of memory.")
        return result


    return wrapper


def validate_input(items: List[SUPPORTED_ITEM_TYPES], key):
    if len(items) > 0 and type(items[0]) is dict and key is None:
        raise ValueError(
            "A `key` must be supplied if the `items` is a list of dictionaries."
        )

    return