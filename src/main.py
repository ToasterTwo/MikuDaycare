from rendering import window
import pygame
import test_scene as ts
from logic import context

class Game:

    def __init__(self):
        self._window = window.Window((400, 600), "Miku Petting Sim")
        self._running = False

    def run(self):
        context.load_scene_set_from_directory(r"resources\scenes")
        context.set_by_alias("main")
        
        self._running = True
        clock = pygame.time.Clock()
        while(self._running):
            context.update()
            if context.current_scene is None:
                break

            delta_time = clock.tick()/1000
            inputs = self._window.get_inputs()
            self.do_tick(inputs)
            context.current_scene.update(delta_time)
            self.render()
        self.exit()

    def do_tick(self, inputs):
        for event in inputs:
            if event.type == pygame.QUIT:
                self._running = False
            else:
                if context.current_scene is not None:
                    context.current_scene.on_event(event)
            
    def render(self):
        if context.current_scene is not None:
            res = context.current_scene.get_resources()
            self._window.render(res)

    def exit(self):
        self._window.quit()
        window.pygame.quit()


if __name__ == "__main__":
    master = Game()
    master.run()
