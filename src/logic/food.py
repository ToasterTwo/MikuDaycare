import logic.game_components as gc
from logic.sprite_controller import SpriteController
from logic import context

class FoodScript(gc.Script):
    def __init__(self, parent:gc.GameObject, sprite: SpriteController, hitbox: gc.Hitbox, image: gc.Image, clone: gc.GameObject):
        gc.Script.__init__(self, parent)
        self._sprite = image
        self._hitbox = hitbox
        self._controller = sprite
        self._clone = clone
    
    def cursor_enter(self):
        self._sprite.scale(2, 2)
        self._sprite._angle = 30
    
    def cursor_exit(self):
        self._sprite.scale(1, 1)
        self._sprite._angle = 0
    
    def mouse(self, button: int, down: bool):
        if button == 1 and down and not self._clone._active:
            self._clone._active = True


class FoodCloneScript(gc.Script):
    def __init__(self, parent: gc.GameObject, sprite: SpriteController, cursor: gc.Transform):
        gc.Script.__init__(self, parent)
        self._sprite: SpriteController = sprite
        self._cursor: gc.Transform = cursor
    
    def init(self):
        self._transform:gc.Transform = self._parent.get_component(gc.Transform)
        if self._transform is None:
            raise ValueError("None where Transform is expected")
    
    def update(self, delta_time):
        self._transform._x = self._cursor._x
        self._transform._y = self._cursor._y
    
    def mouse(self, button: int, down: bool):
        if button == 1 and not down:
            self._parent._active = False