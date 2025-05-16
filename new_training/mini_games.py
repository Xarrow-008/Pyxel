import pyxel, math, random, os

WIDTH = 64
HEIGHT = 64

CAM_W = 8*8
CAM_H = 8*8

class App:
    def __init__(self):
        pyxel.init(CAM_W,CAM_H,title='Hauted Shooter',fps=120)
        pyxel.load('../training.pyxres')
    def update(self):
        pass
    def draw(self):
        pyxel.bltm(0,0,0,)

class World:
    def __init__(self):
        pass

class Camera:
    def __init__(self,player):
        pass

App()