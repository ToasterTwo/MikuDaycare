import pygame
try:
    from logic.game_components import *
except ModuleNotFoundError:
    from game_components import *



class CreatureBehaviour(Script):

    def __init__(self, parent: GameObject, happy_bar: GameObject):
        Script.__init__(self, parent)
        self._happiness = 10
        self._inner_clock : float = 0.
        self._happy_bar : GameObject = happy_bar
    
    def update(self, delta_time: float):
        self._inner_clock+=delta_time
        if self._inner_clock>2:
            self._happiness-=1
            self._inner_clock = 0
            self._happy_bar.message("set_value", self._happiness)
            
    
    def on_event(self, _event: pygame.event.Event):
        if _event.type == pygame.MOUSEBUTTONDOWN:
            self._happiness += 1
            self._happy_bar.message("set_value", self._happiness)
