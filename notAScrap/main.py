import pyxel, os, random

SPRITEBANK = 0
TILE_SIZE = 8
WIDTH = 256
HEIGHT = 256

CAMERA_WIDTH = 256
CAMERA_HEIGHT = 256

class App:
    def __init__(self):
        os.system('cls')
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
    GROUND = (0,2)
    WALL = (0,0)

    TILES = [GROUND, WALL]

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

        last_down = False
        X_tile = CAMERA_WIDTH//16 - 2
        Y_tile = 0
        W_rect = 3
        H_rect = 3
        rect_append(self.world_map, X_tile, 0, 3, 3)
        for i in range(25):              #need fis prolly wipe need sleep now
            if last_down:
                sq_pos = random.randint(0,2)
                if sq_pos == 0 and X_tile>0:
                    self.world_map[Y_tile+H_rect//2+1][X_tile-H_rect//2+1] = (9,2)
                    X_tile -= 4
                    last_down = False
                elif sq_pos == 1 and X_tile<CAMERA_WIDTH:
                    self.world_map[Y_tile+H_rect//2+1][X_tile+W_rect] = (9,2)
                    X_tile += 4
                    last_down = False
                else:
                    self.world_map[Y_tile+H_rect][X_tile+W_rect//2+1] = (9,3) 
                    Y_tile += 4 
            else:
                self.world_map[Y_tile+H_rect][X_tile+W_rect//2+1] = (9,3)
                Y_tile += 4 
                last_down = True

            W_rect = random.randint(3,9)
            H_rect = random.randint(3,9)
            rect_append(self.world_map, X_tile ,Y_tile,W_rect,H_rect)
            
def rect_append(tab, x, y, w, h):
    for in_y in range(h):
        for in_x in range(w):
            tab[y+in_y][x+in_x] = WorldItem.GROUND


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
