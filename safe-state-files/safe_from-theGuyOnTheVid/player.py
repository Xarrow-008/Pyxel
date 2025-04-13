import os
import pyxel
from world import WorldItem, TILE_SIZE, sprites_dont_collide

class Player:
    IMG = 0
    U = 0
    V = 0
    WIDTH = 8
    HEIGHT = 8
    DX = 1

    def __init__(self, world):
        self.x = world.player_grid_x * TILE_SIZE
        self.y = world.player_grid_y * TILE_SIZE
        self.speed = self.DX
        self.world = world

    def move_left(self): #Ma shala it works

        tile_x = int(self.x / TILE_SIZE)
        tile_y = int(self.y / TILE_SIZE)

        new_x = self.x - self.DX
        new_tile_x = tile_x - 1


        next_tile_up = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]

        print(next_tile_up,next_tile_bottom)
        if not (
        (next_tile_up != WorldItem.GRASS
        and sprites_dont_collide(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
        (next_tile_bottom != WorldItem.GRASS)
        and sprites_dont_collide(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE))):
            self.x = new_x

    def move_right(self):
        self.x += self.speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed
    
    def speed_up(self,amount=0.1,limit_up=3):
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
        

        

