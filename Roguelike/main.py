import pyxel

SPRITEBANK = 0
TILE_SIZE = 8
WIDTH = 256
HEIGHT = 256

CAMERA_WIDTH = 128
CAMERA_HEIGHT = 128

class App:
    def __init__(self):
        pyxel.init(CAMERA_WIDTH, CAMERA_HEIGHT, title="Roguelike", fps=120)
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

        pyxel.blt(
            self.player.x,
            self.player.y,
            SPRITEBANK,
            WorldItem.PLAYER[0]*TILE_SIZE,
            WorldItem.PLAYER[1]*TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
            colkey=11
            )

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
        self.physics = Physics(world)
        self.camera = Camera(self)
        self.mousePositionInWorld_x = self.camera.x + pyxel.mouse_x
        self.mousePositionInWorld_y = self.camera.y + pyxel.mouse_y
        self.facing = [1,0]

        self.isDashing = False
        self.dashLength = 20
        self.dashFrame = 0
        self.dashCooldown = 10
        self.dashStrength = self.physics.speed*2.5

    def update(self):

        self.camera.update()

        if not self.isDashing:

            if pyxel.btn(pyxel.KEY_Z):
                self.x, self.y = self.physics.move(self.x, self.y, [0,-1])
                self.facing[1] = -1
            if pyxel.btn(pyxel.KEY_S):
                self.x, self.y = self.physics.move(self.x, self.y, [0,1])
                self.facing[1] = 1
            if pyxel.btn(pyxel.KEY_Q):
                self.x, self.y = self.physics.move(self.x, self.y, [-1,0])
                self.facing[0] = -1
            if pyxel.btn(pyxel.KEY_D):
                self.x, self.y = self.physics.move(self.x, self.y, [1,0])
                self.facing[0] = 1
            if not(pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S)):
                self.facing[1] = 0
            if not(pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D)):
                self.facing[0] = 0

            if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D) and self.physics.momentum<=self.physics.speed:
                self.physics.momentum = self.physics.speed
            else:
                self.physics.momentum /= 2
            
            self.dashFrame += 1

            if pyxel.btnp(pyxel.KEY_SPACE) and self.dashFrame >= self.dashCooldown:
                self.isDashing = True
                self.physics.momentum = self.dashStrength
                self.dashFrame = 0
        else:
            self.x, self.y = self.physics.move(self.x, self.y, self.facing)
            self.dashFrame += 1
            if self.dashFrame == self.dashLength:
                self.isDashing = False
                self.dashFrame = 0
            

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > WIDTH*TILE_SIZE:
            self.x = (WIDTH-1)*TILE_SIZE
        if self.y > HEIGHT*TILE_SIZE:
            self.y = (HEIGHT-1)*TILE_SIZE

class Physics:
    def __init__(self, world):
        self.momentum = 0
        self.speed = 0.4
        self.world = world

    def move(self, x, y, vector):

        tile_x = int(x//TILE_SIZE)
        tile_y = int(y//TILE_SIZE)

        new_x = x + self.momentum*vector[0]
        new_y = y + self.momentum*vector[1]
        
        new_tile_x = tile_x + pyxel.sgn(vector[0])
        new_tile_y = tile_y + pyxel.sgn(vector[1])

        if pyxel.sgn(vector[0]) != 0:
            next_tile_x_1 = self.world.world_map[tile_y][new_tile_x]
            if y != tile_y*TILE_SIZE:
                next_tile_x_2 = self.world.world_map[tile_y+1][new_tile_x]
            else:
                next_tile_x_2 = WorldItem.BACKGROUND
            if (next_tile_x_1 != WorldItem.BLOCK or not collision(new_x, y, new_tile_x*TILE_SIZE, tile_y*TILE_SIZE)) and (next_tile_x_2 != WorldItem.BLOCK or not collision(new_x, y, new_tile_x*TILE_SIZE, (tile_y+1)*TILE_SIZE)):
                x = new_x
            elif (next_tile_x_1 == WorldItem.BLOCK or next_tile_x_2 == WorldItem.BLOCK) and (new_x+TILE_SIZE>(new_tile_x)*TILE_SIZE and (new_tile_x)*TILE_SIZE+TILE_SIZE>new_x):
                if pyxel.sgn(vector[0])==1:
                    x = (new_tile_x-1)*TILE_SIZE
                else:
                    x = (new_tile_x+1)*TILE_SIZE

        tile_x = int(x//TILE_SIZE)

        if pyxel.sgn(vector[1]) != 0:
            next_tile_y_1 = self.world.world_map[new_tile_y][tile_x]
            if x != tile_x*TILE_SIZE:
                next_tile_y_2 = self.world.world_map[new_tile_y][tile_x+1]
            else:
                next_tile_y_2 = WorldItem.BACKGROUND
            if (next_tile_y_1 != WorldItem.BLOCK or not collision(x, new_y, tile_x*TILE_SIZE, new_tile_y*TILE_SIZE)) and (next_tile_y_2 != WorldItem.BLOCK or not collision(x, new_y, (tile_x+1)*TILE_SIZE, new_tile_y*TILE_SIZE)):
                y = new_y
            elif (next_tile_y_1 == WorldItem.BLOCK or next_tile_y_2 == WorldItem.BLOCK) and (new_y+TILE_SIZE>(new_tile_y)*TILE_SIZE and (new_tile_y)*TILE_SIZE+TILE_SIZE>new_y):
                if pyxel.sgn(vector[1])==1:
                    y = (new_tile_y-1)*TILE_SIZE
                else:
                    y = (new_tile_y+1)*TILE_SIZE

        return x,y
    
def collision(x1,y1,x2,y2):
        return x1+TILE_SIZE>x2 and x2+TILE_SIZE>x1 and y1+TILE_SIZE>y2 and y2+TILE_SIZE>y1    

    
class Camera:
    def __init__(self, player):
        self.x = 0
        self.y = 0
        self.max_x = WIDTH*TILE_SIZE-CAMERA_WIDTH
        self.max_y = HEIGHT*TILE_SIZE-CAMERA_HEIGHT
        self.player = player
        self.LENIENCE_x = 4*TILE_SIZE
        self.LENIENCE_y = 4*TILE_SIZE

    def update(self):

        self.playerDistanceFromCenter_x = self.player.x - (self.x + CAMERA_WIDTH/2)
        self.playerDistanceFromCenter_y = self.player.y - (self.y + CAMERA_WIDTH/2)

        if self.playerDistanceFromCenter_x > self.LENIENCE_x:
            self.x += self.playerDistanceFromCenter_x - self.LENIENCE_x
        elif self.playerDistanceFromCenter_x < -self.LENIENCE_x:
            self.x += self.playerDistanceFromCenter_x + self.LENIENCE_x
        if self.playerDistanceFromCenter_y > self.LENIENCE_y:
            self.y += self.playerDistanceFromCenter_y - self.LENIENCE_y
        elif self.playerDistanceFromCenter_y < -self.LENIENCE_y:
            self.y += self.playerDistanceFromCenter_y + self.LENIENCE_y

        if self.x > self.max_x:
            self.x = self.max_x
        if self.x < 0:
            self.x = 0
        if self.y > self.max_y:
            self.y = self.max_y
        if self.y < 0:
            self.y = 0
        
        pyxel.camera(self.x, self.y)


App()
