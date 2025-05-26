import pygame
from enum import Enum
from logic.game_components import *

class BarMode(Enum):
    HORIZONTAL = 0b0
    VERTICAL = 0b1

class BarAligngment(Enum):
    TOPLEFT = 0
    BOTTOMRIGHT = 1
    CENTER = 2


class ProgressBar(Script):
    def __init__(self, parent: GameObject |None, max_value: int, start_value: int, bar_image: Rectangle, mode: BarMode | str = BarMode.VERTICAL, alignment = BarAligngment.CENTER):
        Script.__init__(self, parent)
        self._max_value = max_value
        self.value = start_value
        self._image: Rectangle = bar_image
        
        if type(mode) == str:
            mode = BarMode.__dict__[mode]
        self._mode = mode

        if type(alignment) == str:
            alignment = BarAligngment.__dict__[alignment]
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

            