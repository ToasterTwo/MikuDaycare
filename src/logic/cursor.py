import pygame
import logic.game_components as gc

class CursorScript(gc.Script):
    def __init__(self, parent: gc.GameObject | None, transform: gc.Transform, hitbox: gc.Hitbox, window_height:int):
        gc.Script.__init__(self, parent)
        self._transform = transform
        self._hitbox = hitbox
        self._hovering = []
        self._window_height = window_height

    def update(self, delta_time):
        colliders : list[gc.Hitbox] = self._hitbox.get_colliding() #type:ignore
        for h in self._hovering:
            if h not in colliders:
                self._hovering.remove(h)
                h._parent.message("cursor_exit")
            else:
                h._parent.message("cursor_hover")

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
                for hov in self._hovering:
                    hov._parent.message("mouse", _event.button, True)
            
            case pygame.MOUSEBUTTONUP:
                for hov in self._hovering:
                    hov._parent.message("mouse", _event.button, False)