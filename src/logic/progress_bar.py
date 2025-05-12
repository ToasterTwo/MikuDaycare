import pygame
from enum import Enum
try:
    from logic.game_components import *
except ModuleNotFoundError:
    from game_components import *

class BarMode(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class ProgressBar(Script):
    def __init__(self, parent: GameObject, max_value: int, start_value: int, bar_image: Image, mode: BarMode = BarMode.VERTICAL):
        Script.__init__(self, parent)
        self._max_value = max_value
        self.value = start_value
        self._image: Rectangle = bar_image
        self._mode = mode

    def set_value(self, new_value):
        self.value = new_value
        scale = self.value/self._max_value
        match self._mode:
            case BarMode.HORIZONTAL:
                self._image.scale((scale, 1))
            case BarMode.VERTICAL:
                self._image.scale((1, scale))
            