from logic.game_components import *
from enum import Enum
from logic.logic_resource import *
import json

class Scene:
    def __init__(self):
        self._objects: list[GameObject] = []

    def add_objects(self, *objects):
        for obj in objects:
            self._objects.append(obj)
    
    def update(self, delta_time: float):
        Hitbox.recalculate_collisions()
        for obj in self._objects:
            obj.update(delta_time)
    
    def on_event(self, event):
        for obj in self._objects:
            obj.on_event(event)
    
    def get_resources(self) -> tuple[LogicResource, ...]:
        resources = []
        for obj in self._objects:
            for comp in obj.get_components():
                if type(comp) == Image:
                    resources.append(LogicResource.of_image(comp))
                
                elif type(comp) == Rectangle:
                    resources.append(LogicResource.of_shape(comp))
                
                elif type(comp) == Hitbox:
                    global_bounds = comp.get_global_bounds()
                    gx = (global_bounds[1]+global_bounds[3])/2
                    gy = (global_bounds[0]+global_bounds[2])/2
                    resources.append(LogicResource(
                        ResourceType.SHAPE, 
                        dimensions = [global_bounds[3]-global_bounds[1], global_bounds[2]-global_bounds[0]],
                        scale = [1, 1],
                        color = [0x00, 0xff, 0x00, 0xf0],
                        global_position = [gx, gy],
                        layer = 11
                        ))

        return tuple(resources)


def from_json(filepath:str):
    parsed = None
    with open(filepath, mode="r",encoding="UTF-8") as file:
        parsed = json.loads(file.read())

    object_dict: dict[str, Any] = {}
    objects = []
    for o in parsed:
        parent_name : str = parsed[o]["Parent"]
        parent: GameObject | None = None
        if parent_name in object_dict:
            parent = object_dict[parent_name]
        
        object_dict[o] = GameObject(parent = parent)
        objects.append(object_dict[o])
    
    incomplete = []
    for o in parsed:
        for comp in parsed[o]["Components"]:
            comp["Name"] = o+"."+comp["Name"] # type: ignore
            object_dict[comp["Name"]] = None

    for o in parsed:
        for comp in parsed[o]["Components"]:
            args = comp["args"][:]
            for i in range(len(args)):
                if type(args[i]) == list:
                    continue
                if args[i] in object_dict:
                    requested = object_dict[args[i]]
                    if requested is None:
                        incomplete.append(comp)
                    args[i] = requested
            
            kwargs = comp["kwargs"].copy()
            for a in kwargs:
                if type(kwargs[a]) == list:
                    continue

                if kwargs[a] in object_dict:
                    requested = object_dict[kwargs[a]]
                    if requested is None:
                        incomplete.append(comp)
                    kwargs[a] = requested
            
            comp_obj = Component.from_name(comp["Type"], object_dict[o], *args, **kwargs)
            object_dict[comp["Name"]] = comp_obj
            object_dict[o].add_components(comp_obj)
            
    
    for revisited in incomplete:
        args = revisited["args"]
        for i in range(len(args)):
            if args[i] in object_dict:
                if type(args[i]) == list:
                    continue
                args[i] = object_dict[args[i]]
        
        kwargs = revisited["kwargs"]
        for a in kwargs:
            if type(kwargs[a]) == list:
                    continue
            if kwargs[a] in object_dict:
                kwargs[a] = object_dict[kwargs[a]]

        
        revisited_obj = object_dict[revisited["Name"]]
        revisited_obj.__init__(revisited_obj._parent, *args, **kwargs)
    
    scene = Scene()
    scene.add_objects(*objects)

    return scene


