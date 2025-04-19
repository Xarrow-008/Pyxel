from world import*

 

class Physics:

    def __init__(self, world):
        self.world = world
        self.speed = 1
        self.jumpStrength = 1
        self.GRAVITY_ACCELERATION = 10
        self.GRAVITY_SCALE = 0.01
        self.TERMINAL_VELOCITY = 15
        self.vertical_momentum = 0
        self.frame = 0



    def move_horizontal(self, x, y, direction):
        tile_x = int(x//TILE_SIZE)
        tile_y = int(y//TILE_SIZE)
        new_tile_x = tile_x+direction
        new_x = x + self.speed*direction
        next_tile_1 = self.world.world_map[tile_y][new_tile_x]
        next_tile_2 = self.world.world_map[tile_y+1][new_tile_x]
        if (next_tile_1 != WorldItem.BLOCK or not collision(new_x, y, new_tile_x*TILE_SIZE, tile_y*TILE_SIZE)) and (next_tile_2 != WorldItem.BLOCK or not collision(new_x, y, new_tile_x*TILE_SIZE, (tile_y+1)*TILE_SIZE)):
            return new_x
        return x

    def isGrounded(self, x, y):
        tile_x = int(x//TILE_SIZE)
        tile_y = int(y//TILE_SIZE)
        tile_y_under = tile_y+1
        tile_under1 = self.world.world_map[tile_y_under][tile_x]
        tile_under2 = self.world.world_map[tile_y_under][tile_x+1]
        if (y+TILE_SIZE>=tile_y_under*TILE_SIZE and y+TILE_SIZE<(tile_y_under+1)*TILE_SIZE) and (tile_under1 == WorldItem.BLOCK or tile_under2 == WorldItem.BLOCK) and not (tile_under1 == WorldItem.BACKGROUND and x+TILE_SIZE==(tile_x+1)*TILE_SIZE):
            self.vertical_momentum = 0
            return True
        else:
            return False
        
    def applyGravity(self):
        self.vertical_momentum += self.GRAVITY_ACCELERATION*self.GRAVITY_SCALE
        if self.vertical_momentum > self.TERMINAL_VELOCITY:
            self.vertical_momentum = self.TERMINAL_VELOCITY
    
    def jump(self):
        self.vertical_momentum -= self.jumpStrength

    def move_vertical(self, x, y):
        if self.vertical_momentum>=0:
            direction = 1
        else:
            direction = -1

        new_y = y+self.vertical_momentum

        if direction == 1:
            return new_y
        
        else:
            tile_x = int(x//TILE_SIZE)
            tile_y = int(y//TILE_SIZE)
            new_tile_y = tile_y-1
            next_tile_1 = self.world.world_map[new_tile_y][tile_x]
            next_tile_2 = self.world.world_map[new_tile_y][tile_x+1]
            if (next_tile_1 != WorldItem.BLOCK or not collision(x, new_y, tile_x*TILE_SIZE, new_tile_y*TILE_SIZE)) and (next_tile_2 != WorldItem.BLOCK or not collision(x, new_y, (tile_x+1)*TILE_SIZE, new_tile_y*TILE_SIZE)):
                return new_y
        return y

def collision(x1,y1,x2,y2):
        return x1+TILE_SIZE>x2 and x2+TILE_SIZE>x1 and y1+TILE_SIZE>y2 and y2+TILE_SIZE>y1