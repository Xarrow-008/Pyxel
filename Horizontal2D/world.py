SPRITEBANK = 0
TILE_SIZE = 8
WIDTH = 256
HEIGHT = 256

class WorldItem:
    PLAYER = (0,1)
    BLOCK = (1,0)
    BACKGROUND = (0,0)

    TILES = [BLOCK, BACKGROUND]

class World:

    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.world_map = []
        self.player_init_pos_x = 0
        self.player_init_pos_y = 0
        for y in range(HEIGHT):
            self.world_map.append([])
            for x in range(WIDTH):
                for tile in WorldItem.TILES:
                    if self.tilemap.pget(x,y) == tile:
                        self.world_map[y].append(tile)
                if self.tilemap.pget(x,y) == WorldItem.PLAYER:
                    self.player_init_pos_x = x
                    self.player_init_pos_y = y
                    self.world_map[y].append(WorldItem.BACKGROUND)

    
def draw_tile(pyxel, x, y, tile):
    pyxel.blt(x*TILE_SIZE,
                y*TILE_SIZE,
                SPRITEBANK,
                tile[0]*TILE_SIZE,
                tile[1]*TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
                )