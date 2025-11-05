import toml, pyperclip, pathlib
from pynput.keyboard import Key, Listener
from utility import *


"""
def draw_palette(x, y, col):
    rgb = pyxel.colors[col]
    hex = f"#{rgb:06X}"
    dec = f"{rgb >> 16},{(rgb >> 8) & 0xFF},{rgb & 0xFF}"

    pyxel.rect(x, y, 13, 13, col)
    pyxel.text(x + 16, y + 1, hex, 7)
    pyxel.text(x + 16, y + 8, dec, 7)
    pyxel.text(x + 5 - (col // 10) * 2, y + 4, f"{col}", 7 if col < 6 else 0)

    if col == 0:
        pyxel.rectb(x, y, 13, 13, 13)


pyxel.init(255, 81, title="Pyxel Color Palette")
pyxel.cls(0)
old_colors = pyxel.colors.to_list()
pyxel.colors.from_list([0x111111, 0x222222, 0x333333])
pyxel.colors[15] = 0x112233

for i in range(16):
    draw_palette(2 + (i % 4) * 64, 4 + (i // 4) * 20, i)

pyxel.show()
"""
os.system('cls')
canvas = [['.' for x in range(20)] for y in range(20)]

digits = [0,1,2,3,4,5,6,7,8,9]
"""
def draw_line(x0,y0,x1,y1):
    positions = []
    cos = x1 - x0
    sin = y1 - y0
    step_ref = max(abs(cos),abs(sin))
    if step_ref != 0:
        stepX = cos / step_ref #diviser toute la longueur par step pour creer chaque marche de l'escalier
        stepY = sin / step_ref #l'autre cote de l'escalier
        for i in range(step_ref+1): #+1 car on met un carre a 0 et a la fin
            positions.append(   (round(x0 + i * stepX), #i fois le nombre de marche auquel on se trouve
                                round(y0 + i * stepY))
                            )
    return positions


class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(width=128,height=128,fps=120)

        self.tab = []
        self.number = 0
        self.index = 0
        self.coming_back = False
        self.last_lclick = False
        self.lclick = False

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)
    
    def update(self):

        self.last_lclick = self.lclick
        self.lclick = False

        for i in range(10):
            if pyxel.btnp(getattr(pyxel,'KEY_'+str(i))):
                self.number = i
                self.lclick = True
        
        if self.last_lclick and not self.lclick:
            if self.coming_back:
                for i in range(self.index):
                    self.tab.pop(0)
                self.index = 0
            self.tab.insert(0,self.number)
            self.coming_back = False
        
        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_Z):
            if self.index < len(self.tab)-1:
                self.index += 1
                self.coming_back = True
                self.number = self.tab[self.index]

        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_Y):
            if self.index > 0:
                self.index += -1
                self.number = self.tab[self.index]
                self.coming_back = True

        if pyxel.btnp(pyxel.KEY_A):
            print(self.tab, self.index, self.number, self.coming_back)

        #                                                  //\\CAN ERASE CODE - NO PROBLEM//\\
    def draw(self):
        pyxel.cls(0)
        pyxel.text(10,10,str(self.tab),7)
        pyxel.text(14+12*self.index,13,'_',11)
        pyxel.text(18,20,str(self.number),3)

App()
"""

def string_to_list(string):
    final = []
    for i in range(len(string)-1):
        char = string[i]
        if char != ' ' and char != ',' and char != '[' and char != ']':
            if int(char) in digits:
                final.append(int(char))
    return final

def str_to_int(string):
    number = 0
    in_number = False
    for char in string:
        if int(char) in digits:
            if not in_number:
                in_number = True
                number = int(char)
            else:
                number *= 10
                number += int(char)
        elif in_number:
            return number
    return number

def rect_in_list(x, y, w, h): 
    all_pos = []
    for in_y in range(h):
        for in_x in range(w):
            all_pos.append((x+in_x,y+in_y))
    return all_pos

def on_press(key):
    print('{0} pressed'.format(key))
    if key == Key.f7:
        draw.App()

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

"""
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
"""

class Actions:
    def __init__(self, map, entities, player, owner):
        self.map = map
        self.entities = entities
        self.player = player
        self.owner = owner
        self.currentActionPriority = 0
        self.collision_happened = False

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

    def init_walk(self, priority, maxSpeed, speedChangeRate, knockbackCoef): #Gets the parameters of the "walk" action
        self.walkPriority = priority
        self.maxSpeed = maxSpeed
        self.speedChangeRate = speedChangeRate
        self.knockbackCoef = knockbackCoef

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
            self.currentActionPriority = 0
            self.isDashing = False
            self.dashFrame = 0
            self.owner.momentum = [pyxel.sgn(self.dashVector[0])*self.dashSpeed, pyxel.sgn(self.dashVector[1])*self.dashSpeed]
            self.dashVector = [0,0]

        self.dashFrame += 1

    def heal(self, value, target):
        target.health += value
        if target.health > target.maxHealth:
            target.health = target.maxHealth

    def hurt(self, value, vector, knockback_coef, target, shot):
        if hasattr(target.actions, "isHitStun"):
            if not target.actions.isHitStun or target.hitBy == shot:
                target.health -= value
                target.actions.isHitStun = True
                target.actions.hitStunFrame = 0
                target.actions.frozen = target.actions.hitFreezeFrame
                target.hitBy = shot
                if hasattr(target.actions, "maxSpeed"):
                    knockback_value = len(str(value))*knockback_coef*target.actions.knockbackCoef
                    target.momentum[0] += vector[0]*knockback_value
                    target.momentum[1] += vector[1]*knockback_value
        else:
            target.health -= value
            if hasattr(target.actions, "maxSpeed"):
                knockback_value = len(str(value))*knockback_coef*target.actions.knockbackCoef
                target.momentum[0] += vector[0]*knockback_value
                target.momentum[1] += vector[1]*knockback_value

    def init_death(self, spawn_item):
        self.deathItemSpawn = spawn_item

        self.dead = False

    def add_death_list(self, list):
        self.deathList = list

    def death(self):
        if self.dead == False:
            self.deathList.remove(self.owner)
            self.dead = True

    def init_ranged_attack(self, priority):
        self.rangedAttackPriority = priority
        self.rangedAttackFrame = 0
        self.shotsFired = 0

    def ranged_attack(self, weapon, x, y, team):
        if self.rangedAttackPriority >= self.currentActionPriority and self.rangedAttackFrame >= weapon["cooldown"] and weapon["mag_ammo"]:

            self.currentActionPriority = self.rangedAttackPriority

            self.rangedAttackFrame = 0
            weapon["mag_ammo"] -= 1
            self.shotsFired += 1

            for i in range(weapon["bullet_count"]):
                horizontal = x - (self.owner.x + self.owner.width/2)
                vertical = y - (self.owner.y + self.owner.height/2)
                norm = math.sqrt(horizontal**2 + vertical**2)

                if norm != 0:
                    cos = horizontal/norm
                    sin = vertical/norm
                    angle = math.acos(cos) * pyxel.sgn(sin)
                    lowest_angle = angle - weapon["spread"]*(math.pi/180)
                    highest_angle = angle + weapon["spread"]*(math.pi/180)
                    angle = random.uniform(lowest_angle, highest_angle)
                    cos = math.cos(angle)
                    sin = math.sin(angle)
                else:
                    cos = 0
                    sin = 0
                Projectile(weapon, self.owner.x, self.owner.y, [cos,sin], self.map, self.entities, self.player, team, self.shotsFired)

    def reload_weapon(self, weapon):
        if self.rangedAttackFrame >= weapon["reload"] and weapon["reserve_ammo"]>0 and weapon["mag_ammo"]==0:
            if weapon["reserve_ammo"]>=weapon["max_ammo"]:
                weapon["mag_ammo"] = weapon["max_ammo"]
                weapon["reserve_ammo"] -= weapon["max_ammo"]
            else:
                weapon["mag_ammo"] = weapon["reserve_ammo"]
                weapon["reserve_ammo"] = 0

    def init_collision(self, wall, enemy, player):
        self.wallCollision = wall
        self.enemyCollision = enemy
        self.playerCollision = player

    def collision(self):

        if self.wallCollision[3] != -1:
            if self.collision_happened:
                if self.wallCollision[0] == 0:
                    self.death()

        if self.enemyCollision[3] != -1:
            for entity in self.entities:
                if type(entity) == Enemy and collision(self.owner.x, self.owner.y, entity.x, entity.y, [self.owner.width, self.owner.height], [entity.width, entity.height]):
                    if (hasattr(entity.actions, "isHitStun") and not entity.actions.isHitStun) or not hasattr(entity.actions, "isHitStun"):
                        self.hurt(self.enemyCollision[0], self.enemyCollision[1], self.enemyCollision[2], entity, self.owner.shot)
                        if self.enemyCollision[3] == 0:
                            self.death()
                        else:
                            self.enemyCollision[3] -= 1

        if self.playerCollision[3] != -1 :          
            if collision(self.owner.x, self.owner.y, self.player.x, self.player.y, [self.owner.width, self.owner.height], [self.player.width, self.player.height]):
                if not player.actions.isHitStun:
                    self.hurt(self.playerCollision[0], self.playerCollision[1], self.playerCollision[2], self.player, self.owner.shot)
                    if self.playerCollision[3] == 0:
                        self.death()
                    else :
                        self.playerCollision[3] -= 1

    def init_hitstun(self, duration, freeze_frame):
        self.hitStunDuration = duration
        self.hitFreezeFrame = freeze_frame
        self.frozen = 0

        self.isHitStun = False
        self.hitStunFrame = 0
        self.hitBy = 0

    def hitstun(self):
        if self.hitStunFrame >= self.hitStunDuration and self.isHitStun:
            self.isHitStun = False
        else:
            self.hitStunFrame += 1

def empty_save_anim():
    dic = {'animations':[{'width':16,'height':16,'frames':[]}]}
    file = open('draw/save_anim.toml','w')
    toml.dump(dic,file)
    file.close()

def copy_press(txt):
    pyperclip.copy(txt)

canvas = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 2, 2, 2, 2, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 2, 2, 2, 2, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def get_canvas(string):
    liste = []
    i = 1
    index = -1
    while i != len(string):
        #print(string[i], i, end=' | ')
        if string[i] == '[':
            liste.append([])
            index += 1
        if string[i].isdigit():
            liste[index].append(int(string[i]))
            
        i += 1
    return liste

#print(get_canvas('[[0,0],[0,1,2,3,2][0,9,8]]')[1])

def get_divider(file):
    divider = 0
    for i in range(len(file)):
        if file[i] == '/' or file[i] == "\\":
            divider = i+1
    return divider

pather = 'not_a_scrap_v2'

folder = pathlib.Path(pather)
for item in folder.iterdir():
    print(item.parts[-1])

def is_in_folder(dir,name):
    folder = pathlib.Path(dir)
    for item in folder.iterdir():
        if item.parts[-1] == name:
            return True
    return False

print(is_in_folder(pather,'main.py'))
        
print(random.randint(0,1))