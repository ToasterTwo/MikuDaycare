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
    '''A Script for managing a progress bar with automatic alignment
    
    Attributes
    ----------
    max_value, start_value: int
        self explanatory
    bar_image: Rectangle
        the rectangle this will be operating on
    mode: BarMode
        which way should the bar be scaled
    alignment: BarAlignment
        how to align the bar after scaling
    color_map: list[tuple[int, tuple[int, int, int] | tuple[int, int, int, int]]]
        optional, allows for dynamic color changes depending on the bar's value
    '''
    def __init__(self, parent: GameObject |None, 
                 max_value: int, start_value: int, 
                 bar_image: Rectangle, 
                 mode: BarMode | str = BarMode.VERTICAL, 
                 alignment = BarAligngment.CENTER,
                 color_map: list[tuple[int, tuple[int, int, int] | tuple[int, int, int, int]]] = []):
        Script.__init__(self, parent)
        self._max_value = max_value
        self._value = start_value
        self._image: Rectangle = bar_image
        self._color_map = color_map
        self._color_map.sort(key=lambda x: x[0])
        has_max = False
        for col in self._color_map:
            if col[0] == 100:
                has_max = True
                break
        if not has_max:
            self._color_map.append((100, self._image._color))

        if type(mode) == str:
            mode = BarMode.__dict__[mode]
        self._mode = mode

        if type(alignment) == str:
            alignment = BarAligngment.__dict__[alignment]
        self._alignment = alignment

    def set_value(self, new_value):
        if new_value<0:
            return
        self._value = new_value
        scale = self._value/self._max_value
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
        match self._alignment:
            case BarAligngment.TOPLEFT:
                dx = -width*(scale_x-old_scale_x)/2
                dy = -height*(scale_y-old_scale_y)/2
                self._image.move(dx, dy)

            case BarAligngment.BOTTOMRIGHT:
                dx = +width*(scale_x-old_scale_x)/2
                dy = +height*(scale_y-old_scale_y)/2
                self._image.move(dx, dy)

        for col in self._color_map:
            if scale*100 <= col[0]:
                self._image._color = col[1]
                break