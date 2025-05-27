import pygame
from logic.game_components import *
from logic.sprite_controller import SpriteController


class CreatureBehaviour(Script):

    def __init__(self, parent: GameObject|None, happy_bar: GameObject):
        Script.__init__(self, parent)
        self._happiness = 10
        self._inner_clock : float = 0.
        self._happy_bar : GameObject = happy_bar
    
    def update(self, delta_time: float):
        self._inner_clock+=delta_time
        if self._inner_clock>2:
            self._happiness-=1
            if self._happiness < 0:
                self._happiness = 0
            self._inner_clock = 0
            self._happy_bar.message("set_value", self._happiness)
            
    
    def on_event(self, _event: pygame.event.Event):
        if _event.type == pygame.MOUSEBUTTONDOWN:
            self._happiness += 1
            self._happy_bar.message("set_value", self._happiness)


class MouthScript(SpriteController):
    def __init__(self, parent: GameObject, mouth_sprite: Image, sprite_grid: tuple[int, int], origin: tuple[int, int]):
        SpriteController.__init__(self, parent, mouth_sprite, sprite_grid, origin)
    
    def cursor_enter(self):
        self.switch_sprite(1)

    def cursor_exit(self):
        self.switch_sprite(0)