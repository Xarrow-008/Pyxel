import pyxel
from world import WorldItem, TILE_SIZE, sprites_collide

class Objects:

    OBJECTS_LIST = WorldItem.OBJECTS_LIST

    def __init__(self):
        print("init objects")
        self.lamp_x = 10 * TILE_SIZE
        self.lamp_y = 10 * TILE_SIZE
        self.lamp_moment = 0
        self.lamp_hit = False
        self.lamp_broken = False
        