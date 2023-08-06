from typing import List, Optional

from .constants import SUPPORTED_KEY_TYPES, SUPPORTED_ITEM_TYPES
from .models import Result
from .utils import get_comparable_from_item, validate_input, cleanup_string, default_checker, heap_sort, log_performance


@log_performance
def binary_search(term: SUPPORTED_ITEM_TYPES, items: List[SUPPORTED_ITEM_TYPES], key: SUPPORTED_KEY_TYPES=None) -> Optional[Result]:
    """
    Performs a binary search on a list of integers to find a target value.

    Args:
        term (SUPPORTED_ITEM_TYPES): The value to search for.
        items (List[SUPPORTED_ITEM_TYPES]): A list of items to search through.
        key (SUPPORTED_KEY_TYPES, optional): A key to extract a comparable value from each item in the list.
                                              Defaults to None.

    Returns:
        Optional[Result, None]: A Result object that contains the search result.
                                Returns None if the target value is not found.

    Raises:
        TypeError: If the list of items is empty or if the target value is not comparable.

    Examples:
        >>> binary_search(term='a', items=['a', 'b', 'c'])
        {'confidence': 1, 'index': 0, 'value': 'a'}
        >>> binary_search(term=5, items=[1, 5, 10, 15])
        {'confidence': 1, 'index': 1, 'value': 5}
        >>> binary_search(
            term='Alex',
            items=[{'name': 'Alex'}, {'name': 'Mike'}, {'name': 'John'}],
            key='name'
        )
        {'confidence': 1, 'index': 0, 'value': 'Ade'}
    """

    validate_input(items, key)

    left, right = 0, len(items) - 1

    while left <= right:
        mid = (left + right) // 2

        item = get_comparable_from_item(items[mid], key)

        if item == term:
            return Result(confidence=1, index=mid, value=item)
        elif item > term:
            right = mid - 1
        else:
            left = mid + 1

    return None


@log_performance
def fuzzy_search(term: SUPPORTED_ITEM_TYPES, items: List[SUPPORTED_ITEM_TYPES], key: SUPPORTED_KEY_TYPES=None) -> List[Result]:
    """
    Searches a list of items for a given search term and returns a list of matching results.

    Args:
        term (SUPPORTED_ITEM_TYPES): The search term to match against items in the list.
        items (List[SUPPORTED_ITEM_TYPES]): The list of items to search.
        key (SUPPORTED_KEY_TYPES, optional): A key to extract a comparable value from each item in the list.
                                              Defaults to None.

    Returns:
        List[Result]: A list of Result objects representing the search results. 
                      Returns an empty list if no matches are found.

    Raises:
        TypeError: If the list of items is empty.

    Examples:
        >>> fuzzy_search("app", ["app", "apps", "hello", "world"])
        [
            {'confidence': 1, 'index': 0, 'value': 'app'},
            {'confidence': 0.8, 'index': 1, 'value': 'apps'}
        ]
        >>> fuzzy_search(
            term='Alex',
            items=[{'name': 'Alex'}, {'name': 'Mike'}, {'name': 'John'}],
            key='name'
        )
        [{'confidence': 1, 'index': 0, 'value': 'Alex'}]
    """

    validate_input(items, key)

    results = []

    for index in range(len(items)):
        item = items[index]

        if type(item) is str:
            item = cleanup_string(item)

        item = get_comparable_from_item(item, key)

        match = default_checker(item, term)
        if match[0]:
            results.append(Result(index=index, value=item, confidence=match[1]))

    results.sort(key=lambda x: x['confidence'])

    return results


@log_performance
def natural_language_search(raw_input: str, items: List[SUPPORTED_KEY_TYPES], key: SUPPORTED_KEY_TYPES=None):
    raise NotImplementedError


@log_performance
def regex_search(regex_pattern: str, items: List[SUPPORTED_KEY_TYPES], key: SUPPORTED_KEY_TYPES=None):
    raise NotImplementedError


@log_performance
def search_for_least_frequent_items(size: int, items: List[SUPPORTED_ITEM_TYPES], key: SUPPORTED_KEY_TYPES=None):
    """
    Finds the k least frequent item(s) in a list.

    Args:
        size (int): The number of least frequent items to return.
        items (List[SUPPORTED_ITEM_TYPES]): A list of items to search through.
        key (SUPPORTED_KEY_TYPES, optional): A key used to extract a comparable value from each item in the list.

    Returns:
        results (List[Result]): A list of the least frequent item(s), represented as a Result object containing the item, its index in the original list, and a confidence score of 1.

    Examples:
        >>> items = [1, 2, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7]
        >>> size = 2
        >>> search_for_least_frequent_items(size, items)
        [
            {'confidence': 1, 'index': [0], 'value': 1},
            {'confidence': 1, 'index': [2, 3], 'value': 3}
        ]
    """

    validate_input(items, key)

    results = []
    for item, (_, indices) in heap_sort(size, items, 'ASC', key):
        results.append(Result(confidence=1, value=item, index=indices))
        
    return results


@log_performance
def search_for_most_frequent_items(size: int, items: List[SUPPORTED_ITEM_TYPES], key: SUPPORTED_KEY_TYPES=None):
    """
    Finds the k most frequent item(s) in a list.

    Args:
        size (int): The number of most frequent items to return.
        items (List[SUPPORTED_ITEM_TYPES]): A list of items.
        key (SUPPORTED_KEY_TYPES, optional): A function used to extract a comparable value from each item in the list.

    Returns:
        results (List[Result]): A list of the most frequent item(s).

    Examples:
        >>> search_for_most_frequent_items(2, [1, 2, 2, 3, 3, 3])
        [
            {'confidence': 1, 'index': [3, 4, 5], 'value': 3},
            {'confidence': 1, 'index': [1, 2], 'value': 2}
        ]
    """

    validate_input(items, key)

    results = []
    for item, (_, indices) in heap_sort(size, items, 'DESC', key):
        results.append(Result(confidence=1, value=item, index=indices))
        
    return results


@log_performance
def search_csv_file(filename: str, column: str, value: str):
    raise NotImplementedError
