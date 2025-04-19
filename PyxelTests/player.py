import os
import pyxel
from world import *
    

LEFT = (-1,0)
RIGHT = (1,0)
UP = (0,-1)
DOWN = (0,1)

class Player:
    IMG = 0
    WIDTH = 8
    HEIGHT = 8
    DX = 1

    def __init__(self, world):
        self.x = world.player_grid_x * TILE_SIZE
        self.y = world.player_grid_y * TILE_SIZE
        self.SPEED = self.DX
        self.world = world

    def update(self,facing):
        self.facing = facing
        self.tile_y = int(self.y/TILE_SIZE)
        self.tile_x = int(self.x/TILE_SIZE)
        if pyxel.btn(pyxel.KEY_Q) and self.x > 0:
            self.move(LEFT)
            self.facing[0] = 1
        if pyxel.btn(pyxel.KEY_D) and self.x + TILE_SIZE < TILE_SIZE * World.WIDTH:
            self.move(RIGHT)
            self.facing[0] = 0
        if pyxel.btn(pyxel.KEY_Z) and self.y > 0:
            self.move(UP)
            self.facing[0] = 2
        if pyxel.btn(pyxel.KEY_S) and self.y + TILE_SIZE < TILE_SIZE * World.WIDTH:
            self.move(DOWN)
            self.facing[0] = 3
            
        if pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_D):
            self.facing[0] = 4
        if pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_Q):
            self.facing[0] = 5
        if pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_D):
            self.facing[0] = 6
        if pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_Q):
            self.facing[0] = 7


    def move(self, direction):
        new_x = self.x + self.SPEED * direction[0]
        new_y = self.y + self.SPEED * direction[1]
        
        new_tile_x = self.tile_x + direction[0]
        new_tile_y = self.tile_y + direction[1]

        next_tile_1 = self.world.world_map[new_tile_y][new_tile_x]
        next_tile_2 = self.world.world_map[new_tile_y+abs(direction[0])][new_tile_x+abs(direction[1])]

        if (next_tile_1[1] >= 6 or not sprites_collide(new_x, new_y, new_tile_x*TILE_SIZE, new_tile_y*TILE_SIZE)) and (next_tile_2[1] >= 6 or not sprites_collide(new_x, new_y, (new_tile_x+abs(direction[1]))*TILE_SIZE, (new_tile_y+abs(direction[0]))*TILE_SIZE)):
            self.x = new_x
            self.y = new_y

    def camera_movement(self,cameraPos, margin):
        #print(self.x,self.y)
        #print(cameraPos[1],CAMERA_HEIGHT,World.HEIGHT,cameraPos[1] + CAMERA_HEIGHT < World.HEIGHT)
        if self.x + TILE_SIZE >= cameraPos[0] + CAMERA_WIDTH * (1-margin) and cameraPos[0] + CAMERA_WIDTH < World.WIDTH * TILE_SIZE:
            cameraPos[0] = self.x + TILE_SIZE - CAMERA_WIDTH * (1-margin)
        
        if self.x <= cameraPos[0] + CAMERA_WIDTH * margin and cameraPos[0] > 0:
            cameraPos[0] = self.x - CAMERA_WIDTH * margin
        
        if self.y + TILE_SIZE >= cameraPos[1] + CAMERA_HEIGHT * (1-margin) and cameraPos[1] + CAMERA_HEIGHT < World.HEIGHT * TILE_SIZE:
            cameraPos[1] = self.y + TILE_SIZE - CAMERA_HEIGHT * (1-margin)
        
        if self.y <= cameraPos[1] + CAMERA_HEIGHT * margin and cameraPos[1] > 0:
            cameraPos[1] = self.y - CAMERA_HEIGHT * margin

        cameraPos[0],cameraPos[1] = round(cameraPos[0]), round(cameraPos[1])

    def reset_camera(self,margin):
        camera(self.x-margin,self.y-margin)
    
    '''
    def speed_up(self,amount=0.1,limit_up=3): #ca a juste amene des bugs smeh jmen fous tfacon
        if self.speed <= limit_up:
            self.speed += amount
        if self.speed > limit_up:
            self.speed = limit_up
        print(self.speed)
    
    def speed_down(self,amount=0.1,limit_down=0.6):
        if self.speed >= limit_down:
            self.speed -= amount
        if self.speed < limit_down:
            self.speed = limit_down
        print(self.speed)
    '''

        

