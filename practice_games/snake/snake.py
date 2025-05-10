import pyxel, os, random

TILE_SIZE = 8
WID = 128
HEI = 128
UP,DOWN,LEFT,RIGHT = [0,-1], [0,1], [-1,0], [1,0]
DIRECTIONS = (UP,DOWN,LEFT,RIGHT)
CAM_w = 32
CAM_h= 32

class Snake:
    def __init__(self):
        pyxel.init(CAM_w* TILE_SIZE,CAM_h* TILE_SIZE,title='snake',fps=120)
        pyxel.load('../../snake.pyxres')

        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world)
        self.apple = Apple()
        self.camera = Camera(self.player,1/4)

        pyxel.run(self.update,self.draw)
    def update(self):
        if not self.player.dead:
            self.player.update()
            self.camera.update()
            pyxel.camera(self.camera.x*TILE_SIZE,self.camera.y*TILE_SIZE)
        self.apple.update(self.player,self.world.world_map)
        if on_tick(120):
            print((self.player.x,self.player.y),end='',flush=True)
        if pyxel.btn(pyxel.KEY_R):
            self.player.x,self.player.y = self.apple.pos[0][0], self.apple.pos[0][1]
    def draw(self):
        pyxel.cls(0)
        for y in range(HEI):
            for x in range(WID):
                world_item_draw(pyxel,x,y,self.world.world_map[y][x])
        for i in range(len(self.apple.pos)):
            world_item_draw(
                pyxel,
                self.apple.pos[i][0],
                self.apple.pos[i][1],
                self.apple.image
            )
        player_draw(pyxel,self.player.pos,self.player)

class Blocks:
    WALL = (1,1)
    GROUND1 = (0,0)
    GROUND2 = (0,1)
    PLAYER = (0,2)
    APPLE = (1,0)
    CON = (0,3)

class World:
    def __init__(self,tilemap):
        self.world_map = [[Blocks.WALL for j in range(WID)] for i in range(HEI)]
        self.tilemap = tilemap
        self.player_init_posX = 10
        self.player_init_posY = 10

        self.roomlist = []
        self.nb_rooms = 3

        self.room_size = 20

        rect_place(self.world_map,self.player_init_posX-1,self.player_init_posY-1,20,20,Blocks.GROUND1)
        self.rooms_place(self.player_init_posX-1,self.player_init_posY+19)
        self.tiled_ground()

    def tiled_ground(self):
        for y in range(HEI):
            for x in range(WID):
                if self.world_map[y][x] != Blocks.WALL:
                    if (x+y) % 2 == 0:
                        self.world_map[y][x] = Blocks.GROUND1
                    else:
                        self.world_map[y][x] = Blocks.GROUND2
                if self.world_map[y][x] == Blocks.PLAYER:
                    self.player_init_posX = x
                    self.player_init_posY = y
    
    def rooms_place(self,startX,startY):
        self.x= startX
        self.y= startY+2
        self.con_x= startX + self.room_size//2-1
        self.con_y= startY
        room_pos = 2
        rect_place(self.world_map,self.con_x,self.con_y,2,2,Blocks.CON)
        rect_place(self.world_map,self.x,self.y,self.room_size,self.room_size,Blocks.GROUND1)
        self.roomlist.append(dic_copy({'name':0,'x':self.x,'y':self.y,'con_x':self.con_x,'con_y':self.con_y}))
        for i in range(self.nb_rooms):
            if room_pos == 0:
                room_pos = random.randint(0,1)
            elif room_pos == 2:
                room_pos = random.randint(1,2)
            else:
                room_pos = random.randint(0,2)
            
            if room_pos == 0 and self.x<self.room_size+2+1:
                room_pos = 2
            if room_pos == 2 and self.x>WID-(self.room_size+2+1):
                room_pos = 0
            
            if room_pos == 0:
                self.con_x=self.x-2
                self.con_y=self.y+self.room_size//2-1
                self.x-=2+self.room_size
            elif room_pos == 2:
                self.con_x=self.x+self.room_size
                self.con_y=self.y+self.room_size//2-1
                self.x+=2+self.room_size
            elif room_pos == 1:
                self.con_x=self.x+self.room_size//2-1
                self.con_y=self.y+self.room_size
                self.y+=2+self.room_size
            
            rect_place(self.world_map,self.con_x,self.con_y,2,2,Blocks.CON)
            rect_place(self.world_map,self.x,self.y,self.room_size,self.room_size,Blocks.GROUND1)
            self.roomlist.append(dic_copy({'name':0,'x':self.x,'y':self.y,'con_x':self.con_x,'con_y':self.con_y}))

            
            
            
    
def rect_place(map,x,y,w,h,block):
    for in_x in range(w):
        for in_y in range(h):
            map[in_y + y][in_x + x] = block

def world_item_draw(pyxel,x,y,block,colk=15):
    pyxel.blt(
        x*TILE_SIZE,
        y*TILE_SIZE,
        0,
        block[0]*TILE_SIZE,
        block[1]*TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE,
        colkey=colk
        )
def player_draw(pyxel,pos,player):
    for i in range(len(pos)):
        if i == 0:
            if player.dead:
                world_item_draw(
                    pyxel,
                    pos[0][0],
                    pos[0][1],
                    (0,3)
                )
            else:
                world_item_draw(
                    pyxel,
                    pos[i][0],
                    pos[i][1],
                    (0,2)
                )
        else:
            world_item_draw(
                pyxel,
                pos[i][0],
                pos[i][1],
                (1,2)
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
        self.eat_frame = 0
    def update(self):
        self.moved = False
        if (pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_UP)) and self.facing != DOWN:
            self.facing = UP
        elif (pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN)) and self.facing != UP:
            self.facing = DOWN
        elif (pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_LEFT)) and self.facing != RIGHT:
            self.facing = LEFT
        elif (pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.KEY_RIGHT)) and self.facing != LEFT:
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
            if self.map[new_Y][new_X] == Blocks.WALL:
                self.dead = True
                print('you died')
            else:
                self.x, self.y = new_X, new_Y
                self.moved = True

class Apple:
    def __init__(self):
        self.pos = [[11,11],[11,13]]
        self.image = (1,0)
    def update(self,player,map):
        for i in range(len(self.pos)):
            if [player.x,player.y] == self.pos[i]:
                self.eaten(player,map,i)
            else:
                player.added_length = False
    def eaten(self,player,map,i):
        free_space = []
        for y in range(HEI):
            for x in range(WID):
                if map[y][x] != Blocks.WALL: #and (x,y) not in player.pos and [x,y] not in self.pos:
                    free_space.append((x,y))
        self.pos[i][0], self.pos[i][0] = free_space[random.randint(0,len(free_space)-1)]
        print(self.pos[i][0],self.pos[i][1],map[self.pos[i][0]][self.pos[i][1]])
        player.length+=1
        player.eat_frame = pyxel.frame_count
        

def on_tick(tickframe=60):
    return pyxel.frame_count % tickframe == 0

class Camera:
    def __init__(self,player,margin):
        self.x = 0
        self.y = 0
        self.player = player
        self.margin = margin
    def update(self):
        if self.player.x < self.x + CAM_w * self.margin:
            self.x = self.player.x - CAM_w * self.margin
        if self.player.x + 1 > self.x + CAM_w * (1-self.margin):
            self.x = self.player.x + 1 - CAM_w * (1-self.margin)
        if self.player.y < self.y + CAM_h * self.margin:
            self.y = self.player.y - CAM_h * self.margin
        if self.player.y + 1 > self.y + CAM_h * (1-self.margin):
            self.y = self.player.y + 1 - CAM_h * (1-self.margin)
        
        if self.x<0:
            self.x = 0
        if self.x + CAM_w > WID:
            self.x = WID - CAM_w
        if self.y<0:
            self.y = 0
        if self.y + CAM_h > HEI:
            self.y = HEI - CAM_h

def dic_copy(dico):
    dicoC = {}
    for key in dico.keys():
        dicoC[key]=dico[key]
    return dicoC
def list_copy(tab):
    new_tab = []
    for i in tab:
        new_tab.append(tab[i])
    return new_tab


Snake()