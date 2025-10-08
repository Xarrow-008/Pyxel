import pyxel,os,math,random,copy

KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}

WIDTH = 32
HEIGHT = 32
TILE_SIZE = 16

class App:
    def __init__(self):
        pyxel.init(128,128,fps=120)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[2] = 5373971
        
        self.world = World()
        self.player = Player(self.world.map)
        self.animation = Animation()
        self.showing = 'screen'
        self.keyboard = 'zqsd'

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.player.update()
            
    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                block = self.world.map[y][x]
                draw_block(x*TILE_SIZE,y*TILE_SIZE,0,block)
        self.player.draw()

class Player: #Everything relating to the player and its control
    def __init__(self, map):
        self.keyboard = 'zqsd'
        self.x = 10
        self.y = 10

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
            self.direction = copy.copy(self.last_direction)
        self.last_direction = copy.copy(self.direction)
        self.dash()

        self.image_gestion()

        self.last_facing = copy.copy(self.facing)
        

    def draw(self):
        step_y = self.y
        second_step_y = self.y
        if self.step:
            step_y += -1
        if self.second_step:
            second_step_y += -1


        pyxel.blt(self.x, second_step_y, 0, (self.image[0] + self.facing[0]) * 16, (self.image[1] + self.facing[1] - 2) * 16, 16, 16, 11)
        pyxel.blt(self.x, step_y, 0, (self.image[0] + self.facing[0]) * 16, (self.image[1] + self.facing[1]) * 16, 16, 16, 11)
        pyxel.blt(self.x, second_step_y, 0, (self.image[0] + self.facing[0]) * 16, (self.image[1] + self.facing[1] + 2) * 16, 16, 16, 11)


    def movement(self):
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())):
            if self.momentum[1] > -self.max_speed:
                self.momentum[1] -= self.max_speed/self.speed_change_rate
            else:
                self.momentum[1] = -self.max_speed
            self.direction[1] = -1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())):
            if self.momentum[0] > -self.max_speed:
                self.momentum[0] -= self.max_speed/self.speed_change_rate
            else:
                self.momentum[0] = -self.max_speed
            self.direction[0] = -1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper())):
            if self.momentum[1] < self.max_speed:
                self.momentum[1] += self.max_speed/self.speed_change_rate
            else:
                self.momentum[1] = self.max_speed
            self.direction[1] = 1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())):
            if self.momentum[0] < self.max_speed:
                self.momentum[0] += self.max_speed/self.speed_change_rate
            else:
                self.momentum[0] = self.max_speed
            self.direction[0] = 1
        
        if not(pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())) or pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper()))):
            self.momentum[1] -= self.momentum[1]/self.speed_change_rate
            self.direction[1] = 0

        if not(pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())) or pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper()))):
            self.momentum[0] -= self.momentum[0]/self.speed_change_rate
            self.direction[0] = 0
        
        if abs(self.momentum[0]) <= 0.01:
            self.momentum[0] = 0
        if abs(self.momentum[1]) <= 0.01:
            self.momentum[1] = 0

        self.actions.walk(self.momentum)
    
    def dash(self):
        if self.actions.isDashing:
            self.actions.dash()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.actions.start_dash(self.direction)
            


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
        self.current_action_priority = 0

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
        self.walk_priority = priority

    def walk(self, vector): #Used for regular walking.
    
        if self.current_action_priority <= self.walk_priority:
            self.current_action_priority = self.walk_priority

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
        self.isDashing = True
        self.dashVector = copy.copy(vector)

    def dash(self):
        if self.dashFrame < self.dashDuration:
            self.move([self.dashVector[0]*self.dashSpeed, self.dashVector[1]*self.dashSpeed])

        else :
            self.isDashing = False
            self.dashFrame = 0
            self.owner.momentum = [pyxel.sgn(self.dashVector[0])*self.dashSpeed,pyxel.sgn(self.dashVector[1])*self.dashSpeed]
            self.dashVector = [0,0]

        self.dashFrame += 1
        


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

App()
