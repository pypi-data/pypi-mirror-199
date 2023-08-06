import dataclasses
from typing import Any, Dict, List, TypedDict
from enum import Enum

ResponseMessage = Dict | List


class SpotResponseMessage(TypedDict):
    id: str
    status: int
    result: dict | list
