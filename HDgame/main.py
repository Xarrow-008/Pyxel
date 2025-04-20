import pyxel
import os
from world import *
from camera import *

class Game:

    def __init__(self):

        os.system('cls')
        pyxel.init(CAM_W,CAM_H,title='HDgame')
        pyxel.load('../HDgame.pyxres')

        pyxel.run(self.update,self.draw)
    
    def update(self):
        pass

    def draw(self):
        pyxel.blt(
            0,
            0,
            0,
            0,
            0,
            SIZE,
            SIZE
        )
        pyxel.blt(
            0,
            0,
            0,
            0 * SIZE,
            2 * SIZE,
            SIZE,
            SIZE,
            colkey= 2
        )
Game()