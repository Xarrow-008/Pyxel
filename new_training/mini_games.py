import pyxel, math, random, os

TILE_SIZE = 8

WIDTH = 64
HEIGHT = 64

CAM_W = 12*8
CAM_H = 12*8

UP,DOWN,LEFT,RIGHT = [0,-1], [0,1], [-1,0], [1,0]

class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(CAM_W,CAM_H,title='Haunted Shooter',fps=120)
        pyxel.load('../training.pyxres')

        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world)
        self.camera = Camera(self.player,1/4)

        pyxel.run(self.update,self.draw)
    def update(self):
        self.player.update()


        self.camera.update()
        pyxel.camera(self.camera.x,self.camera.y)
    def draw(self):
        pyxel.bltm(0,0,0,0,0,WIDTH*TILE_SIZE,HEIGHT*TILE_SIZE)

        pyxel.blt(
            self.player.x,
            self.player.y,
            0,
            self.player.image[0]*TILE_SIZE,
            self.player.image[1]*TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
            colkey=11
            )

class WorldItem:
    WALL = (1,0)
    WOOD_WALL = (0,1)
    FLOOR = (0,0)
    GRASS = (2,0)

    BLOCKS = [WALL, WOOD_WALL, FLOOR, GRASS]

    FLOORS = [FLOOR, GRASS]
    WALLS = [WALL, WOOD_WALL]

class World:
    def __init__(self,tilemap):
        self.tilemap = tilemap
        self.map = [[(2,0) for x in range(WIDTH)] for y in range(HEIGHT)]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                
                for block in WorldItem.BLOCKS:
                    if self.tilemap.pget(x,y) == block:
                        self.map[y][x] = block

class Player:
    def __init__(self,world):
        self.x = 2*TILE_SIZE
        self.y = 2*TILE_SIZE
        self.image = [0,2]
        self.moved = False

        self.map = world.map
        self.physics = Physics(self,self.map)
    
    
    def update(self):
        
        if self.presses('z'):
            self.move(UP)
            self.facing = UP
        if self.presses('s'):
            self.move(DOWN)
            self.facing = DOWN
        if self.presses('q'):
            self.move(LEFT)
            self.facing = LEFT
        if self.presses('d'):
            self.move(RIGHT)
            self.facing = RIGHT

        if self.presses('z') or self.presses('s') or self.presses('q') or self.presses('d'):
            self.moved = True
            if self.facing == UP:
                self.image = (1,2)
            elif self.facing == DOWN:
                self.image = (0,2)
            elif self.facing == LEFT:
                self.image = (1,3)
            elif self.facing == RIGHT:
                self.image = (0,3)
        else:
            self.moved = False

    def move(self,direction):
    
        self.x, self.y = self.x + direction[0], self.y + direction[1]

    def presses(self,button):
        presses = []
        if pyxel.btn(pyxel.KEY_Z):
            presses.append('z')
        if pyxel.btn(pyxel.KEY_S):
            presses.append('s')
        if pyxel.btn(pyxel.KEY_Q):
            presses.append('q')
        if pyxel.btn(pyxel.KEY_D):
            presses.append('d')
        return button in presses

class Physics:
    def __init__(self,entity,map):
        self.map = map
        self.x = entity.x
        self.y = entity.y
        self.momentum = 1



class Camera:
    def __init__(self,player,margin):
        self.x = 0
        self.y = 0
        self.player = player
        self.margin = margin
    
    def update(self):
        if self.player.x < self.x + CAM_W * self.margin:
            self.x = self.player.x - CAM_W * self.margin
        if self.player.x > self.x + CAM_W * (1-self.margin):
            self.x = self.player.x - CAM_W * (1-self.margin)
        
        if self.player.y < self.y + CAM_H * self.margin:
            self.y = self.player.y - CAM_H * self.margin
        if self.player.y > self.y + CAM_H * (1-self.margin):
            self.y = self.player.y - CAM_H * (1-self.margin)

        if self.x<0:
            self.x = 0
        if self.x > WIDTH*TILE_SIZE - CAM_W:
            self.x = WIDTH*TILE_SIZE - CAM_W
        
        if self.y<0:
            self.y = 0
        if self.y > HEIGHT*TILE_SIZE - CAM_H:
            self.y = HEIGHT*TILE_SIZE - CAM_H
        print(self.x, self.y, WIDTH*TILE_SIZE - CAM_W)


def collision(x1, y1, x2, y2, size1, size2):
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1

App()