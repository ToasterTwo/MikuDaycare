import pygame
import logic.game_components as gc

class CursorScript(gc.Script):
    def __init__(self, parent: gc.GameObject | None, transform: gc.Transform, hitbox: gc.Hitbox):
        gc.Script.__init__(self, parent)
        self._transform = transform
        self._hitbox = hitbox
        self._hovering = []

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
        if _event.type == pygame.MOUSEMOTION:
            self._transform._x = _event.pos[0]
            self._transform._y = _event.pos[1]