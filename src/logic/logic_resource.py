from typing import Any
from enum import Enum

class ResourceType(Enum):
    IMAGE = 0
    SHAPE = 1
    SOUND = 2
    TILES = 3
    TEXT = 4

class LogicResource:
    '''A class representing a resource to be passed along to the renderer.

    The resource parameters are given as kwargs and stored as attributes of the object. It is up to the individual Renderable objects to define what data is passed
    along, and up to the renderer to decide what to do with this data.

    The only required attribute is the type, which is defined as an Enum
    '''
    def __init__(self, r_type: ResourceType, **kwargs):
        self._type = r_type
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        
    def __getattribute__(self, name: str) -> Any:
        return object.__getattribute__(self, name)