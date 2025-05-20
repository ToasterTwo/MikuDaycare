import pygame
from logic.game_components import *


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
            self._inner_clock = 0
            self._happy_bar.message("set_value", self._happiness)
            
    
    def on_event(self, _event: pygame.event.Event):
        if _event.type == pygame.MOUSEBUTTONDOWN:
            self._happiness += 1
            self._happy_bar.message("set_value", self._happiness)

spritepath = "resources\\images\\spritesheet.png"

body_image = Image(path = spritepath, texture_rect=(0, 0, 50, 145),layer=0)
hair_image = Image(path = spritepath, texture_rect=(50, 0, 110, 105), layer=2)
eyes_image = Image(path = spritepath, texture_rect=(50, 105, 30, 15), layer=1)
mouth_image = Image(path = spritepath, texture_rect=(50, 120, 15, 7), layer=1)
left_arm_image = Image(path = spritepath, texture_rect=(160, 0, 24, 43), layer=1)
right_arm_image = Image(path = spritepath, texture_rect=(160, 43, 24, 43), layer=1)

hair_sprite = GameObject(hair_image, Transform(position=[-5, -27]))
eyes_sprite = GameObject(eyes_image, Transform(position=[0, -50]))
mouth_sprite = GameObject(mouth_image, Transform(position=[0, -40]))
left_arm_sprite = GameObject(left_arm_image, Transform(position=[18, -10]))
right_arm_sprite= GameObject(right_arm_image, Transform(position=[-20, -10]))
