import pygame
try:
    from rendering.resource_manager import manager
except ModuleNotFoundError:
    from resource_manager import manager
from logic import logic_resource as lr

class Window:
    def __init__(self, size:tuple[int], title: str):
        if not pygame.get_init():
            pygame.init()

        self._window = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

    def quit(self):
        pygame.display.quit()
    
    def render(self, objects: lr.LogicResource):
        self._window.fill((0, 0, 0))
        
        for obj in objects:
            match obj._type:
                case lr.ResourceType.IMAGE:
                    self._window.blit(manager.fetch_image(obj._data["path"]), obj._data["global_position"][:2])
                
                case lr.ResourceType.SHAPE:
                    center_x, center_y = obj._data["global_position"][:2]
                    width, height = obj._data["dimensions"]
                    scale_x, scale_y = obj._data["scale"]
                    width *= scale_x
                    height*= scale_y
                    shape = pygame.Rect(center_x-width/2, center_y-height/2, width, height)
                    pygame.draw.rect(self._window, obj._data["color"], shape)

        pygame.display.update()

    def get_inputs(self):
        return pygame.event.get()