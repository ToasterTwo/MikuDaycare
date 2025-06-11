from logic.game_components import *
from logic.logic_resource import LogicResource, ResourceType

class TilesetImage(Renderable):
    '''A class for logic representation of a tileset-constructed image
    
    Attributes
    ----------
    _source: str
        a path to the source image
    _rect: tuple[int, int, int, int]
        cutout area containing the tileset
    _grid: tuple[int, int, int, int]
        a grid defining the individual tiles. in order: cells horizontally, cells vertically, cell width, cell height
    _shape: tuple[int, int]
        how many tiles horizontally and vertically will compose this image
    _id: int
        a helper attribute, used by the resource manager to cache constructed tile images
    '''
    __ID__ = 0
    def __init__(self, 
                 parent:GameObject, 
                 source: str,  texture_rect:tuple[int, int, int, int],grid:tuple[int, int, int, int], shape: tuple[int, int],
                 position:list[float] = [0, 0], 
                 angle: float = 0, 
                 scale:list[float]= [1., 1.],
                 layer: int = 0,):
        Renderable.__init__(self, parent, position, angle, scale, layer)
        self._source = source
        self._grid = grid
        self._rect = texture_rect
        self._shape = shape
        self._id = TilesetImage.__ID__
        TilesetImage.__ID__ += 1
    
    def get_resource(self) -> LogicResource:
        pos = self.get_global()
        return LogicResource(ResourceType.TILES,
                             id = self._id,
                             source = self._source,
                             rect = self._rect,
                             global_position = pos[:3],
                             scale = pos[3:],
                             grid = self._grid,
                             shape = self._shape,
                             layer = self._layer)
