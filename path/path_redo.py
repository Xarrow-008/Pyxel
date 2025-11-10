from utility import *

WID = 256
HEI = 256
TILE_SIZE = 16

FPS = 120

map = [[0 for x in range(HEI//TILE_SIZE)] for y in range(WID//TILE_SIZE)]


class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(WID,HEI,fps=FPS)
        pyxel.load('pather.pyxres')
        pyxel.colors[2] = 5373971
        
        self.empty_space()

        self.controller = Controller()
        self.mapper = Mapper()

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.update_map()
        self.update_entities()

    
    def draw(self):
        pyxel.cls(0)
        self.draw_map()
        self.draw_entities()

    def update_map(self):
        self.mapper.update()
        if self.mapper.needs_re_init:
            self.mapper.needs_re_init = False
            self.controller.reinitialize()

    def update_entities(self):
        if self.mapper.can_run():
            self.controller.update()

    def draw_map(self):
        self.mapper.draw()

    def draw_entities(self):
        self.controller.draw()
    


class Mapper:
    def __init__(self):
        global map
        self.needs_re_init = False

    def update(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mouse_place_block(7)

        if pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            self.mouse_place_block(0)

    def mouse_place_block(self,block):
        x = pyxel.mouse_x//TILE_SIZE
        y = pyxel.mouse_y//TILE_SIZE
        try:
            map[y][x] = block
        except:
            pass
        self.needs_re_init = True

    def draw(self):
        self.draw_walls()

    def draw_walls(self):
        for y in range(len(map)):
            for x in range(len(map[y])):
                color = self.map[y][x]
                pyxel.rect(x*10,y*10,10,10,color)

    def can_run(self):
        return not (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT))


        
class Controller:
    def __init__(self):
        self.hider = Hider()
        self.pather = Pather(x=TILE_SIZE, y=TILE_SIZE)

    def update(self):
        self.pather.update(self.hider.x,self.hider.y)
        self.check_interactions()
        self.hider.update()


    def draw(self):
        self.pather.draw()
        self.hider.draw()

    def check_interactions(self):
        if self.hider.stun_around:
            self.hider.stun_around = False
            if distance(self.hider.x,self.hider.y,self.pather.x,self.pather.y) < 20:
                self.pather.stun(120)
    
    def reinitialize(self):
        self.pather.__init__()
        self.hider.__init__()
        


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



class Pather(Entity):

    def __init__(self, x, y):
        super().__init__(x=x, y=y, width=TILE_SIZE, height=TILE_SIZE)

        self.img = (0,2)
        self.path_img = (0,3)

        self.anims = []
    
    def update(self,target):
        if self.can_move():
            self.movement(target)
        
        self.update_anims()

    def movement(self,target):
        if self.needs_path():
            self.move_path()
        else:
            self.move_towards_target(target)

    def needs_path(self):
        pass





class Blocks:
    WALLS = [7]
    GROUND = [0]



App()