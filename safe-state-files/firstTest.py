import os # BEFORE ASYNC TESTS

import pyxel
from player import Player, sprites_dont_collide
from world import World, WorldItem, world_item_draw, TILE_SIZE

class App:
    facing = 0
    def __init__(self):
        os.system("cls")
        pyxel.init(128,128,title="Hello World")
        pyxel.load("mygame.pyxres")

        self.world = World(pyxel.tilemap(0))

        self.player = Player(self.world)

        pyxel.run(self.update, self.draw) #ok mb ca carry tout banger ca prend que update et draw
    
    def update(self):
        left = (-1,0)
        right = (1,0)
        up = (0,-1)
        down = (0,1)
        if pyxel.btn(pyxel.KEY_Q) and self.player.x > 0:
            self.player.move_left()
            self.facing = 1
        if pyxel.btn(pyxel.KEY_D) and self.player.x + TILE_SIZE < TILE_SIZE*World.WIDTH:
            self.player.move_right()
            self.facing = 0
        if pyxel.btn(pyxel.KEY_Z) and self.player.y > 0:
            self.player.move_up()
            self.facing = 2
        if pyxel.btn(pyxel.KEY_S) and self.player.y + TILE_SIZE < TILE_SIZE*World.HEIGHT:
            self.player.move_down()
            self.facing = 3

        
        if pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_D):
            self.facing = 4
        if pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_Q):
            self.facing = 5
        if pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_D):
            self.facing = 6
        if pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_Q):
            self.facing = 7
        
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
    
    def draw(self):
        pyxel.cls(0)

        AIR_LIST = [] #--ATTENTION-- On ne voit pas la différence entre blocs air et non air que jai mis dans l'editeur
        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                world_item = self.world.world_map[y][x]
                if world_item[1] >= 4 and world_item != (1,5): #Si c'est un bloc transparent
                    AIR_LIST.append([x,y,world_item]) #Mettre dans la list qui se dessine apres le joueur(par dessus)
                else:
                    world_item_draw(pyxel, x, y, world_item) #Sinon dessiner car derriere joueur
        
        pyxel.blt(  #dessiner joueur
            self.player.x,
            self.player.y,
            self.player.IMG,
            self.player.PLAYER_DIRECTIONS[self.facing][0] * TILE_SIZE,
            self.player.PLAYER_DIRECTIONS[self.facing][1] * TILE_SIZE,
            self.player.WIDTH,
            self.player.HEIGHT,
        )
        for i in AIR_LIST: #liste de blocs au dessus du joueur
            world_item_draw(pyxel, i[0], i[1], i[2])

App()