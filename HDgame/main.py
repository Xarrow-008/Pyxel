import pyxel
import os
from world import *
from camera import *
from player import *

class Game:

    def __init__(self):

        os.system('cls')
        pyxel.init(CAM_W,CAM_H,title='HDgame')
        pyxel.load('../HDgame.pyxres')

        self.world = World(pyxel.tilemaps[0])

        self.player = Player(self.world)

        self.camera = Camera(self.player)

        pyxel.run(self.update,self.draw)
    
    def update(self):

        self.player.update()
        self.camera.update(1/8)

    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                current_block = self.world.grid_list[y][x]
                world_item_draw(pyxel, x, y, current_block)
        
        pyxel.blt(
            self.player.x,
            self.player.y,
            self.world.world_type,
            0 * T_SIZE,
            2 * T_SIZE,
            T_SIZE,
            T_SIZE,
            colkey= 2
        )
Game()