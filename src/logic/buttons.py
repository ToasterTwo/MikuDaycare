from logic.game_components import *

class ButtonScript(Script):
    def __init__(self, parent: GameObject, message: str, *targets: GameObject):
        Script.__init__(self, parent)
        self._message = message
        self._targets = targets
    
    def mouse(self, button, down):
        if button == 1 and down:
            for target in self._targets:
                target.message(self._message)