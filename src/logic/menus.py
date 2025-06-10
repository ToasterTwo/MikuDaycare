from logic.game_components import *
from logic.creature import *
from logic.food import *

class MenuScript(Script):
    derivative_id = 0
    def __init__(self, parent: GameObject, activate_messages:list[str], deactivate_messages:list[str], menu_elements:list[Component]):
        
        #pretty sure this is evil but what the hell
        attrs = {}
        for m in activate_messages:
            attrs[m] = MenuScript.activate
        
        for m in deactivate_messages:
            attrs[m] = MenuScript.deactivate
        
        classname = ""
        if type(self) != MenuScript:
            classname = self.__class__.__name__
        else:
            classname = f"MenuScript#{MenuScript.derivative_id}"
            MenuScript.derivative_id+=1

        self.__class__ = type.__new__(type, classname, (Script,), attrs)

        Script.__init__(self, parent)
        self._menu_elements = menu_elements

    def activate(self):
        for element in self._menu_elements: #type:ignore
            element._active = True 

    def deactivate(self):
        for element in self._menu_elements: #type:ignore
            element._active = False 
    

class ShopScript(Script):
    def __init__(self, parent:GameObject, miku: CreatureBehaviour, food: FoodScript, shop_display: SpriteController, price_display:Text, funds_display: Text):
        Script.__init__(self, parent)
        self._food = food
        self._miku = miku
        self._food_list = self._food._foods
        self._display = shop_display
        self._displayed_food = 0
        self._price_display = price_display
        self._funds_display = funds_display
        
    
    def update(self, delta_time):
        self._display.switch_sprite(self._displayed_food)
        self._price_display._text = f"{self._food_list[self._displayed_food].cost}"
        if self._food_list[self._displayed_food].cost > self._miku._coins:
            self._funds_display._color = (255, 0, 0)
        else:
            self._funds_display._color = (0, 0, 0)
        self._funds_display._text = f"{self._miku._coins:03}"
    
    def next(self):
        self._displayed_food = (self._displayed_food+1)%len(self._food_list)
    
    def prev(self):
        self._displayed_food = (self._displayed_food-1)%len(self._food_list)
    
    def buy(self):
        if self._miku._coins >= self._food_list[self._displayed_food].cost:
            self._food_list[self._displayed_food].amount+=1
            self._miku._coins -= self._food_list[self._displayed_food].cost