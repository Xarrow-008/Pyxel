import pyxel, math, random, os

TILE_SIZE = 8

WIDTH = 64
HEIGHT = 64

CAM_W = 12*8
CAM_H = 12*8

class App:
    def __init__(self):
        pyxel.init(CAM_W,CAM_H,title='Hauted Shooter',fps=120)
        pyxel.load('../training.pyxres')


        pyxel.run(self.update,self.draw)
    def update(self):
        pass
    def draw(self):
        pyxel.bltm(0,0,0,0,0,WIDTH*TILE_SIZE,HEIGHT*TILE_SIZE)

class World:
    def __init__(self):
        pass

class Camera:
    def __init__(self,player):
        pass

App()