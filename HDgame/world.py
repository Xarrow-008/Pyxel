from random import *

T_SIZE = 16
IMG_SIZE = 8
RATIO = T_SIZE/IMG_SIZE

HEIGHT = 16  # *16
WIDTH = 16

class WorldItems:

    GRASS = [(0,0),(1,0)]
    WALL = [(0,1),(1,1)]
    PLAYER = [(0,2)]
    BLOCKS = [WALL,GRASS]
    BLOCKS_BG = [GRASS]


class World:

    world_type = 0

    def __init__(self,tilemap):

        self.tilemap = tilemap
        self.player_init_pos_x = 0
        self.player_init_pos_y = 0
        self.grid_list = []

        for y in range(HEIGHT+1):
            self.grid_list.append([])
            for x in range(WIDTH+1):
                block_placed = False
                tm_block = self.tilemap.pget(x*2,y*2)
                tm_block = (tm_block[0]//2,tm_block[1]//2)
                for block in WorldItems.BLOCKS:
                    if tm_block in block:
                        self.grid_list[y].append(choice(block))
                        block_placed = True

                if tm_block in WorldItems.PLAYER:
                    self.player_init_pos_x = x * T_SIZE
                    self.player_init_pos_y = y * T_SIZE
                    self.grid_list[y].append(choice(WorldItems.GRASS))
                    block_placed = True
                
                if not block_placed:
                    self.grid_list[y].append(choice(WorldItems.GRASS))

def world_item_draw(pyxel, x, y, current_block):
            pyxel.blt(
                x * T_SIZE,
                y * T_SIZE,
                World.world_type,
                current_block[0] * T_SIZE,
                current_block[1] * T_SIZE,
                T_SIZE,
                T_SIZE
            )