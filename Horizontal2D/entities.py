import pyxel
from world import TILE_SIZE, SPRITEBANK
from physics import*

class EntityHandler :
    def __init__(self):
        self.loadedEntities = []

class EntityTemplate:
    BALL_YELLOW = {"image" : [0,6*TILE_SIZE], "width" : TILE_SIZE, "height" : TILE_SIZE, "gravity":True, "tangible":False}
    BALL_RED = {"image" : [0,7*TILE_SIZE], "width" : TILE_SIZE, "height" : TILE_SIZE, "gravity":True, "tangible":True}

class Entity:
    def __init__(self, x, y, entity, entityHandler, world):
        self.x = x
        self.y = y
        self.image = entity["image"]
        self.width = entity["width"]
        self.height = entity["height"]
        self.gravity = entity["gravity"]
        self.tangible = entity["tangible"]
        entityHandler.loadedEntities.append(self)

        self.world = world
        self.physics = Physics(self.world, entityHandler)

    def update(self):
        if self.gravity == True:
            if not self.physics.isGrounded(self.x, self.y, self)[0]:
                self.physics.applyGravity()
            else:
                self.y = self.physics.isGrounded(self.x, self.y, self)[1]

        self.y = self.physics.move_vertical(self.x, self.y)

    def draw(self):
        pyxel.blt(self.x,
                  self.y,
                  SPRITEBANK,
                  self.image[0],
                  self.image[1],
                  self.width,
                  self.height,
                  colkey = 11)
        


