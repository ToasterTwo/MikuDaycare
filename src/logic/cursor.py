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
        self._petting = False
        self._grabbing = False
        self._holding = False

    def init(self):
        self._sprite_ctrl: SpriteController = self._parent.get_component(SpriteController)

    def update(self, delta_time):
        colliders : list[gc.Hitbox] = self._hitbox.get_colliding() #type:ignore
        for h in self._hovering:
            if h not in colliders:
                self._hovering.remove(h)
                h._parent.message("cursor_exit")
                if not self._holding:
                    self._sprite_ctrl.switch_sprite(0)
                if h._parent.has_tag("pettable") and self._petting:
                    self._petting = False
                    self._transform._angle = 0
                if h._parent.has_tag("grabbable") and self._grabbing:
                    self._holding = False
                    self._grabbing = False

            else:
                h._parent.message("cursor_hover")
                if h._parent.has_tag("clickable"):
                    self._sprite_ctrl.switch_sprite(1)
                
                elif h._parent.has_tag("pettable") and not (self._petting or self._holding):
                    self._sprite_ctrl.switch_sprite(2)
                    self._transform._angle = -30
                    self._petting = True
                
                elif h._parent.has_tag("grabbable") and not (self._grabbing or self._holding):
                    self._sprite_ctrl.switch_sprite(3)
                    self._grabbing = True


        for coll in colliders:
            if coll not in self._hovering:
                self._hovering.append(coll)
                coll._parent.message("cursor_enter")
        

    def on_event(self, _event: pygame.event.Event)->None:
        match _event.type:
            case pygame.MOUSEMOTION:
                self._transform._x = _event.pos[0]
                self._transform._y = self._window_height-_event.pos[1]
        
            case pygame.MOUSEBUTTONDOWN:
                if self._petting:
                    self._transform._angle = 0
                elif self._grabbing:
                    self._holding = True
                    self._sprite_ctrl.switch_sprite(4)
                for hov in self._hovering:
                    hov._parent.message("mouse", _event.button, True)
            
            case pygame.MOUSEBUTTONUP:
                if self._petting:
                    self._transform._angle = -30
                if self._holding:
                    self._holding = False
                for hov in self._hovering:
                    hov._parent.message("mouse", _event.button, False)