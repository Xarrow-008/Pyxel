import pyxel
from world import T_SIZE, HEIGHT, WIDTH

CAM_W = 16 * 8
CAM_H = 16 * 8

class Camera:

    def __init__(self,player):
        self.x = 1 * T_SIZE
        self.y = 1 * T_SIZE
        self.player = player

    def update(self, margin):
        
        #print(self.x,self.y)
        #print(self.y,CAM_H,HEIGHT,self.y + CAM_H < HEIGHT)
        if self.player.x + T_SIZE >= self.x + CAM_W * (1-margin) and self.x + CAM_W < WIDTH * T_SIZE:
            self.x = self.player.x + T_SIZE - CAM_W * (1-margin)
        
        if self.player.x <= self.x + CAM_W * margin and self.x > 0:
            self.x = self.player.x - CAM_W * margin
        
        if self.player.y + T_SIZE >= self.y + CAM_H * (1-margin) and self.y + CAM_H < HEIGHT * T_SIZE:
            self.y = self.player.y + T_SIZE - CAM_H * (1-margin)
        
        if self.player.y <= self.y + CAM_H * margin and self.y > 0:
            self.y = self.player.y - CAM_H * margin

        self.x,self.y = round(self.x), round(self.y)

    def reset_camera(self,margin):
        camera(self.player.x-margin,self.player.y-margin)