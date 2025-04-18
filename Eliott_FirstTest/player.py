from world import*
import pyxel
class Player:

    IMG = 0
    U = 0
    V = 0
    WIDTH = TILE_SIZE
    HEIGTH = TILE_SIZE
    VELOCITY = 1

    def __init__(self, world):
        self.x = world.player_init_pos_x*TILE_SIZE
        self.y = world.player_init_pos_y*TILE_SIZE
        self.world = world
        
    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            self.left()
        if pyxel.btn(pyxel.KEY_D):
            self.right()
        if pyxel.btn(pyxel.KEY_Z):
            self.up()
        if pyxel.btn(pyxel.KEY_S):
            self.down()
        self.tile_y = int(self.y/TILE_SIZE)
        self.tile_x = int(self.x/TILE_SIZE)

    def left(self):
        new_x = self.x - self.VELOCITY
        new_tile_x = self.tile_x-1
        next_tile = self.world.world_map[self.tile_y][new_tile_x]
        if next_tile != WorldItem.WALL or not collision(new_x, self.y, new_tile_x*TILE_SIZE, self.tile_y*TILE_SIZE) or new_x>=self.tile_x*TILE_SIZE:
                self.x = new_x

    def right(self):
        new_x = self.x + self.VELOCITY
        new_tile_x = self.tile_x+1
        next_tile = self.world.world_map[self.tile_y][new_tile_x]
        if next_tile != WorldItem.WALL or not collision(new_x, self.y, new_tile_x*TILE_SIZE, self.tile_y*TILE_SIZE):
                self.x = new_x
    
    def up(self):
        new_y = self.y - self.VELOCITY
        new_tile_y = self.tile_y-1
        next_tile = self.world.world_map[new_tile_y][self.tile_x]
        if next_tile != WorldItem.WALL or not collision(self.x, new_y, self.tile_y*TILE_SIZE, new_tile_y*TILE_SIZE):
                self.y = new_y

    def down(self):
        new_y = self.y + self.VELOCITY
        new_tile_y = self.tile_y+1
        next_tile = self.world.world_map[new_tile_y][self.tile_x]
        if next_tile != WorldItem.WALL or not collision(self.x, new_y, self.tile_y*TILE_SIZE, new_tile_y*TILE_SIZE):
                self.y = new_y

def collision(x1,y1,x2,y2):
        return (x1+TILE_SIZE>=x2 and y1+TILE_SIZE>=y2) or (x2+TILE_SIZE>=x1 and y2+TILE_SIZE>=y1)