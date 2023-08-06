from typing import Optional, TypedDict, Union


class Result(TypedDict):
    confidence: Union[int, float]
    index: Optional[int]
    value: str
