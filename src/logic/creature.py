import pygame
from logic.game_components import *
from logic.sprite_controller import SpriteController
from enum import Enum
from logic.food import FoodData
import logic.context as context

class CreatureBehaviour(Script):
    '''Script controlling most things in the main scene'''
    def __init__(self, parent: GameObject|None, happy_bar: GameObject, hungry_bar:GameObject, energy_bar:GameObject, coins_text:Text,
                 eyes: GameObject, mouth: GameObject):
        Script.__init__(self, parent)
        self._max_value = 100
        self._hunger = 100
        self._happiness = 100
        self._energy = 100
        self._inner_clock : float = 0.
        self._happy_bar : GameObject = happy_bar
        self._hungry_bar: GameObject = hungry_bar
        self._energy_bar: GameObject = energy_bar
        self._coins = 12
        self._coins_display : Text = coins_text
        self._paused = False
        self._sprite_change_timer = 0;
        self._eyes = eyes
        self._mouth = mouth
        self._death_counter = 0
        self._dead = False
        self._dark = False
        self._sleeping = False

    def init(self):
        self._coins_display._text = f"{self._coins:03}"
        self._hungry_bar.message("set_value", self._hunger)
        self._happy_bar.message("set_value", self._happiness)
        self._energy_bar.message("set_value", self._energy)
        self._transform = self._parent.get_component(Transform)
        self._mouth_sprite:MouthScript = self._mouth.get_component(MouthScript) #type: ignore
        self._eyes_sprite:SpriteController = self._eyes.get_component(SpriteController) #type:ignore
    
    def update(self, delta_time: float):

        self._energy -= context.global_vars.pop("energy", 0)
        self._coins += context.global_vars.pop("score", 0)
 
        if not self._paused and not self._dead:
            self._inner_clock-=delta_time
        
        if self._sprite_change_timer > 0:
            self._sprite_change_timer-=delta_time

        elif self._sprite_change_timer<0:
            self._sprite_change_timer = 0

        if self._inner_clock<=0:
            
            if self._hunger > 0:
                if self._sleeping:
                    self._hunger-=0.5
                else:
                    self._hunger-=2

            if self._happiness < 0:
                self._happiness = 0
            
            if self._hunger < 0:
                self._happiness = 0
            
            if self._energy<0:
                self._energy = 0

            if self._hunger<30:
                self._happiness -=5
            elif self._hunger<60:
                self._happiness-=1
            
            if self._sleeping and self._energy<100:
                self._energy=min(self._energy+1, 100)
        
            if self._energy==100 and self._sleeping:
                self._sleeping = False

            if self._dark and not self._sleeping:
                self._happiness-=2

            self._inner_clock = 2
            self._hungry_bar.message("set_value", self._hunger)
            self._happy_bar.message("set_value", self._happiness)
            self._energy_bar.message("set_value", self._energy)


            if self._hunger ==0:
                self._death_counter+=1
            if self._happiness == 0:
                self._death_counter+=1
            if self._energy ==0:
                self._death_counter+=1
            
            if self._hunger>0 and self._happiness>0 and self._energy>0:
                self._death_counter = 0
            
            if self._death_counter >=500:
                self._dead = True
                self._mouth.message("die")
        
        self.resolve_state()
        self._coins_display._text = f"{self._coins:03}"

    
    def resolve_state(self):
        mouth_id = 0
        eyes_id = 0
        if self._dead:
            mouth_id = 6
        elif self._sleeping:
            mouth_id = 7
        
        elif self._dark and not self._sleeping:
            mouth_id = 3

        elif self._mouth_sprite.is_open:
            if self._hunger <= 95:
                mouth_id = 2
            else:
                mouth_id = 5

        elif self._sprite_change_timer>0:
            mouth_id = 4
        elif self._happiness < 20:
            mouth_id = 5
        elif self._hunger < 60:
            mouth_id = 3
        elif self._happiness > 90:
            mouth_id = 1

        if self._dead:
            eyes_id = 3
        elif self._sleeping:
            eyes_id = 4
        elif self._sprite_change_timer>0:
            eyes_id = 1
        elif self._mouth_sprite.is_open and self._hunger>=95:
            eyes_id = 1
        elif self._energy<20:
            eyes_id = 2
        
        self._eyes_sprite.switch_sprite(eyes_id)
        self._mouth_sprite.switch_sprite(mouth_id)
            
        
    #message-activated


    def feed(self, food_data: FoodData):
        if not self._dead and not self._sleeping:
            if self._hunger < 95:
                self._hunger = min(self._hunger+food_data.saturation, self._max_value)
                self._hungry_bar.message("set_value", self._hunger)
                food_data.amount-=1
    
    def pet(self):
        if not self._dead and not self._sleeping:
            self._happiness =  min(self._happiness+5, self._max_value)
            self._happy_bar.message("set_value", self._happiness)
            self._sprite_change_timer = 1

    

    def toggle_light(self):
        self._dark = not self._dark
        if self._dark:
            if self._energy<=90:
                self._sleeping = True
        else:
            self._sleeping = False
        


class MouthScript(SpriteController):
    '''Script controlling the mouth sprite. It used to do more but became simple utility with production'''
    def __init__(self, parent: GameObject, mouth_sprite: Image, sprite_grid: tuple[int, int], origin: tuple[int, int], food_box: Hitbox):
        SpriteController.__init__(self, parent, mouth_sprite, sprite_grid, origin)
        self.is_open: bool = False
        self._food_box = food_box
        self._dead = False
    
    def init(self):
        self._hitbox: Hitbox = self._parent.get_component(Hitbox)

    def update(self, delta_time):
        if not self._dead:
            tmp = self._hitbox.get_colliding()
            if self._food_box in tmp and not self.is_open:
                self.is_open = True
            elif not self._food_box in tmp and self.is_open:
                self.is_open = False

    #message-activated

    def feed(self, food_data: FoodData):
        self._parent._parent.message("feed", food_data)
    
    def die(self):
        self._dead = True