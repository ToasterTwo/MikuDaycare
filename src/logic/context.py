from typing import Any
from logic import scene

current_scene: scene.Scene | None= None
scene_stack:list[scene.Scene] = []
scene_list: list[scene.Scene] = []

def set_current_scene(scn: scene.Scene):
    global current_scene
    global scene_stack
    global scene_list
    
    if current_scene == scn:
        return
    
    if scn not in scene_list:
        scene_list.append(scn)
    
    scene_stack.append(scn)
    current_scene = scn