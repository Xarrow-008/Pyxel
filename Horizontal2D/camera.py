import pyxel
from world import*
CAMERA_HEIGHT = 128
CAMERA_WIDTH = 128

class Camera:
    def __init__(self, player):
        self.x = 120*TILE_SIZE
        self.y = 240*TILE_SIZE
        self.max_x = WIDTH*TILE_SIZE-CAMERA_WIDTH
        self.max_y = HEIGHT*TILE_SIZE-CAMERA_HEIGHT
        self.player = player
        self.LENIENCE_x = 2*TILE_SIZE
        self.LENIENCE_y = 4*TILE_SIZE

    def update(self):

        self.playerDistanceFromCenter_x = self.player.x - (self.x + CAMERA_WIDTH/2)
        self.playerDistanceFromCenter_y = self.player.y - (self.y + CAMERA_WIDTH/2)

        if self.playerDistanceFromCenter_x > self.LENIENCE_x:
            self.x += self.playerDistanceFromCenter_x - self.LENIENCE_x
        elif self.playerDistanceFromCenter_x < -self.LENIENCE_x:
            self.x += self.playerDistanceFromCenter_x + self.LENIENCE_x
        if self.playerDistanceFromCenter_y > self.LENIENCE_y:
            self.y += self.playerDistanceFromCenter_y - self.LENIENCE_y
        elif self.playerDistanceFromCenter_y < -self.LENIENCE_y:
            self.y += self.playerDistanceFromCenter_y + self.LENIENCE_y

        if self.x > self.max_x:
            self.x = self.max_x
        if self.x < 0:
            self.x = 0
        if self.y > self.max_y:
            self.y = self.max_y
        if self.y < 0:
            self.y = 0
        
        pyxel.camera(self.x, self.y)
        
