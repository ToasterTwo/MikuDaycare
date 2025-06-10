from typing import Any
from logic import scene
from pathlib import Path

current_scene: scene.Scene | None= None
next_scene: scene.Scene | None = None
scene_stack:list[scene.Scene] = []
scenes:dict[str, scene.Scene] = {}

def set_current_scene(scn: scene.Scene):
    global current_scene
    global scene_stack
    global next_scene
    
    if current_scene == scn:
        return
    
    else:    
        next_scene = scn


def update():
    global next_scene
    global current_scene

    if next_scene != current_scene:
        current_scene = next_scene


def load_scene(source: str, alias: str):
    global scenes
    
    scenes[alias] = scene.from_json(source)
    scenes[alias].init()

def set_by_alias(alias:str):
    if alias == ".null":
        set_current_scene(None) #type:ignore
    else:
        set_current_scene(scenes[alias])

def load_scene_set_from_directory(directory:str):
    path = Path.cwd()/directory
    for file in path.glob("*.json"):
        name = file.name.rsplit(".")[0]
        load_scene(file.as_posix(), name)