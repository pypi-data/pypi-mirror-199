# Huntela
**Huntela** is a savvy search module that's an alternative to the default `filter` method. It offers a range of powerful search functions, including fuzzy search, binary search, and searches for least/most frequent items in a list.

```python
>>> import huntela
>>> 
>>> huntela.fuzzy_search(term='app', items=['app', 'paper', 'hello', 'world'])
[
    {'confidence': 1, 'index': 0, 'value': 'app'},
    {'confidence': 0.6, 'index': 1, 'value': 'paper'}
]
>>> 
>>> huntela.binary_search(term='a', items=['a', 'b', 'c'])
{'confidence': 1, 'index': 0, 'value': 'a'}
>>> 
>>> huntela.search_for_least_frequent_items(size=1, ['a', 'b', 'a', 'e', 'a', 'e'])
[
    {'confidence': 1, 'index': [1], 'value': 'b'}
]
>>> 
>>> huntela.search_for_most_frequent_items(size=2, ['a', 'b', 'a', 'e', 'a', 'e'])
[
    {'confidence': 1, 'value': 'a', 'index': [0, 2, 4]},
    {'confidence': 1, 'value': 'e', 'index': [3, 5]}
]
```

With a variety of algorithms to choose from, finding what you're looking for has never been easier.

From binary search to linear search and more, Huntela has everything you need to 
quickly and efficiently search through your data. With a simple, intuitive interface
and lightning-fast performance, Huntela is the go-to package for anyone who needs to search through data.

Whether you're a data scientist, engineer, or  developer, Huntela will help you find what you need.

## Installation

> Huntela officially supports Python 3.9 upwards. 

Huntela is available on PyPi and it can be installed using `pip`

```bash
python -m pip install huntela
```

## Reference

### Parameters

Each of the search methods take in three (3) parameters.
1. `term`: The term being searched for.
2. `items`: The items parameter could then be a iterable of the supported term types.
3. `key` (Optional): Only to be specified if the `term` is a `dict`. In which case, the `key` will be used to pick the corresponding values from the list of `items`.

### Supported Types

#### Term

The term being searched for could be one of the following supported types:

1. `int`
2. `float`
3. `str`
4. `dict[str, Any]`

#### Items

The items parameter could then be a iterable of the supported term types. That is,

1. `List[int]`
2. `List[float]`
3. `List[str]`
4. `List[Dict[str, str]]`

#### Results

Each search result is a `dict` which contains the following item:

1. `confidence`: A number from `0.0` to `1.0` that indicates the degree of relevance of the search match.
2. `value`: The specific item that matched the search criteria.
3. `index`: The position, or a list of positions where the search term was found.

### Methods

`fuzzy_search(term, items, key=None) -> List[Result]`: Searches a list of items for a given search term and returns a list of results which exactly or ***closely*** match the search term.

```python
>>> huntela.fuzzy_search(term='app', items=['app', 'paper', 'hello', 'world'])
[
    {'confidence': 1, 'index': 0, 'value': 'app'},
    {'confidence': 0.6, 'index': 1, 'value': 'paper'}
]
```

`binary_search(term, items, key=None) -> List[Result]`: Performs a binary search on a list to find a target value.

```python
>>> huntela.binary_search(
    term='Alex',
    items=[{'name': 'Alex'}, {'name': 'Mike'}, {'name': 'John'}],
    key='name'
)
{'confidence': 1, 'index': 0, 'value': 'Ade'}
```

`search_for_least_frequent_items`: Finds the k least frequent item(s) in a list.

```python
>>> search_for_least_frequent_items(size, items)
[
    {'confidence': 1, 'index': [0], 'value': 1},
    {'confidence': 1, 'index': [2, 3], 'value': 3}
]
```

`search_for_most_frequent_items`: Finds the k most frequent item(s) in a list.

```python
>>> search_for_most_frequent_items(2, [1, 2, 2, 3, 3, 3])
[
    {'confidence': 1, 'index': [3, 4, 5], 'value': 3},
    {'confidence': 1, 'index': [1, 2], 'value': 2}
]
```
