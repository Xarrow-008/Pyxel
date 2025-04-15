import pyxel
from world import WorldItem, TILE_SIZE, sprites_collide

class Objects:

    OBJECTS_LIST = WorldItem.OBJECTS_LIST

    def __init__(self):
        self.LAMP = {"x":10 * TILE_SIZE,"y":10 * TILE_SIZE,"hit":False,"broken":False,"moment":0}