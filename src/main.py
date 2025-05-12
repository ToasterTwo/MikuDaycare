from rendering import window
from logic import scene
import pygame
import test_scene as ts

class Game:

    def __init__(self):
        self._window = window.Window((600, 500), "MikuCare")
        self._logic = ts.make()
        self._running = False

    def run(self):
        self._running = True
        clock = pygame.time.Clock()
        while(self._running):
            delta_time = clock.tick()/1000
            inputs = self._window.get_inputs()
            self.do_tick(inputs)
            self._logic.update(delta_time)
            self.render()
        self.exit()

    def do_tick(self, inputs):
        for event in inputs:
            if event.type == pygame.QUIT:
                self._running = False
            else:
                self._logic.on_event(event)
            
    def render(self):
        res = self._logic.get_resources()
        # print(res)
        self._window.render(res)

    def exit(self):
        self._window.quit()
        window.pygame.quit()


if __name__ == "__main__":
    master = Game()
    master.run()
