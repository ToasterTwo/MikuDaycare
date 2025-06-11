from logic.game_components import *
import logic.context as context



class SceneChanger(Script):
    '''A class for easily defining scene changes triggered by messages

    Similarly to MenuScript, this requires creating sister classes to work with the message API. This is done here the same way as it is in MenuScript:
    the constructor creates a new SceneChanger#[id] class and switches the initialized object's __class__ attribute to it. The derived classes map messages to 
    scene aliases. 
    '''
    derivative_id = 0
    def __init__(self, parent:GameObject, message_mapping:dict[str, str]):
        '''Create or reinitialize a new SceneChanger#[id] object

        Parameters
        ----------
        message_mapping: dict[str, str]
            mapping between messages and scene aliases
        '''
        def scene_switcher_method(name:str):
            def action(self):
                context.set_by_alias(name)
            return action

        #fuck it, let's do it again babieee
        attrs = {}

        for m in message_mapping:
            attrs[m] = scene_switcher_method(message_mapping[m])
        
        classname = ""
        if type(self) != SceneChanger:
            classname = self.__class__.__name__
        else:
            classname = f"MenuScript#{SceneChanger.derivative_id}"
            SceneChanger.derivative_id+=1

        self.__class__ = type.__new__(type, classname, (Script,), attrs)
        Script.__init__(self, parent)
        
    
