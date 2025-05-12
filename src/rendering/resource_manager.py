import pygame

class ResourceManager:
    def __init__(self):
        self._cache = {}
    
    def fetch_image(self, path:str):
        if not path in self._cache:
            self._cache[path] = pygame.image.load(path)
        
        return self._cache[path]


manager = ResourceManager()
        
        
        