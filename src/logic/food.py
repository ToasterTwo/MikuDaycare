import logic.game_components as gc
from logic.sprite_controller import SpriteController

class FoodScript(gc.Script):
    def __init__(self, parent:gc.GameObject, sprite: SpriteController, hitbox: gc.Hitbox, image: gc.Image):
        gc.Script.__init__(self, parent)
        self._sprite = image
        self._hitbox = hitbox
        self._controller = sprite
    
    def cursor_enter(self):
        self._sprite.scale(2, 2)
        self._sprite._angle = 30
    
    def cursor_exit(self):
        self._sprite.scale(1, 1)
        self._sprite._angle = 0