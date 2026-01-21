from utility import *
from rooms.rooms import *

TILE_SIZE = 16

WID = 256
HEI = 256 

CAM_WIDTH = TILE_SIZE*20
CAM_HEIGHT = TILE_SIZE*20

class App:
    def __init__(self):
        pyxel.init(CAM_WIDTH, CAM_HEIGHT, fps=120)
        pyxel.load('rooms.pyxres')
        pyxel.colors[2] = get_color('740152')
        pyxel.colors[14] = get_color('C97777')
        pyxel.pal(7,10)

        self.show = TestAnim()

        pyxel.mouse(visible=True)

        pyxel.run(self.update,self.draw)

    def update(self):
        self.show.update()

    def draw(self):
        self.show.draw()

class TestAnim:
    def __init__(self):
        self.anim = Animation([0,0],{'u':0,'v':4,'width':5*TILE_SIZE,'height':3*TILE_SIZE}, lifetime='100 cycles')

    def update(self):
        self.anim.update()
    
    def draw(self):
        self.anim.draw(0,0)


def get_color(hex):
    return int(hex, 16)

App()