from pygame import event, time
from typing import Any
import math

class Component:
    def __init__(self, parent :Any  = None):
        self._parent = parent
    
    def set_parent(self, new_parent: Any):
        self._parent = new_parent

class GameObject(Component):
    def __init__(self, *components:Component, parent : Component | None= None):
        Component.__init__(self, parent)
        self._components = list(components)
        for comp in self._components:
            comp.set_parent(self)
    
    def get_components(self, _type: type | None = None, inheritance:bool = False) -> list:
        if _type is None:
            return self._components
        ret = [c for c in self._components if not inheritance and type(c)==_type or inheritance and issubclass(type(c), Script)]
        return ret

    def update(self, delta_time):
        for script in self.get_components(Script, True):
            script.update(delta_time)
    
    def on_event(self, event):
        for script in self.get_components(Script, True):
            script.on_event(event)

    
    def message(self, message: str, *args):
        for script in self.get_components(Script, True):
            if message in type(script).__dict__:
                 type(script).__dict__[message](script, *args)
    
    def add_components(self, *components: Component):
        for comp in components:
            comp.set_parent(self)
            self._components.append(comp)
    

class Script(Component):
    def __init__(self, parent: GameObject|None = None):
        Component.__init__(self, parent)
    
    def update(self, delta_time:float):
        pass

    def on_event(self, _event:event.Event):
        pass



class Transform(Component):
    def __init__(self, parent: GameObject | None = None, position: list[float] = [0,0], angle: float = 0., scale: list[float] = [1., 1.]):
        Component.__init__(self, parent)
        self._x, self._y = position
        self._scale_x, self._scale_y = scale
        self._angle = angle

    def get_global(self):
        root = self._parent
        global_x = self._x
        global_y = self._y
        global_angle = self._angle
        while root != None:
            transforms:list[Transform] = root.get_components(Transform)
            
            if len(transforms)<1:
                continue

            root_x = 0
            root_y = 0
            root_angle = 0
            for t in transforms:
                root_x += t._x
                root_y += t._y
                root_angle += t._angle
            global_x += root_x/len(transforms)
            global_y += root_y/len(transforms)
            global_angle += root_angle/len(transforms)
            root = root._parent
        
        return global_x, global_y, global_angle
    
    def move(self, dx:float = 0, dy:float = 0):
        self._x+=dx
        self._y+=dy
    
    def rotate(self, angle:float):
        self._angle+=angle
    
    def scale(self, scale_x = 1., scale_y = 1.):
        self._scale_x = scale_x
        self._scale_y = scale_y


class Renderable(Transform):
    def __init__(self, 
                 parent: GameObject | None= None, 
                 position: list[float] = [0, 0], 
                 angle: float = 0., 
                 scale:list[float] = [1., 1.], 
                 layer: int = 0):
        Transform.__init__(self, parent, position, angle, scale)
        self._layer = layer

class Rectangle(Renderable):
    def __init__(self, 
                 parent: GameObject | None= None, 
                 dimensions: tuple[float, float] = (100, 100), 
                 color: tuple[int, int, int] = (0xFF, 0xFF, 0xFF), 
                 position: list[float]= [0.,0.], 
                 angle: float = 0, 
                 layer:int = 0):
        Renderable.__init__(self, parent, position, angle, [1,1], layer)
        self._dimensions = dimensions
        self._color = color
    
    def reshape(self, dimensions:tuple[float, float]):
        self._dimensions = dimensions


class Image(Renderable):
    def __init__(self, 
                 parent:GameObject | None = None, 
                 path:str = "none", 
                 scale:list[float] = [1., 1.], 
                 position: list[float] = [0, 0], 
                 angle: float = 0, 
                 layer: int = 0,
                 texture_rect: tuple[int, int, int, int] = (0, 0, -1, -1)):
        
        offset = [0., 0.]
        if texture_rect[2]>0:
            offset[0]=-texture_rect[2]/2
        if texture_rect[3]>0:
            offset[1]=-texture_rect[3]/2

        Renderable.__init__(self, parent, [position[0]+offset[0], position[1]+offset[1]], angle, scale, layer)
        self._path = path
        self._texture_rect = texture_rect

class Hitbox(Component):
    ALL_BOXES = []
    def __init__(self, 
                 parent :GameObject |None = None,
                 top: float = 0,
                 left: float = 0,
                 height: float = 1,
                 width: float = 1):
        Component.__init__(self, parent)
        self._top = top
        self._left = left
        self._bottom = top+height
        self._right = left+width
        Hitbox.ALL_BOXES.append(self)
    
    def get_global_bounds(self) -> tuple[float, float, float, float]:
        parent_coords:tuple[float, float, float] = self._parent.get_components(Transform)[0].get_global()

        return self._top+parent_coords[1], self._left+parent_coords[0], self._bottom + parent_coords[1], self._right + parent_coords[0]

    def move(self, dx:float, dy:float) -> None:
        self._top += dy
        self._bottom += dy
        self._left += dx
        self._right += dx
    
    def set_bounds(self, top: float, left: float, height: float, width: float) -> None:
        self._top = top
        self._left = left
        self._right = top+height
        self._bottom = left+width

    def collides(self, other) -> bool:
        x : bool = not (self._left>other._right or other._left>self._right)
        y : bool = not (self._top>other._bottom or other._top>self._bottom)

        return x and y


    def get_colliding(self) -> list[Component]:
        collided: list[Component] = []
        for other in Hitbox.ALL_BOXES:
            if self.collides(other):
                collided.append(other)
        
        return collided
