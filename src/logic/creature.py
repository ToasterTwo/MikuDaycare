import pygame
from logic.game_components import *
from logic.sprite_controller import SpriteController


class CreatureBehaviour(Script):

    def __init__(self, parent: GameObject|None, happy_bar: GameObject, hungry_bar:GameObject, energy_bar:GameObject):
        Script.__init__(self, parent)
        self._max_value = 100
        self._hunger = 50
        self._happiness = 100
        self._energy = 100
        self._inner_clock : float = 0.
        self._happy_bar : GameObject = happy_bar
        self._hungry_bar: GameObject = hungry_bar
        self._energy_bar: GameObject = energy_bar
        self._coins = 123

    def init(self):
        self._hungry_bar.message("set_value", self._hunger)
        self._happy_bar.message("set_value", self._happiness)
        self._energy_bar.message("set_value", self._energy)
        self._transform = self._parent.get_component(Transform)
        self._mouth:MouthScript = self._parent.get_component(MouthScript)
    
    def update(self, delta_time: float):
        self._inner_clock+=delta_time

        if self._inner_clock>2:
            
            self._hunger-=2
            if self._happiness < 0:
                self._happiness = 0

            if self._hunger<30:
                self._happiness -=5
            elif self._hunger<60:
                self._happiness-=1

            self._inner_clock = 0
            self._hungry_bar.message("set_value", self._hunger)
            self._happy_bar.message("set_value", self._happiness)
    
    def feed(self, value):
        self._hunger = min(self._hunger+value, self._max_value)
        self._hungry_bar.message("set_value", self._hunger)



class MouthScript(SpriteController):
    def __init__(self, parent: GameObject, mouth_sprite: Image, sprite_grid: tuple[int, int], origin: tuple[int, int], food_box: Hitbox):
        SpriteController.__init__(self, parent, mouth_sprite, sprite_grid, origin)
        self.is_open: bool = False
        self._food_box = food_box
    
    def init(self):
        self._hitbox: Hitbox = self._parent.get_component(Hitbox)

    def update(self, delta_time):
        tmp = self._hitbox.get_colliding()
        if self._food_box in tmp and not self.is_open:
            self.do_open()
        elif not self._food_box in tmp and self.is_open:
            self.do_close()
    
    def feed(self, saturation: int):
        self._parent._parent.message("feed", saturation)


    def do_open(self):
        self.switch_sprite(2)
        self.is_open = True
    
    def do_close(self):
        self.switch_sprite(0)
        self.is_open = False