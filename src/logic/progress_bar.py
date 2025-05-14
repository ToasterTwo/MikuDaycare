import pygame
from enum import Enum
try:
    from logic.game_components import *
except ModuleNotFoundError:
    from game_components import *

class BarMode(Enum):
    HORIZONTAL = 0b0
    VERTICAL = 0b1

class BarAligngment(Enum):
    TOPLEFT = 0
    BOTTOMRIGHT = 1
    CENTER = 2


class ProgressBar(Script):
    def __init__(self, parent: GameObject, max_value: int, start_value: int, bar_image: Rectangle, mode: BarMode = BarMode.VERTICAL, alignment = BarAligngment.CENTER):
        Script.__init__(self, parent)
        self._max_value = max_value
        self.value = start_value
        self._image: Rectangle = bar_image
        self._mode = mode
        self._alignment = alignment

    def set_value(self, new_value):
        self.value = new_value
        scale = self.value/self._max_value
        width, height = self._image._dimensions
        old_scale_x = self._image._scale_x
        old_scale_y = self._image._scale_y

        match self._mode:
            case BarMode.HORIZONTAL:
                self._image.scale(scale_x = scale)
            case BarMode.VERTICAL:
                self._image.scale(scale_y = scale)
        
        scale_x = self._image._scale_x
        scale_y = self._image._scale_y
        img_x, img_y = self._image.get_global()[:2]
        match self._alignment:
            case BarAligngment.TOPLEFT:
                dx = width*(scale_x-old_scale_x)/2
                dy = height*(scale_y-old_scale_y)/2
                self._image.move(dx, dy)

            case BarAligngment.BOTTOMRIGHT:
                dx = -width*(scale_x-old_scale_x)/2
                dy = -height*(scale_y-old_scale_y)/2
                self._image.move(dx, dy)

            