from logic.game_components import *

class ButtonScript(Script):
    '''
    Script used to easily define a button functionality.
    
    Attributes
    ----------
    _message: str
        message passed to targets on button activation
    _targets: list[GameObject]
        GameObjects that will recieve information about this button being activated
    '''
    
    def __init__(self, parent: GameObject, message: str, targets: list[GameObject]):
        Script.__init__(self, parent)
        self._message = message
        self._targets = targets
    
    def init(self):
        self._hitboxes:list[Hitbox] = self._parent.get_components(Hitbox)
    

    #activated by messages

    def mouse(self, button, down):
        if button == 1 and not down:
            for target in self._targets:
                target.message(self._message)
    
    def menu(self):
        for hitbox in self._hitboxes:
            hitbox._active = False
    
    def unmenu(self):
        for hitbox in self._hitboxes:
            hitbox._active = True