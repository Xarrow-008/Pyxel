import pyxel

SPRITEBANK = 0
TILE_SIZE = 8
WIDTH = 256
HEIGHT = 256

CAMERA_WIDTH = 128
CAMERA_HEIGHT = 128

class App:
    def __init__(self):
        pyxel.init(CAMERA_WIDTH, CAMERA_HEIGHT, title="Roguelike")
        pyxel.load("../roguelike.pyxres")
        
        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world)

        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):

        self.player.update()

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.world = World(pyxel.tilemaps[0])
            self.player = Player(self.world)

    def draw(self):
        pyxel.cls(0)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                tile = self.world.world_map[y][x]
                draw_tile(pyxel, x, y, tile)

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
    
class Player:
    def __init__(self, world):
        self.x = 0
        self.y = 0
        self.world = world
        self.physics = Physics

    def update(self):
        print("update")

class Physics:
    def __init__(self):
        self.speed = 0

    def move(self, movements):
        new_x = self.x + self.speed*movements[0]
        new_y = self.y + self.speed*movements[1]
        
        new_tile_x = self.tile_x + pyxel.sgn(movements[0])
        new_tile_y = self.tile_y + pyxel.sgn(movements[1])

        next_tile_1 = self.world.world_map[new_tile_y][new_tile_x]
        next_tile_2 = self.world.world_map[new_tile_y+abs(pyxel.sgn(movements[0]))][new_tile_x+abs(pyxel.sgn(movements[1]))]

        if (next_tile_1 != WorldItem.WALL or not collision(new_x, new_y, new_tile_x*TILE_SIZE, new_tile_y*TILE_SIZE)) and (next_tile_2 != WorldItem.WALL or not collision(new_x, new_y, (new_tile_x+abs(direction[1]))*TILE_SIZE, (new_tile_y+abs(direction[0]))*TILE_SIZE)):
            self.x = new_x
            self.y = new_y
    
    def collision(x1,y1,x2,y2):
        return x1+TILE_SIZE>x2 and x2+TILE_SIZE>x1 and y1+TILE_SIZE>y2 and y2+TILE_SIZE>y1


App()
