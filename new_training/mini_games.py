import pyxel, os, math, random

WID = 32
HEI = 32

TILE_SIZE = 16

CAM_W = 16*TILE_SIZE
CAM_H = 12*TILE_SIZE

UP, DOWN, LEFT, RIGHT = (0,-1), (0,1), (-1,0), (1,0)

class Game:
    def __init__(self):

        pyxel.init(CAM_W,CAM_H,title='miniGames',fps=120)
        pyxel.load('../minigame.pyxres')

        self.world = World(pyxel.tilemaps[0],0)
        self.entities = []
        self.player = Player(self.world,self.entities,'azerty')
        self.camera = Camera(self.player,1/4)

        pyxel.run(self.update,self.draw)

    def update(self):
        self.player.update()
        for entity in self.entities:
            entity.update()
        
        self.camera.update()
        pyxel.camera(self.camera.x,self.camera.y)


    def draw(self):
        for y in range(HEI):
            for x in range(WID):
                block = self.world.map[y][x]
                block_draw(x*TILE_SIZE,y*TILE_SIZE,block)
        block_draw(self.player.x,self.player.y,[0,2])

def block_draw(x,y,image):
    pyxel.blt(
        x,
        y,
        0,
        image[0]*TILE_SIZE,
        image[1]*TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE,
        colkey=11
        )

def collision(x1,y1,x2,y2,size1,size2):
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1


class World:
    def __init__(self,tilemap,game_state):
        self.tilemap = tilemap
        self.map = [[(0,0) for x in range(WID)] for y in range(HEI)]
        self.p_init_x = WID*TILE_SIZE//2
        self.p_init_y = HEI-1

class Player:
    def __init__(self,world,entities,keyboard):
        self.world = world
        self.entities = entities
        self.x = self.world.p_init_x
        self.y = self.world.p_init_y

        self.alive = True


    def update(self):

        self.tile_X = self.x // TILE_SIZE
        self.tile_Y = self.y // TILE_SIZE

        if self.press('z') and self.y>0:
            self.move(UP)
        if self.press('s') and self.y < HEI*TILE_SIZE-TILE_SIZE:
            self.move(DOWN)
        if self.press('q') and self.x>0:
            self.move(LEFT)
        if self.press('d') and self.x < WID*TILE_SIZE-TILE_SIZE:
            self.move(RIGHT)

        if self.press('space'):
            Bullet(self.x+TILE_SIZE//2,self.y+TILE_SIZE//2,UP,self.entities)

    def move(self,direction):
        self.x += direction[0]
        self.y += direction[1]
    
    def press(self,button):
        presses=[]
        if pyxel.btn(pyxel.KEY_Z):
            presses.append('z')
        if pyxel.btn(pyxel.KEY_S):
            presses.append('s')
        if pyxel.btn(pyxel.KEY_Q):
            presses.append('q')
        if pyxel.btn(pyxel.KEY_D):
            presses.append('d')
        if pyxel.btn(pyxel.KEY_SPACE):
            presses.append('space')
        
        return button in presses
    
class Bullet:
    def __init__(self,x,y,direction,entities):
        self.x = x
        self.y = y
        self.w = abs(direction[0])*TILE_SIZE
        self.h = abs(direction[1])*TILE_SIZE
        self.direction = direction
        self.image = [0,3]
        self.speed = 3
    
    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        for entity in self.entities:
            if collision(self.x,self.y,entity.x,entity.y,(self.w,self.h),(entity.w,entity.h)):
                entity.health -= 1
                entity.hitFrame = pyxel.frame_count
                entity.hit = True

class Camera:
    def __init__(self,player,margin):
        self.player = player
        self.x = 0
        self.y = 0
        self.margin = margin
    def update(self):
        if self.player.x < self.x + CAM_W * self.margin:
            self.x = self.player.x - CAM_W * self.margin
        if self.player.x+TILE_SIZE > self.x + CAM_W * (1-self.margin):
            self.x = self.player.x+TILE_SIZE - CAM_W * (1-self.margin)

        if self.player.y < self.y + CAM_H * self.margin:
            self.y = self.player.y - CAM_H * self.margin
        if self.player.y+TILE_SIZE > self.y + CAM_H * (1-self.margin):
            self.y = self.player.y+TILE_SIZE - CAM_H * (1-self.margin)

        if self.x<0:
            self.x = 0
        if self.x>WID*TILE_SIZE-CAM_W:
            self.x = WID*TILE_SIZE-CAM_W
        
        if self.y<0:
            self.y = 0
        if self.y>HEI*TILE_SIZE-CAM_H:
            self.y = HEI*TILE_SIZE-CAM_H

        self.x, self.y = round(self.x), round(self.y)




Game()