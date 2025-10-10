import os,random,pyxel
from copy import deepcopy as copy



class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(100,100,fps=50)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[2] = 5373971
        
        self.map = [[0 for x in range(10)] for y in range(10)]
        for y in range(6):
            self.map[y][5] = 7

        self.wall_maker = WallMaker(self.map)
        self.entity = Path(self.map)

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.wall_maker.update()
        if self.wall_maker.change:
            self.entity.__init__(self.map)
            self.wall_maker.change = False
        else:
            self.entity.update()
    
    def draw(self):
        pyxel.cls(0)
        self.wall_maker.draw()
        self.entity.draw()
        

class WallMaker:
    def __init__(self,map):
        self.change = True
        self.map = map
    def update(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x//10
            y = pyxel.mouse_y//10
            self.map[y][x] = 7

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
        self.targetx = 8
        self.targety = 0
        self.found = False

        self.border = [(self.x,self.y)]
        self.new_border = []
        self.checked = []
        self.path_origin = copy(self.map)
        self.path_at = (self.targetx,self.targety)
        self.path = [copy(self.path_at)]
        self.finished = False

        self.lines = []
        self.line_length = 1
        self.line_direction = 0
        self.color = False



    def update(self):
        cross = [(0,-1),(0,1),(-1,0),(1,0)]
        if pyxel.frame_count % 2 == 0:
            cross.reverse()
        if (self.targetx,self.targety) not in self.checked:
            for pos in self.border:
                for addon in cross:
                    new_pos = (pos[0]+addon[0],pos[1]+addon[1])
                    if new_pos not in self.checked:
                        if is_inside_map(new_pos, self.map):
                            if self.map[new_pos[1]][new_pos[0]] == 0:
                                if new_pos not in self.new_border:
                                    self.new_border.append(new_pos)
                                    if self.map[new_pos[1]][new_pos[0]] == 0:
                                        self.path_origin[new_pos[1]][new_pos[0]] = pos
                self.checked.append(pos)
            print(self.border)
            self.border = copy(self.new_border)
            self.new_border = []

        elif not self.found:
            self.path_at = copy(self.path_origin[self.path_at[1]][self.path_at[0]])
            self.path.append(copy(self.path_at))
            if self.path_at == (self.x,self.y):
                self.found = True
                
            
                
    def draw(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                color = self.map[y][x]
                pyxel.rect(x*10,y*10,10,10,color)

        for pos in self.checked:
            pyxel.rect(pos[0]*10,pos[1]*10,10,10,6)

        
        if (self.targetx,self.targety) in self.checked:
            for pos in self.path:
                pyxel.rect(pos[0]*10,pos[1]*10,10,10,1)

        if self.finished:
            pyxel.rect(self.targetx*10,self.targety*10,10,10,11)
        else:
            pyxel.rect(self.targetx*10,self.targety*10,10,10,9)


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





App()