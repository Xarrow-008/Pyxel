import pyxel
from world import T_SIZE, IMG_SIZE, RATIO, WorldItems

LEFT = (-1,0)
RIGHT = (1,0)
UP = (0,-1)
DOWN = (0,1)

class Player:

    U = 0
    V = 2
    SPEED = 1

    def __init__(self,world):
        self.x = world.player_init_pos_x
        self.y = world.player_init_pos_y
        self.world = world

    def update(self):

        if pyxel.btn(pyxel.KEY_Q):
            self.pos_to_tile()
            self.move(LEFT)
        if pyxel.btn(pyxel.KEY_D):
            self.pos_to_tile()
            self.move(RIGHT)
        if pyxel.btn(pyxel.KEY_Z):
            self.pos_to_tile()
            self.move(UP)
        if pyxel.btn(pyxel.KEY_S):
            self.pos_to_tile()
            self.move(DOWN)

    def moveF(self,direction):
        self.x = self.x + self.SPEED*direction[0]
        self.y = self.y + self.SPEED*direction[1]


    def move(self, direction):
        new_x = self.x + self.SPEED*direction[0]
        new_y = self.y + self.SPEED*direction[1]
        
        new_tile_x = self.tile_x+direction[0]
        new_tile_y = self.tile_y+direction[1]

        next_tile_1 = self.world.grid_list[new_tile_y][new_tile_x]
        next_tile_2 = self.world.grid_list[new_tile_y+abs(direction[0])][new_tile_x+abs(direction[1])]
        

        if ((next_tile_1 not in WorldItems.WALL or not collision(new_x, new_y, new_tile_x*T_SIZE, new_tile_y*T_SIZE)) 
        and (next_tile_2 not in WorldItems.WALL or not collision(new_x, new_y, (new_tile_x+abs(direction[1]))*T_SIZE, (new_tile_y+abs(direction[0]))*T_SIZE))):
            self.x = new_x
            self.y = new_y

    
    def pos_to_tile(self):
            
            self.tile_y = int(self.y/T_SIZE)
            self.tile_x = int(self.x/T_SIZE)

def collision(x1,y1,x2,y2):
        return x1+T_SIZE>x2 and x2+T_SIZE>x1 and y1+T_SIZE>y2 and y2+T_SIZE>y1

