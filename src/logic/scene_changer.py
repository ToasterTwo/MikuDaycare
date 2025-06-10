from logic.game_components import *
import logic.context as context



class SceneChanger(Script):
    derivative_id = 0
    def __init__(self, parent:GameObject, message_mapping:dict[str, str]):

        def scene_switcher_method(name:str):
            def action(self):
                context.set_by_alias(name)
            return action

        #fuck it, let's do it again babieee
        attrs = {}

        for m in message_mapping:
            print(message_mapping[m])
            attrs[m] = scene_switcher_method(message_mapping[m])
        
        classname = ""
        if type(self) != SceneChanger:
            classname = self.__class__.__name__
        else:
            classname = f"MenuScript#{SceneChanger.derivative_id}"
            SceneChanger.derivative_id+=1

        self.__class__ = type.__new__(type, classname, (Script,), attrs)
        Script.__init__(self, parent)
        
    
