from world import*
from math import*
import pyxel
class Player:

    IMG = 0
    U = 0
    V = 0
    WIDTH = TILE_SIZE
    HEIGTH = TILE_SIZE
    VELOCITY = 1

    def __init__(self, world):
        self.x = world.player_init_pos_x*TILE_SIZE
        self.y = world.player_init_pos_y*TILE_SIZE
        self.world = world
        
    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            self.move([-1,0])
        if pyxel.btn(pyxel.KEY_D):
            self.move([1,0])
        if pyxel.btn(pyxel.KEY_Z):
            self.move([0,-1])
        if pyxel.btn(pyxel.KEY_S):
            self.move([0,1])
        self.tile_y = int(self.y/TILE_SIZE)
        self.tile_x = int(self.x/TILE_SIZE)

    def move(self, direction):
        new_x = self.x + self.VELOCITY*direction[0]
        new_y = self.y + self.VELOCITY*direction[1]
        
        new_tile_x = self.tile_x+direction[0]
        new_tile_y = self.tile_y+direction[1]

        next_tile_1 = self.world.world_map[new_tile_y][new_tile_x]
        next_tile_2 = self.world.world_map[new_tile_y+abs(direction[0])][new_tile_x+abs(direction[1])]

        if (next_tile_1 != WorldItem.WALL or not collision(new_x, new_y, new_tile_x*TILE_SIZE, new_tile_y*TILE_SIZE)) and (next_tile_2 != WorldItem.WALL or not collision(new_x, new_y, (new_tile_x+abs(direction[1]))*TILE_SIZE, (new_tile_y+abs(direction[0]))*TILE_SIZE)):
            self.x = new_x
            self.y = new_y

def collision(x1,y1,x2,y2):
        return x1+TILE_SIZE>x2 and x2+TILE_SIZE>x1 and y1+TILE_SIZE>y2 and y2+TILE_SIZE>y1