import pygame
import logic.game_components as gc
from logic.sprite_controller import SpriteController

class CursorScript(gc.Script):
    def __init__(self, parent: gc.GameObject | None, transform: gc.Transform, hitbox: gc.Hitbox, window_height:int):
        gc.Script.__init__(self, parent)
        self._transform = transform
        self._hitbox = hitbox
        self._hovering = []
        self._window_height = window_height
        # 0 - neutral
        # 1 - clicking
        # 2 - petting
        # 3 - grabbing
        # 4 - holding
        self._state = 0

    def init(self):
        self._sprite_ctrl: SpriteController = self._parent.get_component(SpriteController)

    def update(self, delta_time):
        self._transform._x, self._transform._y = pygame.mouse.get_pos()
        self._transform._y = self._window_height-self._transform._y
        colliders : list[gc.Hitbox] = self._hitbox.get_colliding() #type:ignore
        for h in self._hovering:
            if h not in colliders:
                self._hovering.remove(h)
                h._parent.message("cursor_exit")
                if self._state == 1 and h._parent.has_tag("clickable"):
                    self._state = 0
                elif self._state == 2 and h._parent.has_tag("pettable"):
                    self._state = 0
                    self._transform._angle = 0
                elif self._state == 3 and h._parent.has_tag("grabbable"):
                    self._state = 0


            else:
                h._parent.message("cursor_hover")
                if h._parent.has_tag("clickable"):
                    self._state = 1
                
                elif h._parent.has_tag("pettable") and self._state == 0:
                    self._transform._angle = -30
                    self._state = 2
                
                elif h._parent.has_tag("grabbable") and self._state == 0:
                    self._state = 3


        for coll in colliders:
            if coll not in self._hovering:
                self._hovering.append(coll)
                coll._parent.message("cursor_enter")
        
        self.update_sprite()
        

    def on_event(self, _event: pygame.event.Event)->None:
        match _event.type:        
            case pygame.MOUSEBUTTONDOWN:
                if self._state  == 2:
                    self._transform._angle = 0
                elif self._state == 3:
                    self._state = 4
                for hov in self._hovering:
                    hov._parent.message("mouse", _event.button, True)
            
            case pygame.MOUSEBUTTONUP:
                if self._state == 2:
                    self._transform._angle = -30
                if self._state == 4:
                    self._state = 0
                for hov in self._hovering:
                    hov._parent.message("mouse", _event.button, False)
        
    def update_sprite(self):
        self._sprite_ctrl.switch_sprite(self._state)