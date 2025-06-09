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
        pygame.mouse.set_visible(False)

    def quit(self):
        pygame.display.quit()
    
    def render(self, objects: tuple[lr.LogicResource, ...]):
        self._window.fill((0, 0, 0))
        
        for obj in sorted(objects, key = lambda o: o.layer):
            match obj._type:
                case lr.ResourceType.IMAGE:
                    base = manager.fetch_image(obj.path)
                    top, left, width, height = obj.rect
                    pos = obj.global_position[:2]
                    if height < 0:
                        height = base.get_height()
                    if width < 0:
                        width = base.get_width()
                    
                

                    text_rect = pygame.Rect(top, left, width, height)
                    sprite = manager.cutout_rect(base, text_rect)
                    img = manager.transform(sprite, obj.scale, obj.global_position[2])

                    pos = (pos[0]-img.get_rect().width/2, 
                           self._window.get_height()-pos[1]-img.get_rect().height/2)

                    self._window.blit(img, pos, img.get_rect())
                    # pygame.draw.circle(self._window, (0x00, 0xFF, 0x00), (pos[0], pos[1]), 1.5)
                
                case lr.ResourceType.SHAPE:
                    center_x, center_y = obj.global_position[:2]
                    width, height = obj.dimensions
                    scale_x, scale_y = obj.scale
                    width *= scale_x
                    height*= scale_y
                    shape = pygame.Rect(center_x-width/2, self._window.get_height()-center_y-height/2, width, height)
                    shape_surf = pygame.Surface(shape.size, pygame.SRCALPHA)
                    shape_surf = pygame.transform.rotate(shape_surf, obj.global_position[2])
                    pygame.draw.rect(shape_surf, obj.color, shape_surf.get_rect())
                    self._window.blit(shape_surf, shape)
                
                case lr.ResourceType.TILES:
                    image = manager.get_tile_box(
                        obj.id, obj.source, 
                        pygame.rect.Rect(*obj.rect), obj.grid, obj.shape)
                    
                    image = manager.transform(image, obj.scale, obj.global_position[2])
                    pos = obj.global_position[:2]
                    pos = (pos[0]-image.get_rect().width/2, 
                           self._window.get_height()-pos[1]-image.get_rect().height/2)

                    self._window.blit(image, pos, image.get_rect())

                case lr.ResourceType.TEXT:
                    image = manager.render_text(obj.text, obj.color, obj.font, obj.size)
                    image = manager.transform(image, obj.scale, obj.global_position[2])
                    pos = obj.global_position[:2]
                    pos = (pos[0]-image.get_rect().width/2, 
                           self._window.get_height()-pos[1]-image.get_rect().height/2)

                    self._window.blit(image, pos, image.get_rect())


        pygame.display.flip()

    def get_inputs(self):
        return pygame.event.get()