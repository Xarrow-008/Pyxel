import pyxel, math, random, os

TILE_SIZE = 8

WIDTH = 64
HEIGHT = 64

CAM_W = 12*8
CAM_H = 12*8

UP,DOWN,LEFT,RIGHT = [0,-1], [0,1], [-1,0], [1,0]

class App:
    def __init__(self):
        pyxel.init(CAM_W,CAM_H,title='Hauted Shooter',fps=120)
        pyxel.load('../training.pyxres')

        self.world = World(pyxel.tilemaps[0])
        self.player = Player()
        self.camera = Camera(self.player)

        pyxel.run(self.update,self.draw)
    def update(self):
        pass
    def draw(self):
        pyxel.bltm(0,0,0,0,0,WIDTH*TILE_SIZE,HEIGHT*TILE_SIZE)

        pyxel.blt(
            self.player.x,
            self.player.y,
            0,
            self.player.image[0],
            self.player.image[1],
            TILE_SIZE,
            TILE_SIZE,
            colkey=11
            )

class World:
    def __init__(self,tilemap):
        self.tilemap = tilemap

class Player:
    def __init__(self):
        self.x = 2*TILE_SIZE
        self.y = 2*TILE_SIZE
        self.image = [0,2]
    
    def update(self):
        if presses('z'):
            self.move(UP)

    def presses(button):
        presses = []
        if pyxel.btn(pyxel.KEY_Z):
            presses.append('z')
        if pyxel.btn(pyxel.KEY_S):
            presses.append('s')
        if pyxel.btn(pyxel.KEY_Q):
            presses.append('q')
        if pyxel.btn(pyxel.KEY_D):
            presses.append('d')


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
        elif self.x > WIDTH*TILE_SIZE - CAM_W:
            self.x > WIDTH*TILE_SIZE - CAM_W
        
        if self.y<0:
            self.y = 0
        elif self.y > HEIGHT*TILE_SIZE - CAM_H:
            self.y = HEIGHT*TILE_SIZE - CAM_H

       



class Player:
    def __init__(self):
        self.x = 2

App()