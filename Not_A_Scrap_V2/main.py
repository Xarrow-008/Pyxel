import pyxel,os,math,random, csv
from enemies import*
from weapons import*
from copy import deepcopy as copy

KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}

WIDTH = 32
HEIGHT = 32
WID = 256
HEI = 256

TILE_SIZE = 16
FPS = 120

class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(WID,HEI,fps=120)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[2] = 5373971
        
        self.state = Game()      

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.state.update()
            
    def draw(self):
        pyxel.cls(0)
        self.state.draw()    

freeze_start = 0
freeze_duration = 0
freeze_frame = 0
game_frame = 0

class Game:
    def __init__(self):
        self.world = World()
        self.entities = []
        self.player = Player()
        
        self.place = inMission(self.world, self.entities, self.player)

    def update(self):
        global freeze_frame, game_frame
        if not self.player.inInventory:
            
            if not self.isFrozen():
                self.place.update()
                game_frame += 1
            freeze_frame += 1
        
        else:
            self.player.updateInventory()
        
        #Tests for adding weapons
        if keyPress("LEFT_HAND","btn") and pyxel.btn(pyxel.KEY_1):
            self.player.inventory.addWeapon(Weapon.RUSTY_PISTOL, "leftHand")
        if keyPress("LEFT_HAND","btn") and pyxel.btn(pyxel.KEY_2):
            self.player.inventory.addWeapon(Weapon.TEST_2_HANDS, "leftHand")
        if keyPress("RIGHT_HAND","btn") and pyxel.btn(pyxel.KEY_1):
            self.player.inventory.addWeapon(Weapon.RUSTY_PISTOL, "rightHand")
        if keyPress("RIGHT_HAND","btn") and pyxel.btn(pyxel.KEY_2):
            self.player.inventory.addWeapon(Weapon.TEST_2_HANDS, "rightHand")

        #Allows the player to switch weapons between backpack and handheld
        if holdKey("LEFT_HAND", 3*FPS, pyxel.frame_count):
            self.player.inventory.switchWeapon("leftHand")
        if holdKey("RIGHT_HAND", 3*FPS, pyxel.frame_count):
            self.player.inventory.switchWeapon("rightHand")
        

        if keyPress("INVENTORY","btnp"):
            if self.player.inInventory:
                self.player.inInventory = False
            else:
                self.player.inInventory = True

    def draw(self):
        if not self.player.inInventory:
            self.place.draw()
        else:
            pyxel.dither(0.25)
            self.place.draw()
            pyxel.dither(1)
            self.player.drawInventory()

    def isFrozen(self):
        global freeze_start, freeze_duration, freeze_frame, game_frame
        return not timer(freeze_start, freeze_duration, freeze_frame)


class inMission:
    def __init__(self, world, entities, player):
        self.world = world
        self.entities = entities
        self.player = player

    def update(self):
        self.entity_gestion()

        self.player.update()

        self.enemy_collision()
        self.player_collision()
        self.enemy_player_collision()

        if pyxel.btnp(pyxel.KEY_M):
            self.entities.append(Enemy(50, 50, EnemyTemplate.DUMMY))
            
        if pyxel.btnp(pyxel.KEY_O):
            self.hurt(5, [0,0], 1, 0, self.player, self.player)

    def entity_gestion(self):

        if self.player.bulletList != []:
                for bullet in self.player.bulletList:
                    self.entities.append(bullet)
                self.player.bulletList = []
        
        for entity in self.entities:
            
            if hasattr(entity, "bulletList") and entity.bulletList != []:
                for bullet in entity.bulletList:
                    self.entities.append(bullet)
                entity.bulletList = []

            if entity.dead:
                self.entities.remove(entity)
                break
            
            entity.update()

    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                block = self.world.map[y][x]
                draw_block(x*TILE_SIZE,y*TILE_SIZE,0,block)
        
        for entity in self.entities:
            if not entity.dead:
                entity.draw()

        for entity in self.entities:
            if not entity.dead:
                entity.drawOver()
        
        self.player.draw()   

    def heal(self, value, healer, target):
        target.health += value
        if target.health > target.maxHealth:
            target.health = target.maxHealth

    def hurt(self, value, vector, knockback_coef, shot, damager, target):
        global freeze_start, freeze_duration, freeze_frame, game_frame

        if hasattr(target, "isHitStun"):
            if not target.isHitStun or target.hitBy == shot:
                target.health -= value

                target.isHitStun = True
                target.hitStunStartFrame = game_frame

                freeze_start = freeze_frame
                freeze_duration = target.hitFreezeFrame

                target.hitBy = shot
                if hasattr(target, "maxSpeed"):
                    knockback_value = len(str(value))*knockback_coef*target.knockbackCoef
                    target.momentum[0] += vector[0]*knockback_value
                    target.momentum[1] += vector[1]*knockback_value


        else:
            target.health -= value
            if hasattr(target, "maxSpeed"):
                knockback_value = len(str(value))*knockback_coef*target.knockbackCoef
                target.momentum[0] += vector[0]*knockback_value
                target.momentum[1] += vector[1]*knockback_value
                
        target.addAnimationHit((damager.x-4,damager.y-4))
        #print(damager)

    def enemy_collision(self): #Handles collisions with enemies by entities
        original_length = len(self.entities)
        for i in range(len(self.entities)-1): #Entities colliding with enemies
            offset = original_length - len(self.entities)
            entity1 = self.entities[i-offset]
            for j in range(i+1, len(self.entities)):
                offset = original_length - len(self.entities)
                entity2 = self.entities[j-offset]

                if entity1.canCollideWithEnemy() and entity1.collidingWithEnemy(entity2) :
                    self.hurt(entity1.enemyCollisionEffect[0], entity1.enemyCollisionEffect[1], entity1.enemyCollisionEffect[2], entity1.shot, entity1, entity2)
                    if entity1.enemyCollisionEffect[3] == 0:
                        if type(entity1) == Enemy:
                            entity1.health = 0
                        elif type(entity1) == Projectile:
                            entity1.range = 0
                    else:
                        entity1.enemyCollisionEffect[3] -= 1

                if entity2.canCollideWithEnemy() and entity2.collidingWithEnemy(entity1):
                    self.hurt(entity2.enemyCollisionEffect[0], entity2.enemyCollisionEffect[1], entity2.enemyCollisionEffect[2], entity2.shot, entity2, entity1)
                    if entity2.enemyCollisionEffect[3] == 0:
                        if type(entity2) == Enemy:
                            entity2.health = 0
                        elif type(entity2) == Projectile:
                            entity2.range = 0
                    else:
                        entity2.enemyCollisionEffect[3] -= 1

    def player_collision(self): #Handles collisions with the player by entities
        for entity in self.entities:
            if entity.canCollideWithPlayer() and self.entityCollidingWithPlayer(entity):
                self.hurt(entity.playerCollisionEffect[0], entity.player_collisionEffect[1], entity.player_collisionEffect[2], entity.shot, entity, self.player)
                if entity.playerCollisionEffect[3] == 0:
                    entity.dead = True
                else:
                    entity.playerCollisionEffect[3] -= 1

    def enemy_player_collision(self): #Handles what happens when a player collides with an enemy
        for entity in self.entities:
            if self.player.collidingWithEnemy(entity):
                pass #Right now, there isn't anything that happens when the player collides with an enemy

    def entityCollidingWithPlayer(self, entity):
        return collision(self.player.x, self.player.y, entity.x, entity.y, [self.player.width, self.player.height], [entity.width, entity.height]) and not self.player.isHitStun


class Entity: #General Entity class with all the methods describing what entities can do
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.momentum = [0,0]

        self.collidedWithWall = False

        self.currentActionPriority = 0

        self.anims = []

    def __str__(self):
        if type(self) == Player:
            return f"Type : Player, x : {self.x}, y : {self.y}, momentum : {self.momentum}"
        elif type(self) == Enemy:
            return f"Type : Enemy, x : {self.x}, y : {self.y}, momentum : {self.momentum}"
        elif type(self) == Projectile:
            return f"Type : Projectile, x : {self.x}, y : {self.y}, momentum : {self.momentum}"

    def update(self):

        self.hitstun()

        if  self.canDoActions():

            self.movement()

            self.dash()

            self.collision()

            self.attack()

        self.death()

        self.imageGestion()

        self.updateAnims()

    def draw(self):
        pass

    def drawOver(self):
        self.drawAnims()

    def drawAnims(self):
        for anim in self.anims:
            anim.draw(self.x,self.y)

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

    def updateAnims(self):
        for anim in self.anims:
            anim.update()
            if anim.is_dead():
                self.anims.remove(anim)

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
                self.x = new_X*TILE_SIZE - pyxel.sgn(vector[0])*self.width
        
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
                self.y = new_Y*TILE_SIZE - pyxel.sgn(vector[1])*self.height


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

    def rangedAttack(self, hand, x, y, team):
        weapon = getattr(self.inventory, hand)
        if self.canRangedAttack(hand):

            self.currentActionPriority = self.rangedAttackPriority

            setattr(self.inventory, hand+"StartFrame", game_frame)

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
        weapon = getattr(self.inventory, hand)
        startFrame = getattr(self.inventory, hand+"StartFrame")
        return self.rangedAttackPriority >= self.currentActionPriority and timer(startFrame, weapon["cooldown"], game_frame) and weapon["mag_ammo"]>0

    def reloadWeapon(self, hand):
        weapon = getattr(self.inventory, hand)
        if self.canReloadWeapon(hand):
            setattr(self.inventory, hand+"IsReloading", False)
            if weapon["reserve_ammo"]>=weapon["max_ammo"]:
                weapon["mag_ammo"] = weapon["max_ammo"]
                weapon["reserve_ammo"] -= weapon["max_ammo"]
            else:
                weapon["mag_ammo"] = weapon["reserve_ammo"]
                weapon["reserve_ammo"] = 0
                setattr(self.inventory, hand+"CanNoLongerReload", True)

    def canReloadWeapon(self, hand):
        weapon = getattr(self.inventory, hand)
        startFrame = getattr(self.inventory, hand+"StartFrame")
        return timer(startFrame, weapon["reload"], game_frame) and weapon["mag_ammo"]==0



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

    def addAnimationHit(self,pos):
        self.addAnimation(pos=(pos[0],pos[1],False),settings={'u':0,'v':1,'length':5},lifetime='1 cycle')

    def addAnimation(self,pos=(0,0),settings=0,lifetime=1):
        self.anims.append(Animation(pos,settings,lifetime))

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

class Player(Entity): #Creates an entity that's controlled by the player
    def __init__(self):
        super().__init__(x=10, y=10, width=TILE_SIZE, height=TILE_SIZE)

        self.characterName = "Scrapper"
        self.characterUpside1 = "This character has no upsides"
        self.characterUpside2 = "This character has no upsides"
        self.characterDownside1 = "This character has no downsides"
        self.characterDownside2 = "This character has no downsides"

        self.keyboard = 'zqsd'

        self.health = 80
        self.maxHealth = 80

        self.initWalk(priority=0, maxSpeed=0.5, speedChangeRate=20, knockbackCoef=1)
        self.initDash(priority=1, cooldown=40, speed=1.5, duration=20)
        self.initRangedAttack(priority=0)
        self.initHitstun(duration=0*FPS, freezeFrame=1*FPS)

        self.inventory = Inventory()
        self.inventory.addWeapon(Weapon.RUSTY_PISTOL, "leftHand")
        
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

        self.inInventory = False
        self.inventoryPosition = 2*WID
        self.inventoryIsMoving = False
        self.inventoryStartFrame = 0
        self.inventoryDirection = 0

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


        
        if not self.inInventory: #The player info isn't shown while the player is in the inventory, since that justs makes it look weird (and also they have that info on the inventory)

            #Health bar
            pyxel.rect(x=1,y=1,w=42,h=10,col=0)

            health_bar_size = int(40*(self.health/self.maxHealth))

            pyxel.rect(x=2,y=2,w=health_bar_size,h=8,col=8)
            sized_text(x=12, y=3, s=str(self.health)+"/"+str(self.maxHealth),col=7,size=7)


            #Dash
            pyxel.rect(x=44,y=1,w=13,h=11,col=0)

            if not self.isDashing:
                dash_cooldown_progress = int(34*((game_frame-self.dashStartFrame)/self.dashCooldown))
                x = 50
                y = 2
                for i in range(40):
                    if dash_cooldown_progress >= i:
                        pyxel.pset(x,y,col=11)
                    else:
                        pyxel.pset(x,y,col=8)
                    if i in range(0,5) or i in range(35,40):
                        x += 1
                    elif i in range(6,14):
                        y += 1
                    elif i in range(15,25):
                        x -= 1
                    elif i in range(26,34):
                        y -= 1
            else:
                pyxel.rectb(x=45,y=2,w=11,h=9,col=13)

            draw(x=46,y=3,img=0,u=104,v=248,w=8,h=7,colkey=11)


            #Weapons
            pyxel.rectb(x=1, y=218, w=18, h=18, col=0)
            pyxel.rect(x=2, y=219, w=16, h=16, col=13)
            draw(x=2, y=219, img=0, u=self.inventory.leftHand["image"][0], v=self.inventory.leftHand["image"][1], w=self.inventory.leftHand["width"], h=self.inventory.leftHand["height"], colkey=11)
            if self.inventory.leftHand != Weapon.NONE:
                sized_text(x=21, y=224, s=str(self.inventory.leftHand["mag_ammo"])+"/"+str(self.inventory.leftHand["max_ammo"])+"("+str(self.inventory.leftHand["reserve_ammo"])+")", col=7)


            pyxel.rectb(x=1, y=237, w=18, h=18, col=0)
            pyxel.rect(x=2, y=238, w=16, h=16, col=13)
            draw(x=2, y=238, img=0, u=self.inventory.rightHand["image"][0], v=self.inventory.rightHand["image"][1], w=self.inventory.rightHand["width"], h=self.inventory.rightHand["height"], colkey=11)
            if self.inventory.rightHand != Weapon.NONE:
                sized_text(x=21, y=243, s=str(self.inventory.rightHand["mag_ammo"])+"/"+str(self.inventory.rightHand["max_ammo"])+" ("+str(self.inventory.rightHand["reserve_ammo"])+")", col=7)


    def updateInventory(self):
        if not self.inventoryIsMoving:

            if self.moveInventoryLeft():
                self.inventoryStartFrame = pyxel.frame_count
                self.inventoryIsMoving = True
                self.inventoryDirection = -1

            if self.moveInventoryRight():
                self.inventoryStartFrame = pyxel.frame_count
                self.inventoryIsMoving = True
                self.inventoryDirection = 1

        else:
            self.moveInventory()

    def moveInventoryLeft(self):
        return self.inventoryPosition != 0 and (pyxel.btnp(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>=1 and pyxel.mouse_x<=7 and pyxel.mouse_y>=123 and pyxel.mouse_y<=130))

    def moveInventoryRight(self):
        return self.inventoryPosition != 2*WID and (pyxel.btnp(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>=WID-8 and pyxel.mouse_x<=WID-2 and pyxel.mouse_y>=123 and pyxel.mouse_y<=130)) 

    def moveInventory(self):
        inventoryFrame = pyxel.frame_count - self.inventoryStartFrame

        if inventoryFrame == 1:
            self.inventoryPosition += 6*self.inventoryDirection

        elif inventoryFrame in [x for x in range(2,16)]:
            self.inventoryPosition += 12*self.inventoryDirection

        elif inventoryFrame in [x for x in range(16,21)]:
            self.inventoryPosition += 6*self.inventoryDirection

        elif inventoryFrame in [x for x in range(21,27)]:
            self.inventoryPosition += 4*self.inventoryDirection

        elif inventoryFrame in [x for x in range(27,41)]:
            self.inventoryPosition += 2*self.inventoryDirection

        else:
            self.inventoryIsMoving = False

    def drawInventory(self):
        if self.inventoryPosition < WID:
            self.drawInventoryCharacterScreen(-self.inventoryPosition)
        if self.inventoryPosition != 0 and self.inventoryPosition != 2*WID:
            self.drawInventoryWeaponScreen(WID-self.inventoryPosition)
        if self.inventoryPosition > WID:
            self.drawInventoryItemScreen(2*WID-self.inventoryPosition)

        if self.inventoryPosition == WID or self.inventoryPosition == 2*WID:
            pyxel.rectb(x=-1, y=121, w=11, h=11, col=7)
            pyxel.rect(x=0, y=122, w=9, h=9, col=0)
            draw(x=1, y=123, img=0, u=0, v=208, w=7, h=7, colkey=11)
        if self.inventoryPosition == 0 or self.inventoryPosition == WID:
            pyxel.rectb(x=WID-10, y=121, w=11, h=11, col=7)
            pyxel.rect(x=WID-9, y=122, w=9, h=9, col=0)
            draw(x=WID-8, y=123, img=0, u=8, v=208, w=7, h=7, colkey=11)   

    def drawInventoryCharacterScreen(self, x):

        #Character information frame
        pyxel.rectb(x=x+5, y=5, w=246, h=90, col=7)
        pyxel.rect(x=x+6, y=6, w=244, h=88, col=0)

        #Character image
        pyxel.rectb(x=x+10, y=10, w=36, h=36, col=7)
        draw(x=x+12, y=12, img=0, u=112, v=64, w=TILE_SIZE, h=TILE_SIZE, colkey=11, scale=2)
        draw(x=x+12, y=12, img=0, u=112, v=96, w=TILE_SIZE, h=TILE_SIZE, colkey=11, scale=2)

        #Character name
        sized_text(x=x+70, y=22, s=f"CHARACTER : {self.characterName}", col=7, size=13)

        #Character stats
        sized_text(x=x+10, y=50, s=f"Health : {self.health}/{self.maxHealth}", col=7, size=6)
        sized_text(x=x+10, y=57, s=f"Speed : {round(self.maxSpeed*FPS/TILE_SIZE, 2)} T/s", col=7, size=6)
        sized_text(x=x+10, y=64, s=f"Dash cooldown : {round(self.dashCooldown/FPS,2)}s", col=7, size=6)

        #Character upsides and downsides
        pyxel.rectb(x=x+10, y=97, w=117, h=45, col=7)
        pyxel.rect(x=x+11, y=98, w=115, h=43, col=0)
        sized_text(x=x+14, y=101, s="Upside 1", col=7, size=6)
        sized_text(x=x+14, y=110, s=self.characterUpside1, col=7, size=6, limit=x+127)

        pyxel.rectb(x=x+128, y=97, w=118, h=45, col=7)
        pyxel.rect(x=x+129, y=98, w=116, h=43, col=0)
        sized_text(x=x+132, y=101, s="Downside 1", col=7, size=6)
        sized_text(x=x+132, y=110, s=self.characterDownside1, col=7, size=6, limit=x+246)

        pyxel.rectb(x=x+10, y=144, w=117, h=45, col=7)
        pyxel.rect(x=x+11, y=145, w=115, h=43, col=0)
        sized_text(x=x+14, y=146, s="Upside 2", col=7, size=6)
        sized_text(x=x+14, y=155, s=self.characterUpside2, col=7, size=6, limit=x+127)

        pyxel.rectb(x=x+128, y=144, w=118, h=45, col=7)
        pyxel.rect(x=x+129, y=145, w=116, h=43, col=0)
        sized_text(x=x+132, y=146, s="Downside 2", col=7, size=6)
        sized_text(x=x+132, y=155, s=self.characterDownside2, col=7, size=6, limit=x+246)

    def drawInventoryWeaponScreen(self, x):
        self.drawSlot(x+10, 5, "leftHand")
        self.drawSlot(x+129, 5, "rightHand")
        
        if self.inventory.canHaveTwoWeaponsInBackPack:
            self.drawSlot(x+10, 98, "backpack1")
            self.drawSlot(x+129, 98, "backpack2")
        else:
            self.drawSlot(x+69, 98, "backpack1")

    def drawWeaponSlot(self, x, y, hand):
        weapon = getattr(self.inventory, hand)
        if hand == "leftHand":
            text = "Lefthand weapon"
        elif hand == "rightHand":
            text = "Righthand weapon"
        elif hand == "backpack1":
            if self.inventory.canHaveTwoWeaponsInBackPack:
                text = "Stored weapon 1"
            else:
                text = "Stored weapon"
        elif hand == "backpack2":
            text = "Stored weapon 2"


        sized_text(x=x+4, y=y+4, s=text, col=7, size=7)

        pyxel.rect(x=x+4, y=y+13, w=18, h=18, col=7)
        draw(x=x+5, y=y+14, img=0, u=weapon["image"][0], v=weapon["image"][1], w=TILE_SIZE, h=TILE_SIZE, colkey=11)
        if weapon != Weapon.NONE:
            sized_text(x=x+25, y=y+18, s=f"{weapon["name"]} (LVL 1)", col=7) #We'll have to change this part once we add scaling to the weapons
            
            if "backpack" not in hand and getattr(self.inventory, hand+"IsReloading"):
                sized_text(x=x+25, y=y+25, s="Reloading", col=7)
                current_frame = pyxel.frame_count%120
                if current_frame >= 30:
                    pyxel.pset(x=x+61, y=y+29, col=7)
                if current_frame >= 60:
                    pyxel.pset(x=x+65, y=y+29, col=7)
                if current_frame >= 90:
                    pyxel.pset(x=x+69, y=y+29, col=7)



            sized_text(x=x+4, y=y+34, s=f"Damage : {weapon["damage"]}", col=7)
            sized_text(x=x+4, y=y+41, s=f"Piercing : {weapon["piercing"]}", col=7)
            sized_text(x=x+4, y=y+48, s=f"Attack speed : {round(FPS/(weapon["cooldown"]),2)} ATK/s", col=7)
            sized_text(x=x+4, y=y+55, s=f"Reload time : {round((weapon["reload"])/FPS,2)}s", col=7)
            sized_text(x=x+4, y=y+62, s=f"Ammo : {weapon["mag_ammo"]}/{weapon["max_ammo"]} ({weapon["reserve_ammo"]})", col=7)
            sized_text(x=x+4, y=y+69, s=f"Bullet count : {weapon["bullet_count"]}", col=7)
            sized_text(x=x+4, y=y+76, s=f"Spread : {weapon["spread"]}°", col=7)
            sized_text(x=x+4, y=y+83, s=f"Range : {round(weapon["range"]/TILE_SIZE,2)}T", col=7)
        else:
            sized_text(x=x+25, y=y+18, s=f"{weapon["name"]}", col=7)

    def drawOccupiedSlot(self, x, y):
        w = 122
        h = 91

        pyxel.line(x1=x, y1=y, x2=x+w,y2=y+h, col=7)
        pyxel.line(x1=x, y1=y+h, x2=x+w, y2=y, col=7)

        inner_rect_width = int(w/2)
        inner_rect_height = int(h/2)
        inner_rect_x = int(x+w/2) - int(inner_rect_width/2)
        inner_rect_y = int(y+h/2) - int(inner_rect_height/2)

        pyxel.rectb(x=inner_rect_x, y=inner_rect_y, w=inner_rect_width, h=inner_rect_height, col=7)
        pyxel.rect(x=inner_rect_x+1, y=inner_rect_y+1, w=inner_rect_width-2, h=inner_rect_height-2, col=0)

        sized_text(x=inner_rect_x+2, y=inner_rect_y+8, s="This slot is occupied by a two-handed weapon in another slot", col=7, limit=inner_rect_x+inner_rect_width-1)

    def drawSlot(self, x, y, hand):
        pyxel.rectb(x=x, y=y, w=117, h=91, col=7)
        pyxel.rect(x=x+1, y=y+1, w=115, h=89, col=0)
        if getattr(self.inventory, hand+"Occupied"):
            self.drawOccupiedSlot(x,y)
        else:
            self.drawWeaponSlot(x,y,hand)

    def drawInventoryItemScreen(self, x):
        pyxel.rectb(x=x+25, y=200, w=205, h=50, col=7)
        pyxel.rect(x=x+26, y=201, w=203, h=48, col=0)
        sized_text(x=x+27, y=202, s=f"Description", col=7, limit=x+230)
        sized_text(x=x+27, y=212, s=f"Hover over an item to see its description (We currently haven't implemented any items)", col=7, limit=x+230)


    def movement(self):
        #If the player is trying to move, and they're not at max speed, we increase their speed  (and change direction)
        if keyPress("UP","btn"):
            if self.momentum[1] > -self.maxSpeed:
                self.momentum[1] -= self.maxSpeed/self.speedChangeRate
            self.direction[1] = -1

        if keyPress("LEFT","btn"):
            if self.momentum[0] > -self.maxSpeed:
                self.momentum[0] -= self.maxSpeed/self.speedChangeRate
            self.direction[0] = -1

        if keyPress("DOWN","btn"):
            if self.momentum[1] < self.maxSpeed:
                self.momentum[1] += self.maxSpeed/self.speedChangeRate
            self.direction[1] = 1

        if keyPress("RIGHT","btn"):
            if self.momentum[0] < self.maxSpeed:
                self.momentum[0] += self.maxSpeed/self.speedChangeRate
            self.direction[0] = 1
        
        self.speedDecrease()

        self.walk(self.momentum)
    
    def speedDecrease(self):
        #If the player isn't moving in a specific direction, we lower their speed in that direction progressively
        if not(keyPress("UP","btn") or keyPress("DOWN","btn")):
            self.momentum[1] -= self.momentum[1]/self.speedChangeRate
            self.direction[1] = 0

        if not(keyPress("LEFT","btn") or keyPress("RIGHT","btn")):
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

    def dash(self):
        if self.isDashing:
            self.dashMovement()
        elif keyPress("DASH","btnp"):
            self.startDash(self.direction)
            
    def attack(self):
        if keyPress("ATTACK_LEFT", "btn"):
            self.rangedAttack("leftHand", pyxel.mouse_x, pyxel.mouse_y, "player")

        if keyPress("ATTACK_RIGHT", "btn"):
            self.rangedAttack("rightHand", pyxel.mouse_x, pyxel.mouse_y, "player")

        if keyPress("LEFT_HAND","btn") and keyPress("RELOAD","btn") and not self.inventory.leftHandIsReloading and not self.inventory.leftHandCanNoLongerReload:
            self.inventory.leftHand["mag_ammo"] = 0
            self.inventory.leftHandStartFrame = game_frame
            self.inventory.leftHandIsReloading = True

        if keyPress("RIGHT_HAND","btn") and keyPress("RELOAD","btn") and not self.inventory.rightHandIsReloading and not self.inventory.rightHandCanNoLongerReload:
            self.inventory.rightHand["mag_ammo"] = 0
            self.inventory.rightHandStartFrame = game_frame
            self.inventory.rightHandIsReloading = True
        

        if self.inventory.leftHand["mag_ammo"] == 0 and not self.inventory.leftHandIsReloading and not self.inventory.leftHandCanNoLongerReload:
            self.inventory.leftHandStartFrame = game_frame
            self.inventory.leftHandIsReloading = True

        if self.inventory.rightHand["mag_ammo"] == 0 and not self.inventory.rightHandIsReloading and not self.inventory.rightHandCanNoLongerReload:
            self.inventory.rightHandStartFrame = game_frame
            self.inventory.rightHandIsReloading = True

        self.reloadWeapon("leftHand")
        self.reloadWeapon("rightHand")

    def imageGestion(self):
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

    def collision(self):
        pass

    def death(self):
        pass

class Enemy(Entity): #Creates an entity that fights the player
    def __init__(self, x, y, template):
        super().__init__(x=x, y=y, width=template["width"], height=template["height"])

        self.originalImage = template["image"]
        self.image = template["image"]

        self.health = template["health"]
        self.maxHealth = template["max_health"]

        #We initialise all of the enemies abilities
        for ability in template["abilities"].items():
            
            initialiser = getattr(self, "init"+ability[0])
            parameters = ability[1].values()
            initialiser(*parameters)

        self.inventory = Inventory()

    def draw(self):
        draw(self.x, self.y, 0, self.image[0], self.image[1], self.width, self.height, colkey=11)

    def movement(self):

        self.speedDecrease

        self.walk(self.momentum)

    def speedDecrease(self):
        #These two lines are temporary and will be removed once we have pathing. They're just there to make sure the speed decreases
        self.momentum[0] -= self.momentum[0]/self.speedChangeRate
        self.momentum[1] -= self.momentum[1]/self.speedChangeRate

        if abs(self.momentum[0]) <= 0.01:
            self.momentum[0] = 0
        if abs(self.momentum[1]) <= 0.01:
            self.momentum[1] = 0

    def dash(self):
        pass

    def collision(self):
        pass

    def attack(self):
        pass

    def imageGestion(self):
        if self.canDoActions():
            self.image = self.originalImage
        else:
            self.image = [self.originalImage[0]+TILE_SIZE, self.originalImage[1]]

    def death(self):
        if self.health <= 0 and not self.dead:
            self.dead = True

class Inventory:
    def __init__(self):
        self.leftHand = Weapon.NONE
        self.leftHandOccupied = False
        self.leftHandStartFrame = 0
        self.leftHandIsReloading = False
        self.leftHandCanNoLongerReload = False

        self.rightHand = Weapon.NONE
        self.rightHandOccupied = False
        self.rightHandStartFrame = 0
        self.rightHandIsReloading = False
        self.rightHandCanNoLongerReload = False

        self.backpack1 = Weapon.NONE
        self.backpack1Occupied = False

        self.canHaveTwoWeaponsInBackPack = True

        self.backpack2 = Weapon.NONE
        self.backpack2Occupied = False

        

    def addWeapon(self, weapon, hand): #Function used when the player picks up a weapon

        setattr(self, hand, weapon)

        #We can almost definitely make this more efficient but this works and is understandable

        if not self.canHaveTwoWeaponsInBackPack:

            if self.backpack1["hand_number"]==1:

                setattr(self, hand+"Occupied", False)

                #We check wether or not its a two handed weapon to block off the other hand
                if weapon["hand_number"]==1:
                    setattr(self, self.oppositeHand(hand)+"Occupied", False)
                    if getattr(self, self.oppositeHand(hand))["hand_number"]==2:
                        setattr(self, self.oppositeHand(hand), Weapon.NONE)

                elif weapon["hand_number"]==2:
                    setattr(self, self.oppositeHand(hand)+"Occupied", True)
                    setattr(self, self.oppositeHand(hand), Weapon.NONE)

            elif self.backpack1["hand_number"]==2:

                if getattr(self, hand+"Occupied"):
                    self.backpack1 = Weapon.NONE
                    setattr(self, hand+"Occupied", False)

                    if weapon["hand_number"]==2:
                        setattr(self, self.oppositeHand(hand)+"Occupied", True)
                        setattr(self, self.oppositeHand(hand), Weapon.NONE)

                else:
                    setattr(self, hand+"Occupied", False)
                    if weapon["hand_number"]==2:
                        setattr(self, self.oppositeHand(hand)+"Occupied", True)
                        setattr(self, self.oppositeHand(hand), Weapon.NONE)
                        self.backpack1 = Weapon.NONE

        else:
            setattr(self, hand+"Occupied", False)
            #We check wether or not its a two handed weapon to block off the other hand
            if weapon["hand_number"]==1:
                setattr(self, self.oppositeHand(hand)+"Occupied", False)
                if getattr(self, self.oppositeHand(hand))["hand_number"]==2:
                    setattr(self, self.oppositeHand(hand), Weapon.NONE)

            elif weapon["hand_number"]==2:
                setattr(self, self.oppositeHand(hand)+"Occupied", True)
                setattr(self, self.oppositeHand(hand), Weapon.NONE)

    def switchWeapon(self, hand): #Function used to switch hand-held weapons with ones stored in the backpack
        
        #This is also ugly, but its the best I'm gonna do right now

        if not self.canHaveTwoWeaponsInBackPack:

            if self.backpack1["hand_number"]==1:

                setattr(self, hand+"Occupied", False)
                
                if self.leftHand["hand_number"]==2:
                    weapon = self.leftHand
                    setattr(self, hand, self.backpack1)
                    self.backpack1 = weapon

                    setattr(self, self.oppositeHand(hand)+"Occupied", True)
                    setattr(self, self.oppositeHand(hand), Weapon.NONE)

                elif self.rightHand["hand_number"]==2:
                    weapon = self.rightHand
                    setattr(self, hand, self.backpack1)
                    self.backpack1 = weapon

                    setattr(self, self.oppositeHand(hand)+"Occupied", True)
                    setattr(self, self.oppositeHand(hand), Weapon.NONE)

                else:
                    weapon = getattr(self, hand)
                    setattr(self, hand, self.backpack1)
                    self.backpack1 = weapon

            else:
                if getattr(self, hand+"Occupied"):
                    setattr(self, hand+"Occupied", False)

                    setattr(self, hand, self.backpack1)
                    self.backpack1 = getattr(self, self.oppositeHand(hand))

                    setattr(self, self.oppositeHand(hand), Weapon.NONE)
                    setattr(self, self.oppositeHand(hand)+"Occupied", True)

                else:
                    weapon = getattr(self, hand)
                    setattr(self, hand, self.backpack1)
                    self.backpack1 = weapon

        else:
            
            if self.backpack1["hand_number"]==2:
                weapon = self.backpack1
                
                setattr(self, self.equivalentHand(hand), getattr(self, hand))
                setattr(self, self.equivalentHand(self.oppositeHand(hand)), getattr(self, self.oppositeHand(hand)))
                setattr(self, hand, weapon)

                setattr(self, self.oppositeHand(hand), Weapon.NONE)
                setattr(self, hand+"Occupied", False)
                setattr(self, self.oppositeHand(hand)+"Occupied", True)

                if self.backpack1["hand_number"]==2:
                    self.backpack2Occupied = True
                else:
                    self.backpack2Occupied = False
                if self.backpack2["hand_number"]==2:
                    self.backpack1Occupied = True
                else:
                    self.backpack1Occupied = False

            elif self.backpack2["hand_number"]==2:
                weapon = self.backpack2
                
                setattr(self, self.equivalentHand(hand), getattr(self, hand))
                setattr(self, self.equivalentHand(self.oppositeHand(hand)), getattr(self, self.oppositeHand(hand)))
                setattr(self, hand, weapon)

                setattr(self, self.oppositeHand(hand), Weapon.NONE)
                setattr(self, hand+"Occupied", False)
                setattr(self, self.oppositeHand(hand)+"Occupied", True)

                if self.backpack1["hand_number"]==2:
                    self.backpack2Occupied = True
                else:
                    self.backpack2Occupied = False
                if self.backpack2["hand_number"]==2:
                    self.backpack1Occupied = True
                else:
                    self.backpack1Occupied = False
            else:
                weapon1 = self.backpack1
                weapon2 = self.backpack2

                setattr(self, self.equivalentHand(hand), getattr(self, hand))
                setattr(self, self.equivalentHand(self.oppositeHand(hand)), getattr(self, self.oppositeHand(hand)))

                setattr(self, hand, weapon1)
                setattr(self, self.oppositeHand(hand), weapon2)

                self.leftHandOccupied = False
                self.rightHandOccupied = False

                if self.backpack1["hand_number"]==2:
                    self.backpack2Occupied = True
                else:
                    self.backpack2Occupied = False
                if self.backpack2["hand_number"]==2:
                    self.backpack1Occupied = True
                else:
                    self.backpack1Occupied = False
               

    def oppositeHand(self,hand):
        if hand == "leftHand":
            return "rightHand"
        if hand == "rightHand":
            return "leftHand"
        if hand == "backpack1":
            return "backpack2"
        if hand == "backpack2":
            return "backpack1"

    def equivalentHand(self, hand):
        if hand == "leftHand":
            return "backpack1"
        if hand == "rightHand":
            return "backpack2"


class Projectile(Entity) : #Creates a projectile that can hit other entitiesz
    def __init__(self, weapon, x, y, vector, team, shot):
        super().__init__(x=x, y=y, width=weapon["bullet_width"], height=weapon["bullet_height"])

        self.momentum = vector

        self.image = weapon["bullet_image"]

        self.damage = weapon["damage"]
        self.piercing = weapon["piercing"]

        self.range = weapon["range"]

        self.team = team

        self.shot = shot

        self.initWalk(priority=0, maxSpeed=weapon["bullet_speed"], speedChangeRate=0, knockbackCoef=0)
        self.initDeath(spawnItem=False)
        if self.team == "player":
            self.initCollision([0, 0, 0, 0], [self.damage, self.momentum, weapon["knockback_coef"], self.piercing], [0, 0, 0, -1])
        if self.team == "enemy":
            self.initCollision([0, 0, 0, 0], [0, 0, 0, -1], [self.damage, self.momentum, weapon["knockback_coef"], self.piercing])

    def draw(self):
        draw(self.x, self.y, 0, self.image[0], self.image[1], self.width, self.height, colkey=11)

    def movement(self):
        self.walk([self.momentum[0]*self.maxSpeed, self.momentum[1]*self.maxSpeed])
        self.range -= math.sqrt((self.momentum[0]*self.maxSpeed)**2 + (self.momentum[1]*self.maxSpeed)**2)

    def dash(self):
        pass

    def collision(self):
        self.wallCollision()

    def attack(self):
        pass

    def imageGestion(self):
        pass

    def death(self):
        if self.range <= 0:
            self.dead = True


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


class Blocks:
    WALLS = [(0,0),(1,0),(2,0),(3,0)]
    WALLS_DOWN = [(0,0),(1,0)]
    WALLS_UP = [(2,0),(3,0)]

    GROUND = [(0,1)]

map = []

class World:
    def __init__(self):
        global map
        self.map = [[random.choice(Blocks.GROUND) for x in range(WIDTH)] for y in range(HEIGHT)]
        self.map[5][6] = Blocks.WALLS[0]
        map = self.map


class Animation:
    def __init__(self,pos,settings,lifetime):
        self.start = pyxel.frame_count
        self.settings = settings
        self.lifetime = lifetime
        self.pos = pos
        self.posRelative = True
        self.default_set = {'u':0,'v':0,'width':TILE_SIZE,'heigth':TILE_SIZE,'vector':(1,0),'length':3,'duration':10}

        self.apply_settings()


        self.img = (self.settings['u'],self.settings['v'])
        self.kill = False

    def update(self):
        if not self.is_dead():
            self.get_img()
            
    def draw(self,x,y):
        if self.posRelative:
            show(x + self.pos[0], y + self.pos[1], self.img, colkey=0, save=1)
        else:
            show(self.pos[0], self.pos[1], self.img, colkey=0, save=1)
        
    def get_img(self):
        frame_anim = (self.frame() // self.settings['duration']) % self.settings['length']
        x = self.settings['u'] + self.settings['vector'][0]*frame_anim
        y = self.settings['v'] + self.settings['vector'][1]*frame_anim
        self.img = (x,y)

        #print(x,y,flush=True)

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
            self.lifetime = self.settings['duration']*self.settings['length']*nb - 1


        if len(self.pos) > 2:
            if type(self.pos[2]) is bool:
                self.posRelative = self.pos[2]
            self.pos = (self.pos[0],self.pos[1])

    def is_dead(self):
        return pyxel.frame_count > self.start + self.lifetime or self.kill

    def frame(self):
        return pyxel.frame_count - self.start
      


def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

def timer(start_frame, duration, counter):
    return counter - start_frame >= duration

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

def sized_text(x, y, s, col, size=6, limit=256): #Like pyxel.text, but you can modify the size of the text
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    other_characters = ["0","1","2","3","4","5","6","7","8","9",",","?",";",".",":","/","!","'","(",")","[","]","{","}","-","_","°"]

    current_x = x

    scale = size/6

    for i in range(len(s)):
        chr = s[i]
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

        if chr != " ":
            pyxel.pal(0,col)
            draw(current_x, y, 0, u, v, w, h, scale=scale, colkey=11)
            pyxel.pal()

        if not(chr==" " and current_x==x):
            current_x += int(4*scale)

        if current_x + 2*int(4*scale) >= limit: #Make the text wrap around if it goes past the limit
            if chr != " " and not (i<len(s)-1 and s[i+1]==" "):
                pyxel.pal(0,col)
                draw(current_x, y, 0, 96, 238, w, h, scale=scale, colkey=11)
                pyxel.pal()
            current_x = x
            y += int(6*scale)

def import_csv(file):
    tab = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            tab.append(line)
    return tab

keybinds = import_csv("Not_A_Scrap_V2/keybinds.csv")

def keyPress(action, method):
    for dic in keybinds:
        if dic["action"]==action:
            if "MOUSE" in dic["key"]:
                key = dic["key"]
            else:
                key = "KEY_"+dic["key"]
    
    if method=="btn":
        return pyxel.btn(getattr(pyxel, key))
    elif method=="btnp":
        return pyxel.btnp(getattr(pyxel, key))

heldKeyStartFrame = 0
holdingKey = False
keyBeingHeld = None

def holdKey(action, duration, counter):
    global heldKeyStartFrame, holdingKey, keyBeingHeld
    for dic in keybinds:
        if dic["action"]==action:
            if "MOUSE" in dic["key"]:
                key = dic["key"]
            else:
                key = "KEY_"+dic["key"]
    if holdingKey and key==keyBeingHeld and pyxel.btn(getattr(pyxel,key)):
        if timer(heldKeyStartFrame, duration, counter):
            holdingKey = False
        return timer(heldKeyStartFrame, duration, counter)
    elif pyxel.btn(getattr(pyxel,key)):
        heldKeyStartFrame = counter
        holdingKey = True
        keyBeingHeld = key
    else:
        pressingAKey = False
        for dic in keybinds:
            if "MOUSE" in dic["key"]:
                if pyxel.btn(getattr(pyxel,dic["key"])):
                    pressingAKey = True
            else:
                if pyxel.btn(getattr(pyxel,"KEY_"+dic["key"])):
                    pressingAKey = True
        if not pressingAKey:
            holdingKey = False
            keyBeingHeld = None
            heldKeyStartFrame = counter

    return False


        
    
App()
