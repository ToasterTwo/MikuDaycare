import pygame

class ResourceManager:
    def __init__(self):
        self._source_cache = {}
        self._sprite_cache = {}
        self._tiles_cache = {}
        
    def fetch_image(self, path:str)->pygame.Surface:
        if not path in self._source_cache:
            self._source_cache[path] = pygame.image.load(path)
        
        return self._source_cache[path]
    
    def transform(self, surf: pygame.Surface, scale_by: tuple[float, float], angle: float)->pygame.Surface:
        
        inter = pygame.transform.scale_by(surf, scale_by)
        return pygame.transform.rotate(inter, angle)
        
    
    def cutout_rect(self, surf: pygame.Surface, rect: pygame.rect.Rect)->pygame.Surface:
        hsh = (surf, rect.top, rect.left, rect.bottom, rect.right)
        if not hsh in self._sprite_cache:
            sprite = pygame.Surface(rect.size, pygame.SRCALPHA)
            sprite.blit(surf, (0, 0), rect)

            self._sprite_cache[hsh] = sprite
        
        return self._sprite_cache[hsh]

    def get_tile_box(self, 
                     id: int, 
                     source: str, 
                     rect:pygame.rect.Rect, 
                     grid: tuple[int, int, int, int],
                     size: tuple[int, int]):
        
        if id not in self._tiles_cache:
            
        
            base = self.cutout_rect(self.fetch_image(source), rect)
            x_count, y_count, tile_width, tile_height = grid
            width = tile_width*size[0]
            height = tile_height*size[1]
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            for x in range(size[0]):
                for y in range(size[1]):
                    tile_x, tile_y = x%(x_count-2)+1, y%(y_count-2)+1
                    if x == 0:
                        tile_x = 0
                    elif x == size[0]-1:
                        tile_x = x_count-1
                    
                    if y == 0:
                        tile_y = 0
                    elif y == size[1]-1:
                        tile_y = y_count-1
                    surf.blit(
                        self.cutout_rect(base, pygame.rect.Rect(tile_x*tile_width, tile_y*tile_height, tile_width, tile_height)),
                        (x*tile_width, y*tile_height))
            self._tiles_cache[id] = surf
            
        return self._tiles_cache[id]
    
    def fetch_font(self, font_source: str, font_size: int)->pygame.font.Font:
        full_name = font_source+":"+str(font_size)
        if full_name not in self._source_cache:
            self._source_cache[full_name] = pygame.font.Font(font_source, font_size)
        
        return self._source_cache[full_name]

    def render_text(self, text: str, color:tuple[int, ...], font_source: str, font_size)->pygame.surface.Surface:
        font = self.fetch_font(font_source, font_size)
        return font.render(text, False, color)


manager = ResourceManager()
        
        
        