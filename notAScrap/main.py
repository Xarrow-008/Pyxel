import pyxel

SPRITEBANK = 0
TILE_SIZE = 8
WIDTH = 256
HEIGHT = 256

CAMERA_WIDTH = 128
CAMERA_HEIGHT = 128

class App:
    def __init__(self):
        pyxel.init(CAMERA_WIDTH, CAMERA_HEIGHT, title="Not a scrap")
        pyxel.load("../notAScrap.pyxres")
        
        self.world = World(pyxel.tilemaps[0])

        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            print("reset")

    def draw(self):
        pyxel.cls(0)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                tile = self.world.world_map[y][x]
                draw_tile(pyxel, x, y, tile)

class WorldItem:
    PLAYER = (0,4)
    BLOCK = (0,2)
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

App()
