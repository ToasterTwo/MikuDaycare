'''
A module serving as a way to easily manage multiple scenes. 

The whole module should be treated as a singular instance of a hypothetical context class.

Attributes
----------
current_scene: Scene
    self explanatory

next_scene: Scene
    this scene will be placed as the current scene after update is called

scenes: dict[str, Scene]
    a dict correlating each loaded scene with its alias. The alias of a scene is the name of its .json file without the extension
    
global_vars: dict[str, Any]
    a dict used for cross-scene variable passing


Functions
---------
set_current_scene(scene)
    schedules a scene switch

update()
    executes a scheduled scene switch

load_scene(source, alias)
    loads a scene from the path given as the source and saves it in the scenes dict under alias

set_by_alias(alias)
    same as set_current_scene, except takes the scene's alias.

load_scene_set_from_directory(directory)
    loads all the .json files from directory as scenes
'''

from typing import Any
from logic import scene
from pathlib import Path

current_scene: scene.Scene | None= None
next_scene: scene.Scene | None = None
scenes:dict[str, scene.Scene] = {}

global_vars:dict[str, Any] = {}

def set_current_scene(scn: scene.Scene):
    '''
    Schedules a scene change
    '''
    global current_scene
    global next_scene
    
    if current_scene == scn:
        return
    
    else:    
        next_scene = scn


def update():
    '''
    Executes a scene change if the next scene is not the current scene
    '''
    global next_scene
    global current_scene

    if next_scene != current_scene:
        current_scene = next_scene


def load_scene(source: str, alias: str):
    '''
    Loads a scene from source under alias

    Source must be a path to a .json file. Alias can be any string.
    '''
    global scenes
    
    scenes[alias] = scene.from_json(source)
    scenes[alias].init()

def set_by_alias(alias:str):
    '''
    Calls set_current_scene with the scene assigned to alias.

    Alias ".null" is tied to a None object. Switching to it effectively means program termination.
    '''
    if alias == ".null":
        set_current_scene(None) #type:ignore
    else:
        set_current_scene(scenes[alias])

def load_scene_set_from_directory(directory:str):
    '''
    loads all .json files from a given directory

    giving it a directory with .json files that arent's scene descriptors will result in undefined behaviour when attempting a load.
    '''
    path = Path.cwd()/directory
    for file in path.glob("*.json"):
        name = file.name.rsplit(".")[0]
        load_scene(file.as_posix(), name)