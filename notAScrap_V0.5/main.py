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

        print(do_rooms_cross(self.world_map,4,10,3,3))
        if(not do_rooms_cross(self.world_map,4,10,3,3)):
            rect_append(self.world_map,4,10,3,3)
        
        last_down = False
        X_room = CAMERA_WIDTH//16 - 2
        Y_room = 0
        W_room = 3
        H_room = 3
        new_X_room = 0
        new_Y_room = 0
        new_W_room = 0
        new_H_room = 0
        path = 0
        X_connect = 0
        Y_connect = 0
        connect_type = (9,2)
        rect_append(self.world_map, X_room, Y_room, W_room, H_room)
        self.rooms = [{'path':[0],'name':0,'X':X_room,'Y':Y_room}]
        for i in range(25):
            new_W_room = random.randint(3,9)
            new_H_room = random.randint(3,9)
            if last_down:
                sq_pos = random.randint(0,2)
                if sq_pos == 0 and X_room>0:
                    X_connect,Y_connect = on_mid_side(X_room-1,Y_room,0,H_room)
                    connect_type = (9,2)
                    new_X_room = X_room - 1 - new_W_room
                    new_Y_room = Y_connect - random.randint(0,new_H_room-1)
                    last_down = False
                elif sq_pos == 1 and X_room<WIDTH-9:
                    X_connect,Y_connect = on_mid_side(X_room,Y_room,W_room,H_room)
                    connect_type = (9,2)
                    new_X_room = X_room + W_room + 1
                    new_Y_room = Y_connect - random.randint(0,new_H_room-1)
                    last_down = False
                else:
                    Y_connect,X_connect = on_mid_side(Y_room,X_room,H_room,W_room)
                    connect_type = (9,3)
                    new_X_room = X_connect - random.randint(0,new_W_room-1)
                    new_Y_room = Y_room + H_room + 1
                    last_down = True
            else:
                Y_connect,X_connect = on_mid_side(Y_room,X_room,H_room,W_room)
                connect_type = (9,3)
                new_X_room = X_connect - random.randint(0,new_W_room-1)
                new_Y_room = Y_room + H_room + 1
                last_down = True
            
            self.world_map[Y_connect][X_connect] = connect_type
            rect_append(self.world_map,new_X_room,new_Y_room,new_W_room,new_H_room)
            X_room, Y_room, W_room, H_room = new_X_room, new_Y_room, new_W_room, new_H_room
            

def do_rooms_cross(world,x, y, w, h):
        for in_y in range(h):
            for in_x in range(w+2):
                if world[y-1+in_y][x-1+in_x] == WorldItem.GROUND:
                    return True
        return False


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
    return posconst+constant,poshlf+halfed//2


App()
