from typing import Any
from enum import Enum

class ResourceType(Enum):
    IMAGE = 0
    SHAPE = 1
    SOUND = 2
    TILES = 3
    TEXT = 4

class LogicResource:
    def __init__(self, r_type: ResourceType, **kwargs):
        self._type = r_type
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        
    def __getattribute__(self, name: str) -> Any:
        return object.__getattribute__(self, name)