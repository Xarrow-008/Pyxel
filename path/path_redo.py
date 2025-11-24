from utility import *

WID = 250
HEI = 250
TILE_SIZE = 10

FPS = 120

map = [[0 for x in range(HEI//TILE_SIZE)] for y in range(WID//TILE_SIZE)]

KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}


class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(WID,HEI,fps=FPS)
        pyxel.load('pather.pyxres')
        pyxel.colors[2] = 5373971
        
        #self.empty_space()

        self.controller = Controller()
        self.mapper = Mapper()

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.updateMap()
        self.updateEntities()

    
    def draw(self):
        pyxel.cls(0)
        self.drawMap()
        self.drawEntities()

    def updateMap(self):
        self.mapper.update()
        if self.mapper.needsReInit:
            self.mapper.needsReInit = False
            self.controller.reinitialize()

    def updateEntities(self):
        if self.mapper.canRun():
            self.controller.update()

    def drawMap(self):
        self.mapper.draw()

    def drawEntities(self):
        self.controller.draw()

        
    


class Mapper:
    def __init__(self):
        global map
        self.needsReInit = False

    def update(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mousePlaceBlock(7)

        if pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            self.mousePlaceBlock(0)

    def mousePlaceBlock(self,block):
        x = pyxel.mouse_x//TILE_SIZE
        y = pyxel.mouse_y//TILE_SIZE
        try:
            map[y][x] = block
        except:
            pass
        self.needsReInit = True

    def draw(self):
        self.drawWalls()

    def drawWalls(self):
        for y in range(len(map)):
            for x in range(len(map[y])):
                color = map[y][x]
                pyxel.rect(x*10,y*10,10,10,color)

    def canRun(self):
        return not (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT))


        
class Controller:
    def __init__(self):
        self.hiderSpawn = [WID-2*TILE_SIZE, HEI-2*TILE_SIZE]
        self.patherSpawn = [TILE_SIZE, TILE_SIZE]

        self.hider = Player(*self.hiderSpawn)
        self.pather = Pather(*self.patherSpawn)

    def update(self):
        self.pather.update((self.hider.x,self.hider.y))
        self.checkInteractions()
        self.hider.update()


    def draw(self):
        self.pather.draw()
        self.hider.draw()

    def checkInteractions(self):
        if self.hider.stunAround:
            self.hider.stunAround = False
            if distance(self.hider.x,self.hider.y,self.pather.x,self.pather.y) < 20:
                self.pather.stun(120)
    
    def reinitialize(self):
        self.pather.__init__(*self.patherSpawn)
        self.hider.__init__(*self.hiderSpawn)
        


class Entity: #General Entity class with all the methods describing what entities can do
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.momentum = [0,0]

        self.collidedWithWall = False

        self.currentActionPriority = 0

    def update(self):

        self.hitstun()

        if  self.canDoActions():

            self.movement()

            self.dash()

            self.collision()

            self.attack()

        self.preventOOB()

        self.death()

        self.imageGestion()

    def draw(self):
        pass


    def canDoActions(self):
        return (hasattr(self, "isHitStun") and not self.isHitStun) or not hasattr(self, "isHitStun")


    def movement(self):
        pass

    def speedDecrease(self):
        pass

    def dash(self):
        pass

    def collision(self):
        pass

    def attack(self):
        pass

    def imageGestion(self):
        pass

    def death(self):
        pass


    def applyVector(self, vector): #We give a movement vector and get the new coordinates of the entity
        X = int(self.x//TILE_SIZE)
        Y = int(self.y//TILE_SIZE)

        #We handle horizontal and vertical movement separatly to make problem solving easier

        #Calculate the new position
        new_x = self.x + vector[0]
        new_X = X+pyxel.sgn(vector[0])

        if new_x*pyxel.sgn(vector[0]) > new_X*TILE_SIZE*pyxel.sgn(vector[0]): #If its going faster than 1T/f, reduce its speed to exactly 1T/f
            new_x = new_X*TILE_SIZE

        if vector[0]!=0:
            next_X_1 = map[Y][new_X]
            if self.y != Y*TILE_SIZE:
                next_X_2 = map[Y+1][new_X]
            else:
                next_X_2 = Blocks.GROUND
            #If there's enough space for the entity to move, it moves unimpeded
            if (next_X_1 not in Blocks.WALLS or not collision(new_x, self.y, new_X*TILE_SIZE, Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])) and (next_X_2 not in Blocks.WALLS or not collision(new_x, self.y, new_X*TILE_SIZE, (Y+1)*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])):
                self.x = new_x
            #Else If the movement puts the entity in the wall, we snap it back to the border to prevent clipping.
            elif (next_X_1 in Blocks.WALLS or next_X_2 in Blocks.WALLS) and new_x+self.width>X*TILE_SIZE and (X+1)*TILE_SIZE>new_x:
                self.collidedWithWall = True
                self.x = (new_X-pyxel.sgn(vector[0]))*TILE_SIZE
        
        X = int(self.x//TILE_SIZE)

        #We calculate vertical movement in the same way we do horizontal movement

        new_y = self.y + vector[1]
        new_Y = Y+pyxel.sgn(vector[1])
        
        if new_y*pyxel.sgn(vector[1]) > new_Y*TILE_SIZE*pyxel.sgn(vector[1]):
            new_y = new_Y*TILE_SIZE

        
        if vector[1]!=0:
            next_Y_1 = map[new_Y][X]
            if self.x != X*TILE_SIZE:
                next_Y_2 = map[new_Y][X+1]
            else:
                next_Y_2 = Blocks.GROUND
            
            if (next_Y_1 not in Blocks.WALLS or not collision(self.x, new_y, X*TILE_SIZE, new_Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])) and (next_Y_2 not in Blocks.WALLS or not collision(self.x, new_y, (X+1)*TILE_SIZE, new_Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])):
                self.y = new_y
            elif (next_Y_1 in Blocks.WALLS or next_Y_2 in Blocks.WALLS) and new_y+self.height>Y*TILE_SIZE and (Y+1)*TILE_SIZE>new_y:
                self.collidedWithWall = True
                self.y = (new_Y-pyxel.sgn(vector[1]))*TILE_SIZE


    def initWalk(self, priority, maxSpeed, speedChangeRate, knockbackCoef): #Gets the parameters of the "walk" action
        self.walkPriority = priority
        self.maxSpeed = maxSpeed
        self.speedChangeRate = speedChangeRate
        self.knockbackCoef = knockbackCoef

    def walk(self, vector): #Used for regular walking.
        if self.currentActionPriority <= self.walkPriority:
            self.currentActionPriority = self.walkPriority

            self.applyVector(vector)


    def initDash(self, priority, cooldown, speed, duration): #Gets the parameters of the "dash" action, and initialises the related variables
        self.dashPriority = priority
        self.dashCooldown = cooldown
        self.dashSpeed = speed
        self.dashDuration = duration

        self.isDashing = False
        self.dashStartFrame = 0
        self.dashVector = [0,0]

    def startDash(self, vector): #Used for dashing/lunging
        if self.canStartDash():
            self.currentActionPriority = self.dashPriority

            self.dashStartFrame = game_frame
            self.isDashing = True
            self.dashVector = copy(vector)

    def canStartDash(self):
        return timer(self.dashStartFrame, self.dashCooldown, game_frame) and self.currentActionPriority <= self.dashPriority

    def dashMovement(self):
        if self.dashOngoing():
            self.applyVector([self.dashVector[0]*self.dashSpeed, self.dashVector[1]*self.dashSpeed])

        else :
            self.currentActionPriority = 0
            self.isDashing = False
            self.dashStartFrame = game_frame
            self.momentum = [pyxel.sgn(self.dashVector[0])*self.dashSpeed, pyxel.sgn(self.dashVector[1])*self.dashSpeed]
            self.dashVector = [0,0]

    def dashOngoing(self):
        return not timer(self.dashStartFrame, self.dashDuration, game_frame)  


    def initDeath(self, spawnItem):
        self.deathItemSpawn = spawnItem

        self.dead = False


    def initRangedAttack(self, priority):
        self.rangedAttackPriority = priority
        self.shotsFired = 0

        self.bulletList = []

        self.isReloading = False

    def rangedAttack(self, hand, x, y, team):
        weapon = getattr(self, hand)
        if self.canRangedAttack(hand):

            self.currentActionPriority = self.rangedAttackPriority

            setattr(self, hand+"StartFrame", game_frame)

            weapon["mag_ammo"] -= 1
            self.shotsFired += 1

            for i in range(weapon["bullet_count"]):
                horizontal = x - (self.x + self.width/2)
                vertical = y - (self.y + self.height/2)
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

                bullet_shot = Projectile(weapon, self.x, self.y, [cos,sin], team, self.shotsFired)

                self.bulletList.append(bullet_shot)

    def canRangedAttack(self, hand):
        weapon = getattr(self, hand)
        startFrame = getattr(self, hand+"StartFrame")
        return self.rangedAttackPriority >= self.currentActionPriority and timer(startFrame, weapon["cooldown"], game_frame) and weapon["mag_ammo"]>0

    def reloadWeapon(self, hand):
        weapon = getattr(self, hand)
        if self.canReloadWeapon(hand):
            self.isReloading = False
            if weapon["reserve_ammo"]>=weapon["max_ammo"]:
                weapon["mag_ammo"] = weapon["max_ammo"]
                weapon["reserve_ammo"] -= weapon["max_ammo"]
            else:
                weapon["mag_ammo"] = weapon["reserve_ammo"]
                weapon["reserve_ammo"] = 0

    def canReloadWeapon(self, hand):
        weapon = getattr(self, hand)
        startFrame = getattr(self, hand+"StartFrame")
        return timer(startFrame, weapon["reload"], game_frame) and weapon["reserve_ammo"]>0 and weapon["mag_ammo"]==0

    def initCollision(self, wall, enemy, player):
        self.wallCollisionEffect = wall
        self.enemyCollisionEffect = enemy
        self.playerCollisionEffect = player

    def wallCollision(self):
        if self.wallCollisionEffect[3] != -1:
            if self.collidedWithWall:
                if self.wallCollisionEffect[0] == 0:
                    if type(self) == Enemy or type(self) == Player:
                        self.health = 0
                    elif type(self) == Projectile:
                        self.range = 0

    def canCollideWithEnemy(self):
        return hasattr(self, "enemyCollisionEffect") and self.enemyCollisionEffect[3] != -1

    def canCollideWithPlayer(self):
        return hasattr(self, "playerCollisionEffect") and self.playerCollisionEffect[3] != -1

    def collidingWithEnemy(self, entity):
        return type(entity) == Enemy and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]) and ((hasattr(entity, "isHitStun") and not entity.isHitStun) or not hasattr(entity, "isHitStun"))


    def initHitstun(self, duration, freezeFrame):
        self.hitFreezeFrame = freezeFrame
        self.frozen = 0

        self.hitStunDuration = duration
        self.hitStunStartFrame = 0
        self.isHitStun = False

        self.hitBy = 0

    def hitstun(self):
        if hasattr(self, "isHitStun"):

            if self.isHitStun:
                self.applyVector(self.momentum)
                self.speedDecrease()

            if timer(self.hitStunStartFrame, self.hitStunDuration, game_frame):
                self.isHitStun = False

    def preventOOB(self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        
        if self.x + self.width > WID-1:
            self.x = WID - self.width -1
        if self.y + self.height > HEI -1:
            self.y = HEI - self.height -1



class Pather(Entity):

    def __init__(self, x, y):
        super().__init__(x=x, y=y, width=TILE_SIZE, height=TILE_SIZE)

        self.img = (0,2)
        self.pathImg = (0,3)

        self.moveTo = [0,0]
        self.moveDirection = [0,0]
        self.direction = [0,0]

        self.initWalk(priority=1,maxSpeed=0.9,speedChangeRate=20,knockbackCoef=1)
        self.initPath()

        self.anims = []
    
    def update(self,target):
        if self.canDoActions():
            self.movement(target)
        
        self.updateAnims()

        self.preventOOB()

    def movement(self,target):
        if self.needsPath(target):
            self.movePath()
        else:
            self.moveTowardsTarget(target)

        self.applyVector(self.momentum)

    def moveTowardsTarget(self,target):
        self.moveTo[0] = target[0] - self.x 
        self.moveTo[1] = target[1] - self.y 
        self.getMomentum()

    def needsPath(self,target):
        return self.directPathBlocked(target)

    def directPathBlocked(self,target):
        myPos = blockPos(self.x,self.y)

        targetPos = blockPos(*target)

        self.blockBetweenPlayer = posLineFilled(*myPos, *targetPos)

        for pos in self.blockBetweenPlayer:
            if map[pos[1]][pos[0]] in Blocks.WALLS:
                return True

        return False

    def getMomentum(self):
        #If the player is trying to move, and they're not at max speed, we increase their speed  (and change direction)
        if self.moveTo[1] < 0:
            if self.momentum[1] > -self.maxSpeed:
                self.momentum[1] -= self.maxSpeed/self.speedChangeRate
            self.direction[1] = -1

        if self.moveTo[0] < 0:
            if self.momentum[0] > -self.maxSpeed:
                self.momentum[0] -= self.maxSpeed/self.speedChangeRate
            self.direction[0] = -1

        if self.moveTo[1] > 0:
            if self.momentum[1] < self.maxSpeed:
                self.momentum[1] += self.maxSpeed/self.speedChangeRate
            self.direction[1] = 1

        if self.moveTo[0] > 0:
            if self.momentum[0] < self.maxSpeed:
                self.momentum[0] += self.maxSpeed/self.speedChangeRate
            self.direction[0] = 1
        
        #If the player isn't moving in a specific direction, we lower their speed in that direction progressively
        if not (self.moveTo[1] < 0 or self.moveTo[1] > 0):
            self.momentum[1] -= self.momentum[1]/self.speedChangeRate
            self.direction[1] = 0

        if not(self.moveTo[0] < 0 or self.moveTo[0] > 0):
            self.momentum[0] -= self.momentum[0]/self.speedChangeRate
            self.direction[0] = 0
        
        #If the player is almost immobile in a specific direction, we snap their speed to 0
        if abs(self.momentum[0]) <= 0.01:
            self.momentum[0] = 0
        if abs(self.momentum[1]) <= 0.01:
            self.momentum[1] = 0

        #If the player is almost at max speed in a specific direction, we snap their speed to max speed
        if self.maxSpeed-abs(self.momentum[0]) <= 0.01:
            self.momentum[0] = self.maxSpeed*pyxel.sgn(self.momentum[0])
        if self.maxSpeed-abs(self.momentum[1]) <= 0.01:
            self.momentum[1] = self.maxSpeed*pyxel.sgn(self.momentum[1])

        #If the player is over max speed, we decrease their speed progressively
        if abs(self.momentum[0]) > self.maxSpeed:
            self.momentum[0] -= self.momentum[0]/self.speedChangeRate
        if abs(self.momentum[1]) > self.maxSpeed:
            self.momentum[1] -= self.momentum[1]/self.speedChangeRate 

    def draw(self):
        for pos in self.blockBetweenPlayer:
            show(pos[0]*10,pos[1]*10,(0,3),TILE_SIZE=TILE_SIZE)
        show(self.x, self.y, self.img, TILE_SIZE=TILE_SIZE)

    def updateAnims(self):
        pass

    def initPath(self):
        self.path = []
        self.pathIndex = 0

    def movePath(self):
        pass

    def findNewPath(self,target):
        start = blockPos(self.x,self.y)
        border = [copy(start)]
        newBorder = []
        checked = []
        pathOrigin = copy(map)
        self.pathAt = copy(target)
        self.path = [copy(self.pathAt)]
        cross = [(0,-1),(0,1),(-1,0),(1,0)]
        while len(border) > 0 and target not in checked:
            cross.reverse()
            for pos in border:
                for addon in cross:
                    newPos = (pos[0]+addon[0],pos[1]+addon[1])
                    if newPos not in checked:
                        if is_inside_map(newPos, map):
                            if map[newPos[1]][newPos[0]] == 0:
                                if newPos not in newBorder:
                                    newBorder.append(newPos)
                                    pathOrigin[newPos[1]][newPos[0]] = pos
                checked.append(pos)
            border = copy(newBorder)
            newBorder = []

        if target in checked:
            while self.pathAt != start:

                self.pathAt = copy(pathOrigin[self.pathAt[1]][self.pathAt[0]])
                self.path.insert(0,copy(self.pathAt))

        self.path_index = 0

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, width=TILE_SIZE, height=TILE_SIZE)

        self.img = (1,2)

        self.stunAround = False
        self.keyboard = 'zqsd'
        self.direction = [0,0]

        self.initWalk(priority=1,maxSpeed=1,speedChangeRate=20,knockbackCoef=1)
    
    def movement(self):
        #If the player is trying to move, and they're not at max speed, we increase their speed  (and change direction)
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())):
            if self.momentum[1] > -self.maxSpeed:
                self.momentum[1] -= self.maxSpeed/self.speedChangeRate
            self.direction[1] = -1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())):
            if self.momentum[0] > -self.maxSpeed:
                self.momentum[0] -= self.maxSpeed/self.speedChangeRate
            self.direction[0] = -1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper())):
            if self.momentum[1] < self.maxSpeed:
                self.momentum[1] += self.maxSpeed/self.speedChangeRate
            self.direction[1] = 1

        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())):
            if self.momentum[0] < self.maxSpeed:
                self.momentum[0] += self.maxSpeed/self.speedChangeRate
            self.direction[0] = 1
        
        self.speedDecrease()

        self.walk(self.momentum)
    
    def speedDecrease(self):
        #If the player isn't moving in a specific direction, we lower their speed in that direction progressively
        if not(pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())) or pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper()))):
            self.momentum[1] -= self.momentum[1]/self.speedChangeRate
            self.direction[1] = 0

        if not(pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())) or pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper()))):
            self.momentum[0] -= self.momentum[0]/self.speedChangeRate
            self.direction[0] = 0
        
        #If the player is almost immobile in a specific direction, we snap their speed to 0
        if abs(self.momentum[0]) <= 0.01:
            self.momentum[0] = 0
        if abs(self.momentum[1]) <= 0.01:
            self.momentum[1] = 0

        #If the player is almost at max speed in a specific direction, we snap their speed to max speed
        if self.maxSpeed-abs(self.momentum[0]) <= 0.01:
            self.momentum[0] = self.maxSpeed*pyxel.sgn(self.momentum[0])
        if self.maxSpeed-abs(self.momentum[1]) <= 0.01:
            self.momentum[1] = self.maxSpeed*pyxel.sgn(self.momentum[1])

        #If the player is over max speed, we decrease their speed progressively
        if abs(self.momentum[0]) > self.maxSpeed:
            self.momentum[0] -= self.momentum[0]/self.speedChangeRate
        if abs(self.momentum[1]) > self.maxSpeed:
            self.momentum[1] -= self.momentum[1]/self.speedChangeRate 

    def draw(self):
        show(self.x, self.y, self.img, TILE_SIZE=TILE_SIZE)

        




class Blocks:
    WALLS = [7]
    GROUND = [0]


def blockPos(x,y,TILE_SIZE=10):
    return (round(x/TILE_SIZE),round(y/TILE_SIZE))


def posLineFilled(x0,y0,x1,y1): #not exactly bresenham's algorithm because i dont understand it all yet but ill change it when i do
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
            if i >= 1:
                if positions[-1][0] != positions[-2][0]:
                    positions.append((round(x0 + i * stepX), #i fois le nombre de marche auquel on se trouve
                                    round(y0 + (i-1) * stepY))
                                    )   

                elif positions[-1][1] != positions[-2][1]:
                    positions.append((round(x0 + (i-1) * stepX), #i fois le nombre de marche auquel on se trouve
                                    round(y0 + i * stepY))
                                    )   

    return positions
      

def is_inside_map(pos,map):
    if pos[0] >= len(map[0]) or pos[1] >= len(map):
        return False
    if pos[0] < 0 or pos[1] < 0:
        return False
    return True


App()