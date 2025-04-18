
TILE_SIZE = 8
SPRITEBANK = 0

class WorldItem :
    WALL = (1,1)
    CORRIDOR = (0,0)
    PLAYER = (0,1)

    BLOCKS_LIST = [WALL,CORRIDOR]

class World:
    WIDTH = 16
    HEIGHT = 16

    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.world_map = []
        self.player_init_pos_x = 0
        self.player_init_pos_y = 0
        for y in range(self.HEIGHT):
            self.world_map.append([])
            for x in range(self.WIDTH):
                for block in WorldItem.BLOCKS_LIST:
                    if self.tilemap.pget(x,y) == block:
                        self.world_map[y].append(block)
                if self.tilemap.pget(x,y) == WorldItem.PLAYER:
                    self.player_init_pos_x = x
                    self.player_init_pos_y = y
                    self.world_map[y].append(WorldItem.CORRIDOR)

    
def draw_tile(pyxel, x, y, tile):
    pyxel.blt(x*TILE_SIZE,
                y*TILE_SIZE,
                SPRITEBANK,
                tile[0]*TILE_SIZE,
                tile[1]*TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
                )
                    