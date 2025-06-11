from logic.game_components import *
from enum import Enum
from logic.logic_resource import *
import json

class Scene:
    '''A class representing some collection of game objects, responsible for managing them'''
    def __init__(self):
        self._objects: list[GameObject] = []

    def add_objects(self, *objects):
        for obj in objects:
            self._objects.append(obj)
    
    def update(self, delta_time: float):
        '''Called every frame'''
        Hitbox.recalculate_collisions(self)
        for obj in self._objects:
            if obj._active:
                obj.update(delta_time)
    
    def on_event(self, event):
        for obj in self._objects:
            if obj._active:
                obj.on_event(event)
    
    def init(self):
        '''called once on the start'''
        for obj in self._objects:
            obj.init()
    
    def get_resources(self) -> tuple[LogicResource, ...]:
        '''returns all resources to be rendered this frame'''
        resources = []
        for obj in self._objects:
            if not obj._active:
                continue
            for comp in filter(lambda o: o._active, obj.get_components()):
                if isinstance(comp, Renderable):
                    resources.append(comp.get_resource())
                
                # elif type(comp) == Hitbox:
                #     global_bounds = comp.get_global_bounds()
                #     gx = (global_bounds[1]+global_bounds[3])/2
                #     gy = (global_bounds[0]+global_bounds[2])/2
                #     resources.append(LogicResource(
                #         ResourceType.SHAPE, 
                #         dimensions = [global_bounds[3]-global_bounds[1], global_bounds[0]-global_bounds[2]],
                #         scale = [1, 1],
                #         color = [0x00, 0xff, 0x00, 0x33],
                #         global_position = [gx, gy, 0],
                #         layer = 100
                #         ))

        return tuple(resources)




def from_json(filepath:str):
    '''Constructs a Scene object from a .json style description'''


    scene = Scene()
    Hitbox.register_scene(scene)

    parsed = None
    with open(filepath, mode="r",encoding="UTF-8") as file:
        parsed = json.loads(file.read())

    object_dict: dict[str, Any] = {}
    object_dict.clear()
    objects = []
    objects.clear()

    for o in parsed:
        parent_name : str = parsed[o]["Parent"]
        parent: GameObject | None = None
        if parent_name in object_dict:
            parent = object_dict[parent_name]
        tags = []
        if "Tags" in parsed[o]:
            tags = parsed[o]["Tags"]
        
        object_dict[o] = GameObject(parent = parent, tags=tags)
        if "Active" in parsed[o]:
            object_dict[o]._active = parsed[o]["Active"] > 0
        
        objects.append(object_dict[o])
    
    def substitute_args(args:list[Any])->tuple[list[Any], bool]:
        substituted = []
        is_incomplete = False
        for something in args:
            if type(something) == str and something in object_dict:
                    if object_dict[something] is None:
                        is_incomplete = True
                    substituted.append(object_dict[something])
            elif type(something) == list:
                sub_args, sub_incomplete = substitute_args(something)
                substituted.append(sub_args)
                is_incomplete = sub_incomplete or is_incomplete
            elif type(something) == dict:
                sub_kwargs, sub_incomplete = substitute_kwargs(something)
                substituted.append(sub_kwargs)
                is_incomplete = sub_incomplete or is_incomplete
            else:
                substituted.append(something)
        
        return substituted, is_incomplete
    
    def substitute_kwargs(kwargs:dict[str, Any])->tuple[dict[str, Any], bool]:
        substituted = {}
        is_incomplete = False
        for something in kwargs:
            value = kwargs[something]
            if type(value) == str and value in object_dict:
                    if object_dict[value] is None:
                        is_incomplete = True
                    substituted[something]=object_dict[value]
            elif type(value) == list:
                substituted[something], sub_incomplete = substitute_args(value)
                is_incomplete = sub_incomplete or is_incomplete
            elif type(value) == dict:
                substituted[something], sub_incomplete = substitute_kwargs(value)
                is_incomplete = sub_incomplete or is_incomplete

            else:
                substituted[something] = value
        
        return substituted, is_incomplete
                    
    
    incomplete = []
    incomplete.clear()
    for o in parsed:
        for comp in parsed[o]["Components"]:
            comp["Name"] = o+"."+comp["Name"] # type: ignore
            object_dict[comp["Name"]] = None

    for o in parsed:
        for comp in parsed[o]["Components"]:
            args, incomplete_args = substitute_args(comp["args"])
            kwargs, incomplete_kwargs = substitute_kwargs(comp["kwargs"])

            if incomplete_args or incomplete_kwargs:
                incomplete.append(comp)
            
            comp_obj :Component= Component.from_name(comp["Type"], object_dict[o], *args, **kwargs)
            if "Active" in comp:
                comp_obj._active = comp["Active"] > 0
            object_dict[comp["Name"]] = comp_obj
            object_dict[o].add_components(comp_obj)
            
    
    for revisited in incomplete:
        args, still_incopmplete_args = substitute_args(revisited["args"])
        
        kwargs, still_incopmplete_kwargs = substitute_kwargs(revisited["kwargs"])

        if still_incopmplete_args or still_incopmplete_kwargs:
            raise ValueError("Unable to complete an object")
        
        revisited_obj = object_dict[revisited["Name"]]
        Component.NAME_MAP[revisited["Type"]].__init__(revisited_obj, revisited_obj._parent, *args, **kwargs)
    
    scene.add_objects(*objects)

    return scene


