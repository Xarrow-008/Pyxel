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
        X_room = CAMERA_WIDTH//16 - 2
        Y_room = 0
        new_X_room = 0
        new_Y_room = 0
        new_W_room = 0
        new_H_room = 0
        W_rect = 3
        H_rect = 3
        path = 0
        X_connect = 0
        Y_connect = 0
        connect_type = (9,2)
        self.rooms = [{'path':[0],'name':0,'X':X_room,'Y':Y_room}]
        rect_append(self.world_map, X_room, Y_room, 3, 3)
        for i in range(25):
            new_W_room = random.randint(3,9)
            new_H_room = random.randint(3,9)
            if last_down:
                sq_pos = random.randint(0,2)
                if sq_pos == 0 and X_room>0:
                    X_connect,Y_connect = on_mid_side(X_room,Y_room,0,H_rect)
                    connect_type = (9,2)
                    new_X_room = X_room - 1 - new_W_room
                    new_Y_room = Y_room
                elif sq_pos == 1 and X_room<CAMERA_WIDTH-9:
                    X_connect,Y_connect = on_mid_side(X_room,Y_room,W_rect,H_rect)
                    connect_type = (9,2)
                    new_X_room = X_room - 1 - new_W_room #no
                    new_Y_room = Y_room

                else:
                    Y_connect,X_connect = on_mid_side(Y_room,X_room,H_rect,W_rect)
                    connect_type = (9,3)
                    
            else:
                Y_connect,X_connect = on_mid_side(Y_room,X_room,H_rect,W_rect)
                connect_type = (9,3)
            self.world_map[Y_connect][X_connect] = connect_type
                    
            
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
def on_mid_side(posconst,poshlf,constant,halfed):
    return posconst+constant,poshlf+hlf(halfed)

def hlf(nb):
    return nb//2+1

App()
