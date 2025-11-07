import os,random,pyxel,math
from copy import deepcopy as copy


WID = 250
HEI = 250
FPS = 120

TILE_SIZE = 10

KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}

class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(WID,HEI,fps=FPS)
        pyxel.load('pather.pyxres')
        pyxel.colors[2] = 5373971
        
        self.map = [[random.choice([0,0,0,0,0,0,0,0,0,0]) for x in range(WID//10+1)] for y in range(HEI//10+1)]
        self.empty_space()


        self.wall_maker = WallMaker(self.map)
        self.controller = Controller(self.map)

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.wall_maker.update()
        if self.wall_maker.change:
            self.controller.walls_changed = True
            self.wall_maker.change = False
        self.controller.update()

    
    def draw(self):
        pyxel.cls(0)
        self.walls_draw()
        self.wall_maker.draw()
        self.controller.draw()
    
    def walls_draw(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                color = self.map[y][x]
                pyxel.rect(x*10,y*10,10,10,color)
        
    def empty_space(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 7:
                    if y < 5 and x < 5:
                        self.map[y][x] = 0
                    if y > len(self.map)-5 and x > len(self.map[y]) - 5:
                        self.map[y][x] = 0

        

class Controller:
    def __init__(self,map):
        self.map = map

        self.hider = Hider(self.map)
        self.pather = Pather(self.map)

        self.walls_changed = False
    def update(self):
        if self.walls_changed:
            self.hider.__init__(self.map)
            self.pather.__init__(self.map)
            self.walls_changed = False
        else:
            self.pather.update(self.hider.x,self.hider.y)
            self.check_weapons()
            self.hider.update()


    def draw(self):
        self.pather.draw()
        self.hider.draw()

    def check_weapons(self):
        if self.hider.stun_around:
            self.hider.stun_around = False
            if distance(self.hider.x,self.hider.y,self.pather.x,self.pather.y) < 20:
                self.pather.stun(120)
        

        
class WallMaker:
    def __init__(self,map):
        self.change = True
        self.map = map
    def update(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x//10
            y = pyxel.mouse_y//10
            try:
                self.map[y][x] = 7
            except:
                pass

            self.change = True

        if pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            x = pyxel.mouse_x//10
            y = pyxel.mouse_y//10
            self.map[y][x] = 0

            self.change = True

    def draw(self):
        pass



class Path:
    def __init__(self,map):
        self.x = 1
        self.y = 1
        self.map = map
        self.found = False

        self.border = [(self.x,self.y)]
        self.new_border = []
        self.checked = []
        self.finished = False

        self.color = False



    def update(self):
        cross = [(0,-1),(0,1),(-1,0),(1,0)]
        for pos in self.border:
            for addon in cross:
                new_pos = (pos[0]+addon[0],pos[1]+addon[1])
                if new_pos not in self.checked:
                    if new_pos not in self.new_border:
                        if self.is_visible(new_pos):
                            if self.map[new_pos[1]][new_pos[0]] == 0:
                                self.new_border.append(new_pos)
            self.checked.append(pos)
        self.border = copy(self.new_border)
        self.new_border = []
                  
    def draw(self):

        for pos in self.checked:
            pyxel.rect(pos[0]*10,pos[1]*10,10,10,6)


    def is_visible(self,pos):
        return pos[0] >= 0 and pos[0] < WID//TILE_SIZE and pos[1] >= 0 and pos[1] < HEI//TILE_SIZE

class Actions:
    def __init__(self, map, owner):
        self.map = map
        self.owner = owner
        self.current_action_priority = 0

    def move(self, vector): #We give a movement vector and get the new coordinates of the entity
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
            if (next_X_1 not in Blocks.WALLS or not collision(new_x, self.owner.y, new_X*TILE_SIZE, Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])) and (next_X_2 not in Blocks.WALLS or not collision(new_x, self.owner.y, new_X*TILE_SIZE, (Y+1)*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])):
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
            
            if (next_Y_1 not in Blocks.WALLS or not collision(self.owner.x, new_y, X*TILE_SIZE, new_Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])) and (next_Y_2 not in Blocks.WALLS or not collision(self.owner.x, new_y, (X+1)*TILE_SIZE, new_Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])):
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
        self.dashVector = copy(vector)

    def dash(self):
        if self.dashFrame < self.dashDuration:
            self.move([self.dashVector[0]*self.dashSpeed, self.dashVector[1]*self.dashSpeed])

        else :
            self.isDashing = False
            self.dashFrame = 0
            self.owner.momentum = [pyxel.sgn(self.dashVector[0])*self.dashSpeed,pyxel.sgn(self.dashVector[1])*self.dashSpeed]
            self.dashVector = [0,0]

        self.dashFrame += 1

class Pather:
    def __init__(self,map):
        self.map = map


        self.x = 0
        self.y = 0
        self.width = 10
        self.height = 10
        self.image = (0,2)
        self.keyboard = 'zqsd'
        self.reset_path()
        self.path_img = (0,3)


        self.momentum = [0,0]
        self.speed_change_rate = 10 #The higher this is, the more "slippery" the character is
        self.max_speed = 0.8
        self.move_to = [0,0]
        self.actions = Actions(self.map,self)

        self.freeze_start = 0
        self.freeze_duration = 0

        self.direction = [0,1]

        self.actions.init_walk(priority=1)

        self.anims = []
    
    def update(self,targetx,targety):
        #self.move_keyboard()


        if self.can_move():
            if self.target_has_moved(targetx,targety) and not self.target_is_close(targetx,targety):
                self.find_path(int(targetx//TILE_SIZE),int(targety//TILE_SIZE))

            if not self.target_is_close(targetx,targety):
                self.move_path()
            else:
                self.move_towards_target(targetx,targety)
            self.movement()
        else:
            self.unstuck_path(targetx,targety)
        
        self.preventOOB()
        
        self.update_anims()

    def draw(self):
        for pos in self.path:
            show(pos[0]*TILE_SIZE,pos[1]*TILE_SIZE,self.path_img)
        draw_n(self.x, self.y,0,self.image[0]*TILE_SIZE,self.image[1]*TILE_SIZE,self.width,self.height,colkey=11)
        self.draw_anims()
    
    def draw_anims(self):
        for anim in self.anims:
            anim.draw(self.x,self.y)

    def update_anims(self):
        for anim in self.anims:
            anim.update()
            if anim.is_dead():
                self.anims.remove(anim)

    def movement(self):
        #If the player is trying to move, and they're not at max speed, we increase their speed  (and change direction)
        if self.move_to[1] < 0:
            if self.momentum[1] > -self.max_speed:
                self.momentum[1] -= self.max_speed/self.speed_change_rate
            self.direction[1] = -1

        if self.move_to[0] < 0:
            if self.momentum[0] > -self.max_speed:
                self.momentum[0] -= self.max_speed/self.speed_change_rate
            self.direction[0] = -1

        if self.move_to[1] > 0:
            if self.momentum[1] < self.max_speed:
                self.momentum[1] += self.max_speed/self.speed_change_rate
            self.direction[1] = 1

        if self.move_to[0] > 0:
            if self.momentum[0] < self.max_speed:
                self.momentum[0] += self.max_speed/self.speed_change_rate
            self.direction[0] = 1
        
        #If the player isn't moving in a specific direction, we lower their speed in that direction progressively
        if not (self.move_to[1] < 0 or self.move_to[1] > 0):
            self.momentum[1] -= self.momentum[1]/self.speed_change_rate
            self.direction[1] = 0

        if not(self.move_to[0] < 0 or self.move_to[0] > 0):
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
    
    def move_keyboard(self):
        self.move_to = [0,0]
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())):
            self.move_to[1] = -1
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())):
            self.move_to[0] = -1
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper())):
            self.move_to[1] = 1
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())):
            self.move_to[0] = 1
        
    def move_path(self):
        self.move_to = [0,0]
        if not self.path_index >= len(self.path)-2:
            self.move_to[0] = self.path[self.path_index+1][0]*TILE_SIZE - self.x
            self.move_to[1] = self.path[self.path_index+1][1]*TILE_SIZE - self.y

            distance_current = distance(self.x,self.y,self.path[self.path_index][0]*TILE_SIZE,self.path[self.path_index][1]*TILE_SIZE)
            distance_next = distance(self.x,self.y,self.path[self.path_index+1][0]*TILE_SIZE,self.path[self.path_index+1][1]*TILE_SIZE)
            if distance_next < distance_current:
                self.path_index += 1

    def move_towards_target(self,x,y):
        self.move_to[0] = x - self.x
        self.move_to[1] = y - self.y

    def find_path(self,targetx,targety):
        start = (self.path[self.path_index][0],self.path[self.path_index][1])
        border = [copy(start)]
        new_border = []
        checked = []
        path_origin = copy(self.map)
        self.path_at = (targetx,targety)
        self.path = [copy(self.path_at)]
        cross = [(0,-1),(0,1),(-1,0),(1,0)]
        while len(border) > 0 and (targetx,targety) not in checked:
            cross.reverse()
            for pos in border:
                for addon in cross:
                    new_pos = (pos[0]+addon[0],pos[1]+addon[1])
                    if new_pos not in checked:
                        if is_inside_map(new_pos, self.map):
                            if self.map[new_pos[1]][new_pos[0]] == 0:
                                if new_pos not in new_border:
                                    new_border.append(new_pos)
                                    path_origin[new_pos[1]][new_pos[0]] = pos
                checked.append(pos)
            border = copy(new_border)
            new_border = []
        if (targetx,targety) in checked:
            while self.path_at != start:
                self.path_at = copy(path_origin[self.path_at[1]][self.path_at[0]])
                self.path.insert(0,copy(self.path_at))

        self.path_index = 0
        
    def reset_path(self):
        self.path = [(int(self.x//TILE_SIZE),int(self.y//TILE_SIZE)) for i in range(2)]
        self.path_at = copy(self.path[0])
        self.path_index = 0

    def target_has_moved(self,x,y):
        return distance(x//TILE_SIZE,y//TILE_SIZE,*self.path[-1]) > 1

    def target_is_close(self,x,y):
        return distance(self.x,self.y,x,y) < 2*TILE_SIZE

    def preventOOB(self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        
        if self.x + self.width > WID:
            self.x = WID - self.width
        if self.y + self.height > HEI:
            self.y = HEI - self.height

    def can_move(self):
        return not self.is_stunned()

    def is_stunned(self):
        return self.freeze_start + self.freeze_duration > pyxel.frame_count

    def stun(self,duration):
        self.freeze_start = pyxel.frame_count
        self.freeze_duration = duration
        self.anims.append(Animation((0,-12),{'duration':10},duration))

    def unstuck_path(self,targetx,targety):
        if pyxel.frame_count+2 > self.freeze_start + self.freeze_duration:
            self.reset_path()
            print('new one',flush=True)

class Hider:
    def __init__(self,map):
        self.map = map

        self.x = WID-10
        self.y = HEI-10
        self.width = 10
        self.height = 10
        self.image = (1,2)
        self.keyboard = 'zqsd'


        self.momentum = [0,0]
        self.speed_change_rate = 20 #The higher this is, the more "slippery" the character is
        self.max_speed = 0.8
        self.move_to = [0,0]
        self.actions = Actions(self.map,self)
        
        self.anims = []

        self.stun_around = False

        self.direction = [0,1]

        self.actions.init_walk(priority=1)


    def update(self):
        self.move_keyboard()
        self.movement()
        self.preventOOB()
        self.weapons_use()
        self.update_anims()

    def weapons_use(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.stun_around = True
            #self.anims.append(Animation((-20,-10),0,'10 cycles'))

    def update_anims(self):
        for anim in self.anims:
            anim.update()
            if anim.is_dead():
                self.anims.remove(anim)

    def draw(self):
        show(self.x,self.y,self.image)
        self.draw_anims()

    def draw_anims(self):
        for anim in self.anims:
            anim.draw(self.x,self.y)

    def movement(self):
        #If the player is trying to move, and they're not at max speed, we increase their speed  (and change direction)
        if self.move_to[1] < 0:
            if self.momentum[1] > -self.max_speed:
                self.momentum[1] -= self.max_speed/self.speed_change_rate
            self.direction[1] = -1

        if self.move_to[0] < 0:
            if self.momentum[0] > -self.max_speed:
                self.momentum[0] -= self.max_speed/self.speed_change_rate
            self.direction[0] = -1

        if self.move_to[1] > 0:
            if self.momentum[1] < self.max_speed:
                self.momentum[1] += self.max_speed/self.speed_change_rate
            self.direction[1] = 1

        if self.move_to[0] > 0:
            if self.momentum[0] < self.max_speed:
                self.momentum[0] += self.max_speed/self.speed_change_rate
            self.direction[0] = 1
        
        #If the player isn't moving in a specific direction, we lower their speed in that direction progressively
        if not (self.move_to[1] < 0 or self.move_to[1] > 0):
            self.momentum[1] -= self.momentum[1]/self.speed_change_rate
            self.direction[1] = 0

        if not(self.move_to[0] < 0 or self.move_to[0] > 0):
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
    
    def move_keyboard(self):
        self.move_to = [0,0]
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())):
            self.move_to[1] = -1
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())):
            self.move_to[0] = -1
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper())):
            self.move_to[1] = 1
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())):
            self.move_to[0] = 1
        
    def preventOOB(self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        
        if self.x + self.width > WID:
            self.x = WID - self.width
        if self.y + self.height > HEI:
            self.y = HEI - self.height


class Blocks:
    WALLS = [7]
    GROUND = [0]

class Animation:
    def __init__(self,relative_pos,settings,lifetime):
        self.start = pyxel.frame_count
        self.settings = settings
        self.lifetime = lifetime
        self.relative_pos = relative_pos
        self.default_set = {'u':0,'v':0,'width':TILE_SIZE,'heigth':TILE_SIZE,'vector':(1,0),'length':3,'duration':30}

        self.apply_settings()

        self.frame = 0

        self.img = (0,0)
        self.kill = False
    def update(self):
        self.frame = pyxel.frame_count - self.start
        if not self.is_dead():
            self.get_img()
    def draw(self,x,y):
        show(x + self.relative_pos[0], y + self.relative_pos[1], self.img, colkey=0)
    def get_img(self):
        frame_anim = (self.frame // self.settings['duration']) % self.settings['length']
        x = self.settings['u'] + self.settings['vector'][0]*frame_anim
        y = self.settings['v'] + self.settings['vector'][1]*frame_anim
        self.img = (x,y)
        #print(frame_anim,x,y)

    def apply_settings(self):
        if type(self.settings) is dict:
            for setting in self.default_set.keys():
                if not setting in self.settings:
                    self.settings[setting] = self.default_set[setting]
        else:
            self.settings = self.default_set

        nb = 1
        if type(self.lifetime) is str:
            if 'cycle' in self.lifetime[-6:]:
                for i in range(1,len(self.lifetime)):
                    if self.lifetime[:i].isdigit():
                        nb = int(self.lifetime[:i])

        if not type(self.lifetime) is int:
            self.lifetime = self.settings['duration']*self.settings['length']*nb

    def is_dead(self):
        return pyxel.frame_count > self.start + self.lifetime or self.kill
                


def is_inside_map(pos,map):
    if pos[0] >= len(map[0]) or pos[1] >= len(map):
        return False
    if pos[0] < 0 or pos[1] < 0:
        return False
    return True

def show(x,y,img,colkey=11,save=0):
    pyxel.blt(x,y,save,img[0]*TILE_SIZE,img[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE,colkey=colkey)

def collision(x1, y1, x2, y2, size1, size2): #Checks if object1 and object2 are colliding with each other
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1

def draw_n(x, y, img, u, v, w, h, colkey=None, rotate=None, scale=1):
    pyxel.blt(x+w//2*(scale-1), y+h//2*(scale-1), img, u, v, w, h, colkey=colkey, rotate=rotate, scale=scale)

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def distance(x1,y1,x2,y2): #looks at distance with pythagorean theorem
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


App()