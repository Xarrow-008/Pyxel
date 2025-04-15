import pyxel
from world import WorldItem, TILE_SIZE, sprites_collide

class Objects:

    OBJs = WorldItem.OBJECTS_LIST

    def __init__(self):
        self.LAMP = {'x':10 * TILE_SIZE,'y':10 * TILE_SIZE,'hit':0,'hitAnim':False,'hp':1,'dead':False,'deathAnim':False,'u':0,'v':WorldItem.LAMP[1],'moment':0,'frameHit':-60}
        self.OBJs.append(self.LAMP)