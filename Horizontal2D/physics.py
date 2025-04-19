from world import*

 

class Physics:

    def __init__(self, world):
        self.world = world
        self.jumpStrength = 1
        self.GRAVITY_ACCELERATION = 10
        self.GRAVITY_SCALE = 0.01
        self.TERMINAL_VELOCITY = 15
        self.vertical_momentum = 0
        self.velocity = [1,0]
        self.frame = 0



    def move_horizontal(self, x, y, direction):
        tile_x = int(x//TILE_SIZE)
        tile_y = int(y//TILE_SIZE)
        new_tile_x = tile_x+direction
        new_x = x + self.velocity[0]*direction

        if new_x+TILE_SIZE >= WIDTH*TILE_SIZE:
            return (WIDTH-1)*TILE_SIZE
        if new_x < 0:
            return 0
        
        next_tile_1 = self.world.world_map[tile_y][new_tile_x]
        next_tile_2 = self.world.world_map[tile_y+1][new_tile_x]
        if (next_tile_1 != WorldItem.BLOCK or not collision(new_x, y, new_tile_x*TILE_SIZE, tile_y*TILE_SIZE)) and (next_tile_2 != WorldItem.BLOCK or not collision(new_x, y, new_tile_x*TILE_SIZE, (tile_y+1)*TILE_SIZE)):
            return new_x
        if (next_tile_1 == WorldItem.BLOCK or next_tile_2 == WorldItem.BLOCK) and (collision(new_x, y, new_tile_x*TILE_SIZE, tile_y*TILE_SIZE) or collision(new_x, y, new_tile_x*TILE_SIZE, (tile_y+1)*TILE_SIZE)):
            return tile_x*TILE_SIZE
        return x

    def isGrounded(self, x, y):
        tile_x = int(x//TILE_SIZE)
        tile_y = int(y//TILE_SIZE)
        tile_y_under = tile_y+1
        tile_under1 = self.world.world_map[tile_y_under][tile_x]
        if tile_x != WIDTH-1:
            tile_under2 = self.world.world_map[tile_y_under][tile_x+1]
        if (y+TILE_SIZE>=tile_y_under*TILE_SIZE and y+TILE_SIZE<(tile_y_under+1)*TILE_SIZE) and (tile_under1 == WorldItem.BLOCK or tile_under2 == WorldItem.BLOCK) and not (tile_under1 == WorldItem.BACKGROUND and x+TILE_SIZE==(tile_x+1)*TILE_SIZE):
            self.velocity[1] = 0
            return (True, (y//TILE_SIZE)*TILE_SIZE)
        else:
            return (False, "N/A")
        
    def applyGravity(self):
        self.velocity[1] += self.GRAVITY_ACCELERATION*self.GRAVITY_SCALE
        if self.velocity[1] > self.TERMINAL_VELOCITY:
            self.velocity[1] = self.TERMINAL_VELOCITY
    
    def jump(self):
        self.velocity[1] -= self.jumpStrength

    def move_vertical(self, x, y):
        if self.velocity[1]>=0:
            direction = 1
        else:
            direction = -1

        new_y = y+self.velocity[1]

        if new_y+TILE_SIZE >= HEIGHT*TILE_SIZE:
            return (HEIGHT-1)*TILE_SIZE
        if new_y < 0:
            return 0

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