import pyxel, os, random

TILE_SIZE = 8
WID = 32
HEI = 32
UP,DOWN,LEFT,RIGHT = [0,-1], [0,1], [-1,0], [1,0]
DIRECTIONS = (UP,DOWN,LEFT,RIGHT)

class Snake:
    def __init__(self):
        pyxel.init(WID*TILE_SIZE,HEI*TILE_SIZE,title='snake',fps=120)
        pyxel.load('../snake.pyxres')

        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world)
        self.apple = Apple()

        pyxel.run(self.update,self.draw)
    def update(self):
        if not self.player.dead:
            self.player.update()
        self.apple.update(self.player,self.world.world_map)
    def draw(self):
        for y in range(HEI):
            for x in range(WID):
                world_item_draw(pyxel,x,y,self.world.world_map[y][x])
        world_item_draw(
            pyxel,
            self.apple.x,
            self.apple.y,
            self.apple.image
        )
        for i in range(len(self.player.pos)):
            world_item_draw(
                pyxel,
                self.player.pos[i][0],
                self.player.pos[i][1],
                self.player.image
            )

class WorldItem:
    WALL = (1,1)
    GROUND1 = (0,0)
    GROUND2 = (0,1)
    PLAYER = (0,2)
    APPLE = (1,0)

class World:
    def __init__(self,tilemap):
        self.world_map = [[(0) for j in range(WID)] for i in range(HEI)]
        self.tilemap = tilemap
        self.player_init_posX = 2
        self.player_init_posY = 2
        self.border_place()
        for y in range(HEI):
            for x in range(WID):
                if self.world_map[y][x] != WorldItem.WALL:
                    if (x+y) % 2 == 0:
                        self.world_map[y][x] = WorldItem.GROUND1
                    else:
                        self.world_map[y][x] = WorldItem.GROUND2
                if self.world_map[y][x] == WorldItem.PLAYER:
                    self.player_init_posX = x
                    self.player_init_posY = y
    def border_place(self):
        for x in range(WID):
            self.world_map[0][x] = WorldItem.WALL
            self.world_map[HEI-1][x] = WorldItem.WALL
        for y in range(HEI):
            self.world_map[y][0] = WorldItem.WALL
            self.world_map[y][WID-1] = WorldItem.WALL

def world_item_draw(pyxel,x,y,block):
    pyxel.blt(
        x*TILE_SIZE,
        y*TILE_SIZE,
        0,
        block[0]*TILE_SIZE,
        block[1]*TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE
        )

class Player:
    def __init__(self,world):
        self.x = world.player_init_posX
        self.y = world.player_init_posY
        self.pos = [(self.x,self.y)]
        self.image = [0,2]
        self.map = world.world_map
        self.length = 1
        self.moved = False
        self.added_length = False
        self.dead = False
        self.facing = (1,0)
    def update(self):
        self.moved = False
        if (pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP)) and self.facing != DOWN:
            self.facing = UP
        if (pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN)) and self.facing != UP:
            self.facing = DOWN
        if (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT)) and self.facing != RIGHT:
            self.facing = LEFT
        if (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT)) and self.facing != LEFT:
            self.facing = RIGHT
        self.move(self.facing)
        if self.moved:
            self.tail_move()
            for i in range(1,len(self.pos)):
                if (self.x,self.y) == self.pos[i]:
                    self.dead = True
                    print('you died')

    def tail_move(self):
        if self.length == len(self.pos):
            if self.length > 1:
                for i in range(self.length-1):
                    self.pos[-i-1] = self.pos[-i-2]
            self.pos[0] = (self.x,self.y)
        else:
            self.pos.insert(0,(self.x,self.y))
    
    def move(self,direction):
        new_X = self.x + direction[0]
        new_Y = self.y + direction[1]
        
        

        if on_tick(10):
            if self.map[new_Y][new_X] == WorldItem.WALL:
                self.dead = True
                print('you died')
            else:
                self.x, self.y = new_X, new_Y
                self.moved = True

class Apple:
    def __init__(self):
        self.x = WID//2
        self.y = HEI//2
        self.image = (1,0)
    def update(self,player,map):
        if player.x == self.x and player.y == self.y:
            self.eaten(player,map)
        else:
            player.added_length = False
    def eaten(self,player,map):
        free_space = []
        for y in range(HEI):
            for x in range(WID):
                if map[y][x] != WorldItem.WALL and x != player.x and y != player.y:
                    free_space.append((x,y))
        self.x, self.y = free_space[random.randint(0,len(free_space)-1)]
        player.length+=1
        

def on_tick(tickframe=60):
    return pyxel.frame_count % tickframe == 0



Snake()