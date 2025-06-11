from pygame import event, time
from typing import Any
import math
from logic.logic_resource import LogicResource, ResourceType

class Component:
    '''Base class for the elements of the game

    Attributes
    ----------
    _parent: GameObject
        the Game object that this component is attached to
    _active: bool
        wether this component is active. While a component is inactive it gets ignored by all other components. 
        For a component to be active, both it and its parent need to be active
    NAME_MAP: dict[str, type]
        a dict containing name-type pairs of every class deriving from Component
    '''
    NAME_MAP:dict[str, type] = {}
    def __init__(self, parent :Any  = None, active: bool = True):
        self._parent = parent
        self._active = True

    def __init_subclass__(cls, **kwargs):
        '''Registers every class deriving from Component in NAME_MAP'''
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
        '''Create a component object by giving the name of the derivative class and appropriate positional and keyword arguments.
        
        Passing improper args or kwargs may result in errors.
        '''
        return Component.NAME_MAP[name](parent, *args, **kwargs)

class GameObject(Component):
    '''A component logically representing a single object in the game.

    It effectively serves as a container class for other components. It also facilitates updates, event handling, and cross-object communication.

    A game object only sees its parent and its components. It does not have immidiate access to every game object that has it set as a parent.
    
    Attributes
    ----------
    _parent, _active:
        inherited from Component
    
    _components: list[Component]
        a list of components attached to this game object
    
    _tags: set[str]
        a set of additional descriptors, that can be checked for by other elements.
    '''
    def __init__(self, parent : Component | None= None, *components:Component, tags:list[str] = []):
        Component.__init__(self, parent)
        self._components = list(components)

        for comp in self._components:
            comp.set_parent(self)
        
        self._tags:set[str] = set(tags)
    
    def get_components(self, _type: type | None = None, inheritance:bool = False) -> list[Component]:
        '''Returns all components tied to this GameObject that are of _type
        
        Parameters
        ----------
        _type: type
            the type that this method is supposed to check for
        inheritance: bool
            wether types derived from _type should be included
        '''
        if _type is None:
            return self._components
        ret = [c for c in self._components if not inheritance and type(c)==_type or inheritance and issubclass(type(c), _type)]
        return ret
    
    def get_component(self, _type: type,  inheritance:bool = False) -> Component | None:
        '''Returns the first component of a _type that is tied to this GameObject
        
        Useful when you are sure there is only one component of a given type (ex. a Transform)

        Parameters
        ----------
        _type: type
            the type that this method is supposed to check for
        inheritance: bool
            wether types derived from _type should be included
        '''
        for comp in self._components:
            if type(comp) == _type or inheritance and issubclass(type(comp), _type):
                return comp
        return None

    def init(self) -> None:
        '''calls the init method of all tied Scripts'''
        self._scripts = self.get_components(Script, True)
        for script in self._scripts:
            script.init() #type:ignore

    def update(self, delta_time) -> None:
        '''calls the update method of all tied Scripts'''
        for script in self._scripts:
            script.update(delta_time) #type: ignore
    
    def on_event(self, event) -> None:
        '''calls the on_event method of all tied Scripts'''
        for script in self._scripts:
            script.on_event(event)#type: ignore

    
    def message(self, message: str, *args:Any) -> None:
        '''An interface for an "easy" command system.

        The method iterates over all tied scripts and checks if its type has a method with a name corresponding to the message. If it does, that method is called, with the script as self.
        Any return value from the called method will be promptly ignored.

        Parameters
        ----------
        message: str
            the name of the method to be called
        *args: Any
            arguments to be passed to the method call
        
        Note: incorrectly given args will cause an error
        '''
        for script in self._scripts:
            if message in type(script).__dict__:
                 type(script).__dict__[message](script, *args)
    
    def add_components(self, *components: Component) -> None:
        '''Adds component to self._components and sets itself as their parent'''
        for comp in components:
            comp.set_parent(self)
            self._components.append(comp)
    
    def has_tag(self, tag: str) -> bool:
        '''checks for a tag'''
        return tag in self._tags

    def add_tag(self, tag: str) -> None:
        '''adds a tag'''
        self._tags.add(tag)
    
    def remove_tag(self, tag:str)->None:
        '''removes a tag'''
        self._tags.remove(tag)

    

class Script(Component):
    '''A general class for defining Script objects, which are the main way of defining custom behaviour'''
    def __init__(self, parent: GameObject|None = None):
        Component.__init__(self, parent)
    
    def init(self):
        '''Called only once before anything else
        
        Use this method to do final object preparations. In particular all calls to other objects that could be in __init__, should be here to avoid
        calling objects that do not exist yet.
        '''
        pass

    def update(self, delta_time:float):
        '''Called every frame
        
        This method is responsible for processing the object after a frame.

        Parameters
        ----------
        delta_time:float
            time [in seconds] that was elapsed since the last frame
        '''
        pass

    def on_event(self, _event:event.Event):
        '''Called to handle an event
        '''
        pass




class Transform(Component):
    '''Component that represents logically a position, rotation and scaling of an object

    Attributes
    ----------
    _x, _y: float
        x and y coordinates of the object
    _scale_x, _scale_y: float
        x and y factors of scaling for the object
    _angle: float
        the angle [in degrees] by which the object is rotated counter-clockwise
    '''
    def __init__(self, parent: GameObject | None = None, position: list[float] = [0,0], angle: float = 0., scale: list[float] = [1., 1.]):
        Component.__init__(self, parent)
        self._x, self._y = position
        self._scale_x, self._scale_y = scale
        self._angle = angle

    def get_global(self) -> tuple[float, float, float, float, float]:
        '''Returns the global postition of this Transform
        
        A transform defines its own coordinate system. If another Transform is a Component of a GameObject parented to this Transform's parent, then the child's Transform is treated
        as residing in the parent's coordinate system and its values are relative to it. Crucially, rotation of the parent means rotating its whole coordinate system.

        Returns
        -------
        tuple[float, float, float, float, float]:
            5 float values, in order: x, y, angle, x scale factor, y scale factor
        '''
        root = self._parent
        global_x = self._x
        global_y = self._y
        global_scale_x = self._scale_x
        global_scale_y = self._scale_y
        global_angle = self._angle
        while root != None:
            parent_transform:Transform = root.get_component(Transform)
            

            if parent_transform is not None and parent_transform != self:
                root_tilt = parent_transform._angle * math.pi /180
                root_space_x = global_x*math.cos(root_tilt)-global_y*math.sin(root_tilt)
                root_space_y = global_x*math.sin(root_tilt)+global_y*math.cos(root_tilt)
                global_x = parent_transform._x+root_space_x*parent_transform._scale_x
                global_y = parent_transform._y+root_space_y*parent_transform._scale_y
                global_angle+=parent_transform._angle

                global_scale_x*=parent_transform._scale_x
                global_scale_y*=parent_transform._scale_y
            
            root = root._parent
        
        return global_x, global_y, global_angle, global_scale_x, global_scale_y
    
    def move(self, dx:float = 0, dy:float = 0):
        '''move the transform by dx and dy'''
        self._x+=dx
        self._y+=dy
    
    def rotate(self, angle:float):
        '''rotate this transform clockwise'''
        self._angle+=angle
    
    def scale(self, scale_x = 1., scale_y = 1.):
        '''set this transform's scale'''
        self._scale_x = scale_x
        self._scale_y = scale_y


class Renderable(Transform):
    '''Abstract class representing a resource that can be rendered on a screen.
    
    It is derived from Transform, and as such has position, rotation and scaling attributes. It is however treated as a child of any pure Transform in the same GameObject.

    Attributes
    ----------
    _layer: int
        a numeric value used for drawing order
    '''
    def __init__(self, 
                 parent: GameObject | None= None, 
                 position: list[float] = [0, 0], 
                 angle: float = 0., 
                 scale:list[float] = [1., 1.], 
                 layer: int = 0):
        Transform.__init__(self, parent, position, angle, scale)
        self._layer = layer
    
    def get_resource(self) -> LogicResource:
        '''Returns a LogicResource representing this Renderable'''
        raise NotImplementedError("Base renderable has no resource to render")

class Rectangle(Renderable):
    '''A colored rectangle, go figure
    
    Attributes
    ----------
    _dimensions: tuple[float, float]
        width and height of this rectangle
    _color: tuple[int, int, int] | tuple[int, int, int, int]
        color of this rectangle (supports transparency)
    '''
    def __init__(self, 
                 parent: GameObject | None= None, 
                 dimensions: tuple[float, float] = (100, 100), 
                 color: tuple[int, int, int] | tuple[int, int, int, int] = (0xFF, 0xFF, 0xFF, 0xFF), 
                 position: list[float]= [0.,0.], 
                 angle: float = 0, 
                 layer:int = 0):
        Renderable.__init__(self, parent, position, angle, [1,1], layer)
        self._dimensions = dimensions
        self._color = color
    
    def reshape(self, dimensions:tuple[float, float]):
        '''set the dimensions of this rectangle'''
        self._dimensions = dimensions

    def get_resource(self) -> LogicResource:
        global_position = self.get_global();
        return LogicResource(
            ResourceType.SHAPE, 
            dimensions = self._dimensions,
            scale = global_position[3:],
            color = self._color,
            global_position = global_position[:3],
            layer = self._layer)
    


class Image(Renderable):
    '''A Component representing an Image
    
    Attributes
    ----------
    _path: str
        Path to a source file that this image comes from
    _texture_rect: tuple[int, int, int, int]
        Data used to cut out only a part of the image.
        In order: x and y coordinates of the top left corner of the cutout, its width, and its height
    '''
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
    
    def get_resource(self) -> LogicResource:
        global_position = self.get_global()
        return LogicResource(
            ResourceType.IMAGE, 
            path = self._path,
            scale = global_position[3:],
            global_position = global_position[:3], 
            layer = self._layer,
            rect = self._texture_rect)
    

    
class Hitbox(Component):
    '''A class implementing box collision functionality
    
    Attributes
    ----------
    _top, _left, _bottom, _right: float
        coordinates of the 4 edges of the box
    ALL_BOXES: dict[Scene:list[Hitbox]]
        a dict containig all boxes, separating them by scene in which they were defined
    '''
    ALL_BOXES = {}
    registering_scene:Any|None= None
    def __init__(self, 
                 parent :GameObject |None = None,
                 top: float = 0,
                 left: float = 0,
                 height: float = 1,
                 width: float = 1):
        Component.__init__(self, parent)
        self._top = top
        self._left = left
        self._bottom = top-height
        self._right = left+width
        self._colliding  = []
        if not self in Hitbox.ALL_BOXES[Hitbox.registering_scene]:
            Hitbox.ALL_BOXES[Hitbox.registering_scene].append(self)
    
    def get_global_bounds(self) -> tuple[float, float, float, float]:
        '''Returns the global top, left, bottom and right coordinates of this hitbox '''
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
    def recalculate_collisions(scene):
        '''Recalculates all collisions between boxes in a given scene
        
        Collisions are stored as a list of colliding boxes in each hitbox.
        '''
        boxes:list[Hitbox] = Hitbox.ALL_BOXES[scene]
        for box in boxes:
            box._colliding.clear()
        for i in range(len(boxes)):
            box: Hitbox= boxes[i]
            if not box.is_active():
                continue
            for j in range(i+1, len(boxes)):
                other:Hitbox = boxes[j]
                if not other.is_active():
                    continue
                if box.collides(other):
                    box._colliding.append(other)
                    other._colliding.append(box)
    
    @staticmethod
    def register_scene(scene:Any):
        Hitbox.registering_scene = scene
        if scene not in Hitbox.ALL_BOXES:
            Hitbox.ALL_BOXES[scene] = []
    
    def set_bounds(self, top: float, left: float, height: float, width: float) -> None:
        self._top = top
        self._left = left
        self._right = top-height
        self._bottom = left+width

    def collides(self, other) -> bool:
        me = self.get_global_bounds()
        them = other.get_global_bounds()

        
        x : bool = not (me[1]>them[3] or them[1]>me[3]) #my left past their right or their left past my right
        y : bool = not (me[0]<them[2] or them[0]<me[2]) #my top under their bottom or their top under my bottom

        return x and y


    def get_colliding(self) -> list[Component]:        
        return self._colliding


class Text(Renderable):
    '''A class representing a text to be rendered
    
    Attributes
    ----------
    _text: str
        the text to be rendered
    _font: str
        a path to a .ttf file containing the desired font
    _color: tuple[int, int, int] | tuple[int, int, int, int]
        color of the text(supports transparency)
    _font_size: int
        font size
    default_font: str
        the font used when font is not specified
    '''
    default_font = "resources\\fonts\\04B_30__.TTF"
    def __init__(self, parent:GameObject,                  
                 scale:list[float] = [1., 1.], 
                 position: list[float] = [0, 0], 
                 angle: float = 0, 
                 layer: int = 0,
                 text: str = "",
                 font: str = "",
                 font_size:int = 12,
                 color: tuple[int, int, int] | tuple[int, int, int, int] = (0, 0, 0)):
        Renderable.__init__(self, parent, position, angle, scale, layer)

        self._text = text
        self._font = font
        self._color = color
        self._font_size = font_size
        if self._font == "":
            self._font = Text.default_font
    
    def get_resource(self) -> LogicResource:
        position = self.get_global()
        return LogicResource(ResourceType.TEXT,
                             global_position = position[:3],
                             scale = position[3:],
                             layer = self._layer,
                             text = self._text,
                             font = self._font,
                             color = self._color,
                             size = self._font_size)