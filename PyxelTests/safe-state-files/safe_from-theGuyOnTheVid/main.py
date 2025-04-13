import os #

import pyxel
from player import Player, sprites_dont_collide
from world import World, WorldItem, world_item_draw, TILE_SIZE

class App:
    def __init__(self):
        os.system("cls")
        pyxel.init(128,128,title="Hello World")
        pyxel.load("mygame.pyxres")

        self.world = World(pyxel.tilemap(0))

        self.player = Player(self.world)

        pyxel.run(self.update, self.draw)
    
    def update(self):
        left = (-1,0)
        right = (1,0)
        up = (0,-1)
        down = (0,1)
        if pyxel.btn(pyxel.KEY_Q):
            self.player.move_left()
        if pyxel.btn(pyxel.KEY_D):
            self.player.move_right()
        if pyxel.btn(pyxel.KEY_Z):
            self.player.move_up()
        if pyxel.btn(pyxel.KEY_S):
            self.player.move_down()
        
        if pyxel.btn(pyxel.KEY_E):
            self.player.speed_up()
        if pyxel.btn(pyxel.KEY_A):
            self.player.speed_down()

        
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
    
    def draw(self):
        pyxel.cls(0)

        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                world_item = self.world.world_map[y][x]
                world_item_draw(pyxel, x, y, world_item)
        
        pyxel.blt(
            self.player.x,
            self.player.y,
            self.player.IMG,
            WorldItem.PLAYER[0] * TILE_SIZE,
            WorldItem.PLAYER[1] * TILE_SIZE,
            self.player.WIDTH,
            self.player.HEIGHT,
        )

App()