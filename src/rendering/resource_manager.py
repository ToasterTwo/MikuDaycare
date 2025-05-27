import pygame

class ResourceManager:
    def __init__(self):
        self._image_cache = {}
        self._translation_cache = {}
        self._sprite_cache = {}
        
    def fetch_image(self, path:str)->pygame.Surface:
        if not path in self._image_cache:
            self._image_cache[path] = pygame.image.load(path)
        
        return self._image_cache[path]
    
    def transform(self, surf: pygame.Surface, scale_by: tuple[float, float], angle: float)->pygame.Surface:
        if not (surf, scale_by, angle) in self._translation_cache:
            
            inter = pygame.transform.scale_by(surf, scale_by)

            self._translation_cache[(surf, scale_by, angle)] = pygame.transform.rotate(inter, angle)
        
        return self._translation_cache[(surf, scale_by, angle)]
    
    def cutout_rect(self, surf: pygame.Surface, rect: pygame.rect.Rect):
        hsh = (surf, rect.top, rect.left, rect.bottom, rect.right)
        if not hsh in self._sprite_cache:
            sprite = pygame.Surface(rect.size, pygame.SRCALPHA)
            sprite.blit(surf, (0, 0), rect)

            self._sprite_cache[hsh] = sprite
        
        return self._sprite_cache[hsh]

manager = ResourceManager()
        
        
        