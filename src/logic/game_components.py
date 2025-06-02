from pygame import event, time
from typing import Any
import math

class Component:
    NAME_MAP:dict[str, type] = {}
    def __init__(self, parent :Any  = None, active: bool = True):
        self._parent = parent
        self._active = True

    def __init_subclass__(cls, **kwargs):
        typename = cls.__name__
        if typename not in Component.NAME_MAP:
            Component.NAME_MAP[typename] = cls

    def set_parent(self, new_parent: Any):
        self._parent = new_parent

    def is_active(self)->bool:
        if self._parent is None:
            return self._active
        return self._active and self._parent.is_active()
    
    @staticmethod
    def from_name(name: str, parent, *args, **kwargs):
        return Component.NAME_MAP[name](parent, *args, **kwargs)

class GameObject(Component):
    def __init__(self, parent : Component | None= None, *components:Component):
        Component.__init__(self, parent)
        self._components = list(components)
        for comp in self._components:
            comp.set_parent(self)
    
    def get_components(self, _type: type | None = None, inheritance:bool = False) -> list:
        if _type is None:
            return self._components
        ret = [c for c in self._components if not inheritance and type(c)==_type or inheritance and issubclass(type(c), _type)]
        return ret
    
    def get_component(self, _type: type,  inheritance:bool = False) -> Component | None:
        for comp in self._components:
            if type(comp) == _type or inheritance and issubclass(type(comp), _type):
                return comp
        return None

    def init(self):
        for script in self.get_components(Script, True):
            script.init()

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
    
    def init(self):
        pass

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
            m_transform:list[Transform] = root.get_components(Transform)
            
            if len(m_transform)<1:
                continue
            
            parent_transform = m_transform[0]

            if parent_transform != self:
                root_tilt = parent_transform._angle * math.pi /180
                root_space_x = global_x*math.cos(root_tilt)-global_y*math.sin(root_tilt)
                root_space_y = global_x*math.sin(root_tilt)+global_y*math.cos(root_tilt)
                global_x = parent_transform._x+root_space_x
                global_y = parent_transform._y+root_space_y
                global_angle+=parent_transform._angle
            
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
        
        Renderable.__init__(self, parent, position, angle, scale, layer)
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
        self._colliding  = []
        if not self in Hitbox.ALL_BOXES:
            Hitbox.ALL_BOXES.append(self)
    
    def get_global_bounds(self) -> tuple[float, float, float, float]:
        master_transform = self._parent.get_components(Transform)

        if len(master_transform) < 1:
            return self._top, self._left, self._bottom, self._right 
        
        parent_coords:tuple[float, float, float] = master_transform[0].get_global()

        return self._top+parent_coords[1], self._left+parent_coords[0], self._bottom + parent_coords[1], self._right + parent_coords[0]

    def move(self, dx:float, dy:float) -> None:
        self._top += dy
        self._bottom += dy
        self._left += dx
        self._right += dx
    
    @staticmethod
    def recalculate_collisions():
        for box in Hitbox.ALL_BOXES:
            box._colliding.clear()
        for i in range(len(Hitbox.ALL_BOXES)):
            box: Hitbox= Hitbox.ALL_BOXES[i]
            if not box.is_active():
                continue
            for j in range(i+1, len(Hitbox.ALL_BOXES)):
                other:Hitbox = Hitbox.ALL_BOXES[j]
                if not other.is_active():
                    continue
                if box.collides(other):
                    box._colliding.append(other)
                    other._colliding.append(box)
    
    def set_bounds(self, top: float, left: float, height: float, width: float) -> None:
        self._top = top
        self._left = left
        self._right = top+height
        self._bottom = left+width

    def collides(self, other) -> bool:
        me = self.get_global_bounds()
        them = other.get_global_bounds()

        x : bool = not (me[1]>them[3] or them[1]>me[3])
        y : bool = not (me[0]>them[2] or them[0]>me[2])

        return x and y


    def get_colliding(self) -> list[Component]:        
        return self._colliding
