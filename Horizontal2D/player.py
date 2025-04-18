import pyxel
from physics import*
from world import*

class Player:
    def __init__(self, world):
        self.world = world
        self.physics = Physics(self.world)
        self.x = self.world.player_init_pos_x*TILE_SIZE
        self.y = self.world.player_init_pos_y*TILE_SIZE
        self.physics.speed = 1
        self.physics.jumpStrength = 2

    def update(self):
        self.x = int(self.x)
        self.y = int(self.y)
        if pyxel.btn(pyxel.KEY_Q):
            self.x = self.physics.move_horizontal(self.x, self.y, -1)
        if pyxel.btn(pyxel.KEY_D):
            self.x = self.physics.move_horizontal(self.x, self.y, 1)
        if not self.physics.isGrounded(self.x, self.y):
            self.physics.applyGravity()
            if not pyxel.btn(pyxel.KEY_SPACE) and self.physics.vertical_momentum<0:
                self.physics.vertical_momentum /= 2
        else:
            self.y = (self.y//TILE_SIZE)*TILE_SIZE
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.physics.jump()
        self.y = self.physics.move_vertical(self.x, self.y)
        print(self.physics.vertical_momentum)
        
            