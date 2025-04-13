import os # BEFORE ASYNC TESTS --AFTER-- ASYNC IS SHIT WITH THIS COUNT W 30frames/s

import pyxel
from player import Player, sprites_dont_collide
from world import World, WorldItem, world_item_draw, TILE_SIZE

class App:
    direction = [0,0]
    frame = 0
    timer = 0
    tickrate = 0.1
    walking_switch=False
    walking = False
    slash_frame = -60
    slashing = False
    slash_direction = [1,0]

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
        facing = self.direction

        self.frame+=1

        if self.movement_keys_pressed():
            self.walking = True
            if self.on_tick(self.tickrate):
                self.walking_switch = not self.walking_switch
        else:
            self.walking = False

        if self.walking_switch:
            facing[1] = 3
        else:
            facing[1] = 2
        if not self.walking:
            facing[1] = 4


        if pyxel.btn(pyxel.KEY_Q) and self.player.x > 0:
            self.player.move_left()
            facing[0] = 1
        if pyxel.btn(pyxel.KEY_D) and self.player.x + TILE_SIZE < TILE_SIZE*World.WIDTH:
            self.player.move_right()
            facing[0] = 0
        if pyxel.btn(pyxel.KEY_Z) and self.player.y > 0:
            self.player.move_up()
            facing[0] = 2
        if pyxel.btn(pyxel.KEY_S) and self.player.y + TILE_SIZE < TILE_SIZE*World.HEIGHT:
            self.player.move_down()
            facing[0] = 3

        
        if pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_D):
            facing[0] = 4
        if pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_Q):
            facing[0] = 5
        if pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_D):
            facing[0] = 6
        if pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_Q):
            facing[0] = 7

        
        if pyxel.btn(pyxel.KEY_SPACE) and not self.slashing:
            self.slash_frame = self.frame
            self.slashing = True
            self.slash_direction = self.facing_to_direction(facing)
            self.slash_facing = facing[0]
            self.slash_x = self.player.x + self.slash_direction[0] * TILE_SIZE
            self.slash_y = self.player.y + self.slash_direction[1] * TILE_SIZE


        if self.slash_frame + 10 < self.frame:
            self.slashing = False

        


        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        self.direction = facing

    def draw(self):
        pyxel.cls(0)

        AIR_LIST = [] #--ATTENTION-- On ne voit pas la différence entre blocs air et non air que jai mis dans l'editeur
        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                world_item = self.world.world_map[y][x]
                if world_item[1] >= 6 and world_item != (1,7): #Si c'est un bloc transparent
                    AIR_LIST.append([x,y,world_item]) #Mettre dans la list qui se dessine apres le joueur(par dessus)
                else:
                    world_item_draw(pyxel, x, y, world_item) #Sinon dessiner car derriere joueur
        
        if self.slashing:
            self.draw_transp(  #dessiner slash
                self.slash_x,
                self.slash_y,
                self.player.IMG,
                self.slash_facing * TILE_SIZE,
                8 * TILE_SIZE,
                self.player.WIDTH,
                self.player.HEIGHT,
                11)

        
        self.draw_transp(  #dessiner joueur
            self.player.x,
            self.player.y,
            self.player.IMG,
            self.direction[0] * TILE_SIZE,
            self.direction[1] * TILE_SIZE,
            self.player.WIDTH,
            self.player.HEIGHT,
            0)

        for i in AIR_LIST: #liste de blocs au dessus du joueur
            world_item_draw(pyxel, i[0], i[1], i[2])
    
    def on_tick(self, tickrate = 0.5):
        if self.frame % (30 * tickrate) == 0:
            return True
        return False
    
    def movement_keys_pressed(self):
        if (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D)
            or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S)):
            return True
        else:
            return False
    
    def facing_to_direction(self,facing):
        if facing[0] == 0:
            return [1,0]
        if facing[0] == 1:
            return [-1,0]
        if facing[0] == 2:
            return [0,-1]
        if facing[0] == 3:
            return [0,1]
        if facing[0] == 4:
            return [1,-1]
        if facing[0] == 5:
            return [-1,-1]
        if facing[0] == 6:
            return [1,1]
        if facing[0] == 7:
            return [-1,1]
    
    def draw_transp(self,x, y, img, u, v, w, h,gscreen): #do every pixel if gscreen, replace by bg color
        bg_pixels = []
        for bg_y in range(TILE_SIZE):
            bg_pixels.append([])
            for bg_x in range(TILE_SIZE):
                bg_pixels[bg_y].append(pyxel.pget(x + bg_x, y + bg_y))
        pyxel.blt(
            x,
            y,
            img,
            u,
            v,
            w,
            h,)
        for bg_y in range(TILE_SIZE):
            for bg_x in range(TILE_SIZE):
                if pyxel.pget(x + bg_x, y + bg_y) == gscreen:
                    pyxel.pset(x + bg_x, y + bg_y, bg_pixels[bg_y][bg_x])



App()