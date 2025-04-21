from random import *

SIZE = 16

HEIGHT = 16  # *16
WIDTH = 16

class WorldItems:

    GRASS = [(0,0),(0,1)]
    WALL = [(0,1)]
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

        for y in range(HEIGHT):
            self.grid_list.append([])
            for x in range(WIDTH):
                block_placed = False
                for block_list in WorldItems.BLOCKS:
                    if self.tilemap.pget(x*2,y*2) in block_list:
                        self.grid_list[y].append(randint(0,len(block_list)-1))
                        block_placed = True

                if self.tilemap.pget(x*2,y*2) in WorldItems.PLAYER:
                    self.player_init_pos_x = x * SIZE
                    self.player_init_pos_y = y * SIZE
                    self.grid_list[y].append(WorldItems.GRASS[0])
                    block_placed = True
                
                if not block_placed:
                    self.grid_list[y].append(WorldItems.GRASS[randint(0,len(WorldItems.GRASS)-1)])

def world_item_draw(pyxel, x, y, current_block):
            pyxel.blt(
                x * SIZE,
                y * SIZE,
                World.world_type,
                current_block[0],
                current_block[1],
                SIZE,
                SIZE
            )