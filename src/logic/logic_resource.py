from logic.game_components import *
from enum import Enum

class ResourceType(Enum):
    IMAGE = 0
    SHAPE = 1
    SOUND = 2

class LogicResource:
    def __init__(self, r_type: ResourceType, **kwargs):
        self._type = r_type
        self._data = kwargs

    @staticmethod
    def of_image(img: Image):
        global_position = img.get_global()
        return LogicResource(
            ResourceType.IMAGE, 
            path = img._path,
            scale = (img._scale_x, img._scale_y), 
            global_position = global_position)

    @staticmethod
    def of_shape(shape: Rectangle):
        return LogicResource(
            ResourceType.SHAPE, 
            dimensions = shape._dimensions,
            scale = shape._scale,
            color = shape._color,
            global_position = shape.get_global())