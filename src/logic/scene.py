from logic.game_components import *
from enum import Enum
from logic.logic_resource import *

class Scene:
    def __init__(self):
        self._objects: list[GameObject] = []

    def add_objects(self, *objects):
        for obj in objects:
            self._objects.append(obj)
    
    def update(self, delta_time: float):
        for obj in self._objects:
            obj.update(delta_time)
    
    def on_event(self, event):
        for obj in self._objects:
            obj.on_event(event)
    
    def get_resources(self):
        resources = []
        for obj in self._objects:
            for comp in obj.get_components():
                if type(comp) == Image:
                    resources.append(LogicResource.of_image(comp))
                
                elif type(comp) == Rectangle:
                    resources.append(LogicResource.of_shape(comp))

        return tuple(resources)

