import pygame
try:
    from rendering.resource_manager import manager
except ModuleNotFoundError:
    from resource_manager import manager
from logic import logic_resource as lr

class Window:
    def __init__(self, size:tuple[int, int], title: str):
        if not pygame.get_init():
            pygame.init()

        self._window = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

    def quit(self):
        pygame.display.quit()
    
    def render(self, objects: tuple[lr.LogicResource, ...]):
        self._window.fill((0, 0, 0))
        
        for obj in sorted(objects, key = lambda o: o.layer):
            match obj._type:
                case lr.ResourceType.IMAGE:
                    img = manager.fetch_image(obj.path)
                    top, left, width, height = obj.rect
                    pos = obj.global_position[:2]
                    if height < 0:
                        height = img.get_height()
                        pos[1]-=height/2
                    if width < 0:
                        width = img.get_width()
                        pos[0]-=width/2


                    text_rect = pygame.Rect(top, left, width, height)
                    self._window.blit(img, pos, text_rect)
                    # pygame.draw.circle(self._window, (0x00, 0xFF, 0x00), (pos[0], pos[1]), 1.5)
                
                case lr.ResourceType.SHAPE:
                    center_x, center_y = obj.global_position[:2]
                    width, height = obj.dimensions
                    scale_x, scale_y = obj.scale
                    width *= scale_x
                    height*= scale_y
                    shape = pygame.Rect(center_x-width/2, center_y-height/2, width, height)
                    shape_surf = pygame.Surface(shape.size, pygame.SRCALPHA)
                    pygame.draw.rect(shape_surf, obj.color, shape_surf.get_rect())
                    self._window.blit(shape_surf, shape)

        pygame.display.flip()

    def get_inputs(self):
        return pygame.event.get()