import pyxel
from physics import*
from world import*
from animation import*
from entities import*
from camera import*

class Player:
    def __init__(self, world, entityHandler):
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.world = world
        self.physics = Physics(self.world, entityHandler)
        self.animation = Animation()
        self.x = self.world.player_init_pos_x*TILE_SIZE
        self.y = self.world.player_init_pos_y*TILE_SIZE
        self.physics.velocity[0] = 1
        self.physics.jumpStrength = 2
        self.image = [0,1*TILE_SIZE]

        self.animation.saveAnimation(3,8,1,"idle")
        self.animation.saveAnimation(3,8,2,"left")
        self.animation.saveAnimation(3,8,3,"right")
        self.animation.saveAnimation(3,8,4,"up")
        self.animation.saveAnimation(3,8,5,"down")

        self.animation.createAnimationGroup(["idle", "left", "right", "up", "down"])

        self.camera = Camera(self)
        self.entityHandler = entityHandler
        

    def update(self):
        self.x = int(self.x)
        self.y = int(self.y)
        self.mousePositionInWorld_x = self.camera.x + pyxel.mouse_x
        self.mousePositionInWorld_y = self.camera.y + pyxel.mouse_y

        if pyxel.btn(pyxel.KEY_Q):
            self.x = self.physics.move_horizontal(self.x, self.y, -1)
            self.image = self.animation.loadAnimation("left")

        if pyxel.btn(pyxel.KEY_D):
            self.x = self.physics.move_horizontal(self.x, self.y, 1)
            self.image = self.animation.loadAnimation("right")

        if not self.physics.isGrounded(self.x, self.y)[0]:
            self.physics.applyGravity()
            if not pyxel.btn(pyxel.KEY_SPACE) and self.physics.velocity[1]<0:
                self.physics.velocity[1] /= 2
        else:
            self.y = self.physics.isGrounded(self.x, self.y)[1]
            if not(pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D)):
                self.image = self.animation.loadAnimation("idle")
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.physics.jump()
        self.y = self.physics.move_vertical(self.x, self.y)

        if self.physics.velocity[1] < 0:
            self.image = self.animation.loadAnimation("up")
        if self.physics.velocity[1] > 0:
            self.image = self.animation.loadAnimation("down")

        self.animation.frame += 1

        self.camera.update()

        if pyxel.btnp(pyxel.KEY_E):
            Entity(self.mousePositionInWorld_x, self.mousePositionInWorld_y, EntityTemplate.BALL_YELLOW, self.entityHandler, self.world)
        
        if pyxel.btnp(pyxel.KEY_A):
            Entity(self.mousePositionInWorld_x, self.mousePositionInWorld_y, EntityTemplate.BALL_RED, self.entityHandler, self.world)

    def draw(self):
        pyxel.blt(self.x,
                self.y,
                SPRITEBANK,
                self.image[0],
                self.image[1],
                self.width,
                self.height,
                colkey = 11)
        


        
            