from logic.game_components import *
from logic.sprite_controller import SpriteController

class LightScript(Script):
    def __init__(self, parent: GameObject, sprite_controller: SpriteController, darkness: Rectangle):
        Script.__init__(self, parent)
        self._sprite = sprite_controller
        self._darknes = darkness
        self._toggle = True
    
    def init(self):
        self._sprite.switch_sprite(1)
    
    def toggle_light(self):
        self._toggle = not self._toggle
        if self._toggle:
            self._sprite.switch_sprite(1)
            self._darknes._active = False
        
        else:
            self._sprite.switch_sprite(0)
            self._darknes._active = True