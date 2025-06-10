import logic.game_components as gc
from logic.sprite_controller import SpriteController
from logic import context
from dataclasses import dataclass

@dataclass
class FoodData:
    sprite_id : int
    saturation: int
    amount:int
    cost:int



class FoodScript(gc.Script):
    def __init__(self, parent:gc.GameObject, sprite: SpriteController, hitbox: gc.Hitbox, image: gc.Image, clone: gc.GameObject, food_counter: gc.Text):
        gc.Script.__init__(self, parent)
        self._sprite = image
        self._hitbox = hitbox
        self._controller = sprite
        self._clone = clone
        self._foods = [FoodData(0, 10, 10, 2), FoodData(1, 15, 10, 4), FoodData(2, 25, 1, 6)]
        self._food_now = 0
        self._counter = food_counter

    def init(self):
        self._controller.switch_sprite(self._foods[self._food_now].sprite_id)
        self._counter._text = f"{self._foods[self._food_now].amount:02}"
    
    def update(self, delta_time):
        self._counter._text = f"{self._foods[self._food_now].amount:02}"

    
    def cursor_enter(self):
        if self._foods[self._food_now].amount>0:
            self._sprite.scale(1.5, 1.5)
            self._sprite._angle = 5
    
    def cursor_exit(self):
        self._sprite.scale(1, 1)
        self._sprite._angle = 0
    
    def mouse(self, button: int, down: bool):
        if button == 1 and down and not self._clone._active and self._foods[self._food_now].amount>0:
            self._clone._active = True
            self._clone.message("pick_food", self._foods[self._food_now])
            self.cursor_exit()
    
    def next(self):
        self._food_now = (self._food_now+1)%len(self._foods)
        self._controller.switch_sprite(self._foods[self._food_now].sprite_id)
    
    def prev(self):
        self._food_now = (self._food_now-1)%len(self._foods)
        self._controller.switch_sprite(self._foods[self._food_now].sprite_id)
    
    def menu(self):
        self._hitbox._active = False
    
    def unmenu(self):
        self._hitbox._active = True



class FoodCloneScript(gc.Script):
    def __init__(self, parent: gc.GameObject, sprite: SpriteController, cursor: gc.Transform, mouth: gc.GameObject):
        gc.Script.__init__(self, parent)
        self._sprite: SpriteController = sprite
        self._cursor: gc.Transform = cursor
        self._food : FoodData
        self._mouth = mouth
    
    def init(self):
        self._transform:gc.Transform = self._parent.get_component(gc.Transform)
        self._hitbox: gc.Hitbox = self._parent.get_component(gc.Hitbox)
        self._mouth_hitbox: gc.Hitbox = self._mouth.get_component(gc.Hitbox) # type: ignore
        if self._transform is None or self._mouth_hitbox is None:
            raise ValueError("None where Transform is expected")
    
    def update(self, delta_time):
        self._transform._x = self._cursor._x
        self._transform._y = self._cursor._y
    
    def mouse(self, button: int, down: bool):
        if button == 1 and not down:
            if self._hitbox.collides(self._mouth_hitbox):
                self._mouth.message("feed", self._food)

            self._parent._active = False
        
    def pick_food(self, food: FoodData):
        self._food = food
        self._sprite.switch_sprite(self._food.sprite_id)