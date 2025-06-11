import logic.game_components as gc

class SpriteController(gc.Script):
    '''Script used for changing texture rects of a given image.
    
    Attributes
    ----------
    _sprite: Image
        the image this will operate on
    _grid: tuple[int, int]
        definition of an n x m grid of euqally sized image cutouts. One cell is the size of _sprite
    _origin: tuple[int, int]
        grid origin point on the source image, the top left corner of the grid area
    _current_id: int
        the id of the currenmt sprite
    '''
    def __init__(self, parent: gc.GameObject, sprite: gc.Image, sprite_grid: tuple[int, int], origin: tuple[int, int]):
        gc.Script.__init__(self, parent)
        self._sprite = sprite
        self._grid = sprite_grid
        self._max_sprite = sprite_grid[0]*sprite_grid[1]
        self._origin = origin
        self._current_id = 0

    def switch_sprite(self, id):
        '''Changes _sprite's texture_rect attribute to cover a different cell'''
        if id == self._current_id:
            return
        
        w, h = self._sprite._texture_rect[2:]
        if id > self._max_sprite:
            id = id%self._max_sprite
        
        row = id//self._grid[1]
        column = id%self._grid[0]

        if self._grid[1] == 1:
            row = 0
        if self._grid[0] == 1:
            column = 0

        self._sprite._texture_rect = (self._origin[0]+column*w, self._origin[1]+row*h, w, h)
        self._current_id = id