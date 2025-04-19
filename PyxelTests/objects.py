import pyxel
from world import WorldItem, World, TILE_SIZE, sprites_collide

class Objects:

    OBJs = WorldItem.OBJECTS_PRESENT

    def __init__(self):
        self.LAMP = {'x':10 * TILE_SIZE,'y':10 * TILE_SIZE,'name':'lamp','hit':0,'hitAnim':False,'hp':3,'dead':False,'deathAnim':False,'u':0,'v':WorldItem.LAMP[1],'moment':0,'frameHit':-60}
        self.OBJs.insert(0,self.LAMP)

        self.GHOST = {'x':8 * TILE_SIZE,'y':10 * TILE_SIZE,'name':'ghost','hit':0,'hitAnim':False,'hp':2,'dead':False,'deathAnim':False,'u':0,'v':WorldItem.GHOST[1],'moment':0,'frameHit':-60}
        self.OBJs.append(self.GHOST)
