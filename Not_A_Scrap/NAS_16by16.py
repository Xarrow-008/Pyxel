import pyxel,os,math,random
from copy import deepcopy as copy

KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}

WIDTH = 32
HEIGHT = 32
WID = 256
HEI = 256

TILE_SIZE = 16

class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(WID,HEI,fps=120)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[2] = 5373971
        
        self.world = World()
        self.player = Player(self.world.map)
        self.animation = Animation()
        self.showing = 'screen'
        self.keyboard = 'zqsd'
        self.entities = [Path(self.world.map)]

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):

        for entity in self.entities:
            entity.update()

        self.player.update()
            
    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                block = self.world.map[y][x]
                draw_block(x*TILE_SIZE,y*TILE_SIZE,0,block)
        
        for entity in self.entities:
            entity.draw()
        
        self.player.draw()        



class Player: #Everything relating to the player and its control
    def __init__(self, map):
        self.keyboard = 'zqsd'
        self.x = 10
        self.y = 10

        self.health = 40
        self.maxHealth = 80

        self.actions = Actions(map, self)
        self.actions.init_walk(priority=0)
        self.actions.init_dash(priority=0, cooldown=40, speed=1.5, duration=20)

        self.momentum = [0,0]
        self.speed_change_rate = 20 #The higher this is, the more "slippery" the character is
        self.max_speed = 0.5
        
        self.image = (6,3)
        self.facing = [1,0]
        self.last_facing = [1,0]
        #We should probably make it so that "facing" and "direction" work the same way (because facing doesn't have diagonals)
        self.direction = [1,0]
        self.last_direction = [1,0]

        self.walking = False
        self.step = False
        self.second_step = False
        self.step_frame = 0

    def update(self):
        self.movement()

        if self.direction == [0,0]:
            self.direction = copy(self.last_direction)
        self.last_direction = copy(self.direction)
        self.dash()

        self.image_gestion()

        self.last_facing = copy(self.facing)

        if pyxel.btnp(pyxel.KEY_O):
            self.actions.heal(5,self)
        if pyxel.btnp(pyxel.KEY_P):
            self.actions.hurt(5,[-0.5,-0.5],1,self)
        

    def draw(self):
        step_y = self.y
        second_step_y = self.y
        if self.step:
            step_y += -1
        if self.second_step:
            second_step_y += -1


        show(self.x, second_step_y,  (self.image[0] + self.facing[0], self.image[1] + self.facing[1] - 2))
        show(self.x, step_y, (self.image[0] + self.facing[0], self.image[1] + self.facing[1]))
        show(self.x, second_step_y, (self.image[0] + self.facing[0], self.image[1] + self.facing[1] + 2))

        #Health bar
        pyxel.rect(x=1,y=1,w=42,h=10,col=0)

        health_bar_size = int(40*(self.health/self.maxHealth))

        pyxel.rect(x=2,y=2,w=health_bar_size,h=8,col=8)
        sized_text(x=12, y=3, s=str(self.health)+"/"+str(self.maxHealth),col=7,size=7)


    def movement(self):
        #If the player is trying to move, and they're not at max speed, we increase their speed  (and change direction)
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())):
            if self.momentum[1] > -self.max_speed:
                self.momentum[1] -= self.max_speed/self.speed_change_rate
            self.direction[1] = -1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())):
            if self.momentum[0] > -self.max_speed:
                self.momentum[0] -= self.max_speed/self.speed_change_rate
            self.direction[0] = -1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper())):
            if self.momentum[1] < self.max_speed:
                self.momentum[1] += self.max_speed/self.speed_change_rate
            self.direction[1] = 1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())):
            if self.momentum[0] < self.max_speed:
                self.momentum[0] += self.max_speed/self.speed_change_rate
            self.direction[0] = 1
        
        #If the player isn't moving in a specific direction, we lower their speed in that direction progressively
        if not(pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())) or pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper()))):
            self.momentum[1] -= self.momentum[1]/self.speed_change_rate
            self.direction[1] = 0

        if not(pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())) or pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper()))):
            self.momentum[0] -= self.momentum[0]/self.speed_change_rate
            self.direction[0] = 0
        
        #If the player is almost immobile in a specific direction, we snap their speed to 0
        if abs(self.momentum[0]) <= 0.01:
            self.momentum[0] = 0
        if abs(self.momentum[1]) <= 0.01:
            self.momentum[1] = 0

        #If the player is almost at max speed in a specific direction, we snap their speed to max speed
        if self.max_speed-abs(self.momentum[0]) <= 0.01:
            self.momentum[0] = self.max_speed*pyxel.sgn(self.momentum[0])
        if self.max_speed-abs(self.momentum[1]) <= 0.01:
            self.momentum[1] = self.max_speed*pyxel.sgn(self.momentum[1])

        #If the player is over max speed, we decrease their speed progressively
        if abs(self.momentum[0]) > self.max_speed:
            self.momentum[0] -= self.momentum[0]/self.speed_change_rate
        if abs(self.momentum[1]) > self.max_speed:
            self.momentum[1] -= self.momentum[1]/self.speed_change_rate 

        self.actions.walk(self.momentum)
    
    def dash(self):
        if self.actions.isDashing:
            self.actions.dash()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.actions.start_dash(self.direction)
        self.actions.dashFrame += 1
            


    def image_gestion(self):
        self.walking = False
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())):
            self.facing = [0,1]
            self.walking = True
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())):
            self.facing = [0,0]
            self.walking = True
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper())):
            self.facing = [1,1]
            self.walking = True
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())):
            self.facing = [1,0]
            self.walking = True
        
        if self.walking:
            if on_tick(120):
                self.step = not self.step
                self.step_frame = 0

        if self.second_step != self.step:
            self.step_frame += 1
            if self.step_frame >= 40:
                self.second_step = self.step
                self.step_frame = 0



   
class Actions:
    def __init__(self, map, owner):
        self.map = map
        self.owner = owner
        self.currentActionPriority = 0

    def move(self, vector): #We give a movement vector and get the new coordinates of the entity. Used for all kind of movement
        X = int(self.owner.x//TILE_SIZE)
        Y = int(self.owner.y//TILE_SIZE)

        #We handle horizontal and vertical movement separatly to make problem solving easier

        #Calculate the new position
        new_x = self.owner.x + vector[0]
        new_X = X+pyxel.sgn(vector[0])

        if new_x*pyxel.sgn(vector[0]) > new_X*TILE_SIZE*pyxel.sgn(vector[0]): #If its going faster than 1T/f, reduce its speed to exactly 1T/f
            new_x = new_X*TILE_SIZE

        if vector[0]!=0:
            next_X_1 = self.map[Y][new_X]
            if self.owner.y != Y*TILE_SIZE:
                next_X_2 = self.map[Y+1][new_X]
            else:
                next_X_2 = Blocks.GROUND
            #If there's enough space for the entity to move, it moves unimpeded
            if (next_X_1 not in Blocks.WALLS or not collision(new_x, self.owner.y, new_X*TILE_SIZE, Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])) and (next_X_2 not in Blocks.WALLS or not Blocks(new_x, self.owner.y, new_X*TILE_SIZE, (Y+1)*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])):
                self.owner.x = new_x
            #Else If the movement puts the entity in the wall, we snap it back to the border to prevent clipping.
            elif (next_X_1 in Blocks.WALLS or next_X_2 in Blocks.WALLS) and new_x+self.owner.width>X*TILE_SIZE and (X+1)*TILE_SIZE>new_x:
                self.collision_happened = True
                self.owner.x = (new_X-pyxel.sgn(vector[0]))*TILE_SIZE
        
        X = int(self.owner.x//TILE_SIZE)

        #We calculate vertical movement in the same way we do horizontal movement

        new_y = self.owner.y + vector[1]
        new_Y = Y+pyxel.sgn(vector[1])
        
        if new_y*pyxel.sgn(vector[1]) > new_Y*TILE_SIZE*pyxel.sgn(vector[1]):
            new_y = new_Y*TILE_SIZE

        
        if vector[1]!=0:
            next_Y_1 = self.map[new_Y][X]
            if self.owner.x != X*TILE_SIZE:
                next_Y_2 = self.map[new_Y][X+1]
            else:
                next_Y_2 = Blocks.GROUND
            
            if (next_Y_1 not in Blocks.WALLS or not collision(self.owner.x, new_y, X*TILE_SIZE, new_Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])) and (next_Y_2 not in Blocks.WALLS or not Blocks(self.owner.x, new_y, (X+1)*TILE_SIZE, new_Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])):
                self.owner.y = new_y
            elif (next_Y_1 in Blocks.WALLS or next_Y_2 in Blocks.WALLS) and new_y+self.owner.height>Y*TILE_SIZE and (Y+1)*TILE_SIZE>new_y:
                self.collision_happened = True
                self.owner.y = (new_Y-pyxel.sgn(vector[1]))*TILE_SIZE

    def init_walk(self, priority): #Gets the parameters of the "walk" action
        self.walkPriority = priority

    def walk(self, vector): #Used for regular walking.
        if self.currentActionPriority <= self.walkPriority:
            self.currentActionPriority = self.walkPriority

            self.move(vector)

    def init_dash(self, priority, cooldown, speed, duration): #Gets the parameters of the "dash" action, and initialises the related variables
        self.dashPriority = priority
        self.dashCooldown = cooldown
        self.dashSpeed = speed
        self.dashDuration = duration

        self.isDashing = False
        self.dashFrame = 0
        self.dashVector = [0,0]

    def start_dash(self, vector): #Used for dashing/lunging
        if self.dashFrame >= self.dashCooldown and self.currentActionPriority <= self.dashPriority:
            self.currentActionPriority = self.dashPriority

            self.dashFrame = 0
            self.isDashing = True
            self.dashVector = copy(vector)
    
    def dash(self):
        if self.dashFrame < self.dashDuration:
            self.move([self.dashVector[0]*self.dashSpeed, self.dashVector[1]*self.dashSpeed])

        else :
            self.currentActionPriority -= 1
            self.isDashing = False
            self.dashFrame = 0
            self.owner.momentum = [pyxel.sgn(self.dashVector[0])*self.dashSpeed, pyxel.sgn(self.dashVector[1])*self.dashSpeed]
            self.dashVector = [0,0]

        self.dashFrame += 1

    def heal(self, value, target):
        target.health += value

    def hurt(self, value, vector, knockback_coef, target):
        target.health -= value
        knockback_value = len(str(value))*10*knockback_coef
        target.momentum[0] += vector[0]*knockback_value
        target.momentum[1] += vector[1]*knockback_value

class Path:
    def __init__(self,map):
        self.x = 128
        self.y = 128
        self.map = free_space(copy(map))


        self.image = (0,3)
    
    def update(self):
        x, y = 0,0
        if pyxel.btnp(pyxel.KEY_E):
            self.find_new_path(x,y)

    def draw(self):
        show(self.x,self.y,self.image)

    def find_new_path(self,targetx,targety):
        checked = []
        path_checked = []
        border = [(self.x//16,self.y//16)]
        new_border = []
        cross = [(0,-1),(0,1),(-1,0),(1,0)]
        while len(border) > 0 and not (targetx,targety) in checked:
            for pos in border:
                for addon in cross:
                    new_pos = (pos[0]+addon[0],pos[1]+addon[1])
                    if new_pos not in checked:
                        if is_inside_map(new_pos,self.map):
                            if self.map[new_pos[1]][new_pos[0]] in Blocks.GROUND:
                                if new_pos not in new_border:
                                    new_border.append(new_pos)
                checked.append(pos)
            border = copy(new_border)
            new_border = []

class Animation:
    def __init__(self):
        self.image1 = (0,0)
        self.slide_pos = 0
    def loop(self,length,duration,u,v,direction):
        if on_tick(duration):
            for i in range(length):
                if pyxel.frame_count % (length*duration) == i*duration:
                    self.image1 = (u+direction[0]*i*8,v+direction[1]*i*8)
    def slide_anim(self,length,duration,blocks_list):
        if on_tick(duration):
            self.slide_pos += -1
            if self.slide_pos <= -8:
                self.slide.pop(0)
                self.slide.append(random.choice(blocks_list))
                self.slide_pos = 0

class Blocks:
    WALLS = [(0,0),(1,0),(2,0),(3,0)]
    WALLS_DOWN = [(0,0),(1,0)]
    WALLS_UP = [(2,0),(3,0)]

    GROUND = [(0,1)]

class World:
    def __init__(self):
        self.map = [[random.choice(Blocks.GROUND) for x in range(WIDTH)] for y in range(HEIGHT)]

def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def draw(x, y, img, u, v, w, h, colkey=None, rotate=None, scale=1):
    pyxel.blt(x+w//2*(scale-1), y+h//2*(scale-1), img, u, v, w, h, colkey=colkey, rotate=rotate, scale=scale)

def draw_block(x,y,img,block):
    draw(x,y,img,block[0]*TILE_SIZE,block[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE)

def draw_screen(u, v,camx,camy):
    for y in range(7):
        for x in range(128//8):
            pyxel.blt(
                camx+x*16,
                camy+y*16,
                0,
                u,
                v,
                16,
                16
            )

def collision(x1, y1, x2, y2, size1, size2): #Checks if object1 and object2 are colliding with each other
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1

def show(x,y,img,colkey=11,save=0):
    pyxel.blt(x,y,save,img[0]*16,img[1]*16,16,16,colkey=11)

def free_space(map):
    new_map = map
    for y in range(len(map)):
        for x in range(len(map[y])):
            block = map[y][x]
            if block in Blocks.GROUND:
                new_map[y][x] = 0
            else:
                new_map[y][x] = 1
    return new_map
   
def is_inside_map(pos,map):
    if pos[0] >= len(map[0]) or pos[1] >= len(map):
        return False
    if pos[0] < 0 or pos[1] < 0:
        return False
    return True

def remove_doubles(list):
    new_list = []
    for element in list:
        if not element in new_list:
            new_list.append(element)
    return new_list

def sized_text(x,y,s,col,size=6): #Like pyxel.text, but you can modify the size of the text
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    other_characters = ["0","1","2","3","4","5","6","7","8","9",",","?",";",".",":","/","!","'","(",")","[","]","{","}"]

    current_x = x
    scale = size/6

    for chr in s:
        if chr in other_characters:
            u = 4*other_characters.index(chr)
            v = 238
        elif chr in alphabet:
            u = 4*alphabet.index(chr)
            v = 244
        elif chr.lower() in alphabet:
            u = 4*alphabet.index(chr.lower())
            v = 250
        
        w = 3
        h = 6

        pyxel.pal(0,col)
        draw(current_x, y, 0, u, v, w, h, scale=scale, colkey=11)
        pyxel.pal()

        current_x += int(4*scale)
    
App()
