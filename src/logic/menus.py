from logic.game_components import *

class MenuScript(Script):
    derivative_id = 0
    def __init__(self, parent: GameObject, activate_messages:list[str], deactivate_messages:list[str], menu_elements:list[Component]):
        
        #pretty sure this is evil but what the hell
        attrs = {}
        for m in activate_messages:
            attrs[m] = MenuScript.activate
        
        for m in deactivate_messages:
            attrs[m] = MenuScript.deactivate
        
        classname = ""
        if type(self) != MenuScript:
            classname = self.__class__.__name__
        else:
            classname = f"MenuScript#{MenuScript.derivative_id}"
            MenuScript.derivative_id+=1

        self.__class__ = type.__new__(type, classname, (Script,), attrs)

        Script.__init__(self, parent)
        self._menu_elements = menu_elements

    def activate(self):
        for element in self._menu_elements: #type:ignore
            element._active = True 

    def deactivate(self):
        for element in self._menu_elements: #type:ignore
            element._active = False 