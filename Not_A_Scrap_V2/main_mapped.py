import pyxel,os,math,random, csv
from enemies import*
from weapons import*
from items import*
from interactables import*
from furniture import*
from construct import*
from copy import deepcopy as copy

KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}

WID = 256
HEI = 256 

CAM_WIDTH = TILE_SIZE*20
CAM_HEIGHT = TILE_SIZE*20

wallsMap = [[0 for x in range(WID)] for y in range(HEI)]


TILE_SIZE = 16
FPS = 120

camera = [0,0]

class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(CAM_WIDTH,CAM_HEIGHT,fps=FPS)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[1] = getColor('232A4F')
        pyxel.colors[2] = getColor('740152')
        pyxel.colors[14] = getColor('C97777')
        
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
game_frame = 0

class Game:
    def __init__(self):
        self.playerPos = (512,512)


        self.world = World(self.playerPos)
        self.player = Player(self.playerPos)
        self.camera = [0,0]
        self.margin = 1/4
        
        self.place = inMission(self.player)

    def update(self):
        if self.canPlay():
            self.inGameUpdate()
        
        elif self.player.inInventory:
            self.player.updateInventory()
        

        #Tests for adding weapons
        if keyPress("LEFT_HAND","btn") and pyxel.btn(pyxel.KEY_1):
            self.player.inventory.addWeapon(Weapon.RUSTY_PISTOL, "leftHand",0)
        if keyPress("LEFT_HAND","btn") and pyxel.btn(pyxel.KEY_2):
            self.player.inventory.addWeapon(Weapon.TEST_2_HANDS, "leftHand",0)
        if keyPress("RIGHT_HAND","btn") and pyxel.btn(pyxel.KEY_1):
            self.player.inventory.addWeapon(Weapon.RUSTY_PISTOL, "rightHand",0)
        if keyPress("RIGHT_HAND","btn") and pyxel.btn(pyxel.KEY_2):
            self.player.inventory.addWeapon(Weapon.TEST_2_HANDS, "rightHand",0)

        #Allows the player to switch weapons between backpack and handheld
        if holdKey("LEFT_HAND", 3*FPS, pyxel.frame_count):
            self.player.inventory.switchWeapon("leftHand")
        if holdKey("RIGHT_HAND", 3*FPS, pyxel.frame_count):
            self.player.inventory.switchWeapon("rightHand")

        self.cameraUpdate()
        if self.world.constructor.isBuilding:
            self.world.update()
        

    def cameraUpdate(self):
        global camera
        if self.player.x  < self.camera[0] + CAM_WIDTH * self.margin and self.camera[0] > 0:
            self.camera[0] = self.player.x - CAM_WIDTH * self.margin
        if self.player.x + TILE_SIZE  > self.camera[0] + CAM_WIDTH * (1-self.margin) and self.camera[0] + CAM_WIDTH < WID *TILE_SIZE:
            self.camera[0] = self.player.x + TILE_SIZE - CAM_WIDTH * (1-self.margin)
        if self.player.y  < self.camera[1] + CAM_HEIGHT * self.margin and self.camera[1] > 0:
            self.camera[1] = self.player.y - CAM_HEIGHT * self.margin
        if self.player.y + TILE_SIZE  > self.camera[1] + CAM_HEIGHT * (1-self.margin) and self.camera[1] + CAM_HEIGHT < HEI * TILE_SIZE:
            self.camera[1] = self.player.y + TILE_SIZE - CAM_HEIGHT * (1-self.margin)

        if self.camera[0]<0:
            self.camera[0] = 0
        if self.camera[0] + CAM_WIDTH > WID*TILE_SIZE:
            self.camera[0] = WID*TILE_SIZE - CAM_WIDTH
        if self.camera[1]<0:
            self.camera[1] = 0
        if self.camera[1] - CAM_HEIGHT > HEI*TILE_SIZE:
            self.camera[1] = HEI*TILE_SIZE-CAM_HEIGHT
        
        self.camera = [round(self.camera[0]),round(self.camera[1])]

        pyxel.camera(*self.camera)
        camera = copy(self.camera)


    def inGameUpdate(self):
        global game_frame
        if not self.isFrozen():
            self.place.update()
            game_frame += 1
        else:
            self.place.updateAllEntityAnims()

    def draw(self):
        self.drawGame()

    def isFrozen(self):
        global freeze_start, freeze_duration
        return not timer(freeze_start, freeze_duration, pyxel.frame_count)

    def drawGame(self):
        if self.canPlay():
            self.worldDraw()
            self.place.draw()
        elif self.player.inInventory:
            pyxel.dither(0.25)
            self.worldDraw()
            self.place.draw()
            pyxel.dither(1)
            self.player.drawInventory()
        else:
            self.world.draw()
        
    def worldDraw(self):
        self.world.draw()

    def canPlay(self):
        return not self.player.inInventory and self.world.doneBuilding


class inMission:
    def __init__(self, player):
        self.entities = []
        self.pickups = []
        self.interactables = []
        self.player = player

        self.infoText = ("","","")

    def update(self):

        self.entity_gestion()
        self.interactable_gestion()

        self.player.update()

        self.collisionGestion()

        if pyxel.btnp(pyxel.KEY_M):
            self.entities.append(Enemy(50, 50, EnemyTemplate.DUMMY, 0))
            
        if pyxel.btnp(pyxel.KEY_O):
            self.hurt(5, [0,0], 1, 0, self.player, self.player)

        if pyxel.btnp(pyxel.KEY_P):
            item = random.choice(ITEM_LIST)
            self.pickups.append(Pickup(100,100, item))

        if pyxel.btnp(pyxel.KEY_L):
            self.interactables.append(Interactable(120,120, InteractableTemplate.CHEST))


    def updateAllEntityAnims(self):
        for entity in self.entities:
            entity.updateAnims()

        self.player.updateAnims()


    def entity_gestion(self):
        if self.player.bulletList != []:
                for bullet in self.player.bulletList:
                    self.entities.append(bullet)
                self.player.bulletList = []

        if self.player.reloadedThisFrame:
            for entity in self.entities:
                if distanceObjects(self.player, entity) <= 1.5*TILE_SIZE:
                    self.player.heal += self.player.inventory.healReloadCloseEnemies
                    break
            self.player.reloadedThisFrame = False

        if self.player.heal > 0:
            self.heal(self.player.heal, self.player, self.player)
            self.player.heal = 0
        
        for entity in self.entities:
            
            if hasattr(entity, "bulletList") and entity.bulletList != []:
                for bullet in entity.bulletList:
                    self.entities.append(bullet)
                entity.bulletList = []

            if hasattr(entity, "spawnedPickups") and entity.spawnedPickups != []:
                for pickup in entity.spawnedPickups:
                    self.pickups.append(pickup)
                entity.spawnedPickups = []

            if entity.dead:
                self.entities.remove(entity)
                break

            if hasattr(entity, "reloadedThisFrame") and entity.reloadedThisFrame : 
                if hasattr(entity, "inventory") and distanceObjects(entity, self.player)<=1.5*TILE_SIZE:
                    entity.heal += entity.inventory.healReloadCloseEnemies
                entity.reloadedThisFrame = False

            if entity.heal > 0:
                self.heal(entity.heal, entity, entity)
                entity.heal = 0
            
            entity.update()

    def pickup_gestion(self):
        self.infoText = ("", "", "")
        pickedUpSomething = False
        for pickup in self.pickups:
            if collisionObjects(pickup, self.player):
                self.infoText = (pickup.pickup.name, pickup.pickup.shortDescription, ("Press","pickup"))


        for i in range(1, len(self.pickups)+1):
            pickup = self.pickups[-i]
            if collisionObjects(pickup, self.player) and (not pickedUpSomething) and keyPress("INTERACT","btnp"):
                pickup.pickedUp = True
                pickedUpSomething = True

                if issubclass(type(pickup.pickup), Item):
                    self.player.inventory.addItem(pickup.pickup)

                elif issubclass(type(pickup.pickup), Weapon): 
                    if keyPress("RIGHT_HAND", "btn"):
                        self.player.inventory.addWeapon(pickup.pickup, "rightHand",0)
                    else:
                            self.player.inventory.addWeapon(pickup.pickup, "leftHand",0)

                elif issubclass(type(pickup.pickup), Fuel): 
                    self.player.fuel += pickup.pickup.value

        for pickup in self.pickups:
            if pickup.pickedUp:
                self.pickups.remove(pickup)

    def interactable_gestion(self):
        self.pickup_gestion()

        for interactable in self.interactables:
            if collisionObjects(interactable, self.player) and not interactable.interactedWith:

                self.infoText = (interactable.template["name"], interactable.template["description"], ("Hold","interact"))

                if holdKey("INTERACT", interactable.template["duration"]*(1-self.player.inventory.interactableSpeed/100), game_frame):
                    interactable.interactedWith = True
                    pickup = interactable.template["function"][1].pickRandom(0)
                    pickupObject = Pickup(interactable.x, interactable.y, pickup)
                    if pickup is None:
                        print("Its meant to drop a rare/legendary item, but I haven't actually implemented those yet")
                    else:
                        self.pickups.append(pickupObject)


    def draw(self):
        
        for interactable in self.interactables:
            interactable.draw()

        for pickup in self.pickups:
            if not pickup.pickedUp:
                pickup.draw()

        for entity in self.entities:
            if not entity.dead:
                entity.draw()

        for entity in self.entities:
            if not entity.dead:
                entity.drawOver()
        

        self.player.draw() 
        self.player.drawOver()

        sized_text(x=2, y=239, s=self.infoText[0], col=7, size=6, background=True)
        sized_text(x=2, y=248, s=self.infoText[1], col=7, size=6, background=True)
        if self.infoText != ("", "", ""):
            sized_text(x=self.player.x-29, y=self.player.y-9, s=f"{self.infoText[2][0]} [F] to {self.infoText[2][1]}", col=7, size=6, background=True)


    def heal(self, value, healer, target):
        target.health += value
        if target.health > target.maxHealth:
            target.health = target.maxHealth
        target.addDamageNumber(target, value, 11)

    def hurt(self, value, vector, knockback_coef, shot, damager, target):
        global freeze_start, freeze_duration, game_frame

        damagerIsOwned = (type(damager)==Projectile)

        target.combatStartFrame = game_frame
        target.inCombat = True
        damager.combatStartFrame = game_frame
        damager.inCombat = True

        if damagerIsOwned:
            damager.owner.combatStartFrame = game_frame
            damager.owner.inCombat = True
            value = self.calculateNewDamageValue(value, damager.owner, target)
        else:
            value = self.calculateNewDamageValue(value, damager, target)

        if hasattr(target, "inventory") and target.inventory.ignoreHitChance >= random.randint(1,100):
            target.addIgnoreDamageMarker((damager.x-4, damager.y-4))
            return

        

        if damagerIsOwned :
            crit = damager.owner.inventory.critChance >= random.randint(1,100)
        else :
            crit = hasattr(damager, "inventory") and damager.inventory.critChance >= random.randint(1,100)

        if damagerIsOwned :
            target.lastHitBy = damager.owner
        else:
            target.lastHitBy = damager

        if hasattr(target, "isHitStun"):
            if (not target.isHitStun or target.hitBy == shot) and not target.isInvincible():
                
                if crit:
                    target.sufferDamage(value*2)
                    if damagerIsOwned :
                        damager.owner.addDamageNumber(target, value*2, 8)
                    else:
                        damager.addDamageNumber(target, value*2, 8)
                else:
                    target.sufferDamage(value)
                    if damagerIsOwned :
                        damager.owner.addDamageNumber(target, value, 7)
                    else:
                        damager.addDamageNumber(target, value, 7)

                target.isHitStun = True
                target.hitStunStartFrame = game_frame

                target.invincibilityStartFrame = game_frame

                freeze_start = pyxel.frame_count
                freeze_duration = target.hitFreezeFrame

                target.hitBy = shot
                if hasattr(target, "maxSpeed"):
                    knockback_value = len(str(value))*knockback_coef*target.knockbackCoef
                    target.momentum[0] += vector[0]*knockback_value
                    target.momentum[1] += vector[1]*knockback_value


        else:
            if crit:
                target.sufferDamage(value*2)
                if damagerIsOwned :
                    damager.owner.addDamageNumber(target, value*2, 8)
                else:
                    damager.addDamageNumber(target, value*2, 8)
            else:
                target.sufferDamage(value)
                if damagerIsOwned :
                    damager.owner.addDamageNumber(target, value, 7)
                else:
                    damager.addDamageNumber(target, value, 7)
            if hasattr(target, "maxSpeed"):
                knockback_value = len(str(value))*knockback_coef*target.knockbackCoef
                target.momentum[0] += vector[0]*knockback_value
                target.momentum[1] += vector[1]*knockback_value
                
        target.addAnimationHit((damager.x-4,damager.y-4))

        if target.health <= 0:
            if damagerIsOwned:
                if hasattr(damager.owner, "inventory"):
                    damager.owner.triggerOnKillEffects()
            else:
                if hasattr(damager, "inventory"):
                    damager.triggerOnKillEffects()

    def calculateNewDamageValue(self, value, damager, target):

        if hasattr(damager, "inventory"):
            if (damager.inventory.leftHandLevel < target.level or damager.inventory.leftHand.name == "None") and (damager.inventory.rightHandLevel < target.level or damager.inventory.rightHand.name == "None"): #TODO : Make this also trigger if the enemy is a boss
                value *= 1+(damager.inventory.strongEnemiesDamageBoost)/100
        
        if hasattr(target, "inventory"):

            if target.lowHealth:
                value *= 1-(target.inventory.lowHealthDamageReduction)/100

            value -= target.inventory.flatDamageReduction

        value = int(value)
        if value < 1 : 
            value = 1

        return value

    def collisionGestion(self):
        self.enemy_collision()
        self.player_collision()
        self.enemy_player_collision()

    def enemy_collision(self): #Handles collisions with enemies by entities
        for i in range(len(self.entities)-1): #Entities colliding with enemies
            entity1 = self.entities[i]
            for j in range(i+1, len(self.entities)):
                entity2 = self.entities[j]

                if not ((type(entity1)==Enemy and entity1.health<=0) or (type(entity1)==Projectile and entity1.range<=0) or (type(entity2)==Enemy and entity2.health<=0) or (type(entity2)==Projectile and entity2.range<=0)):

                    if entity1.canCollideWithEnemy() and entity1.collidingWithEnemy(entity2):
                        
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
        return collisionObjects(self.player, entity) and not self.player.isHitStun


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

        self.heal = 0

        self.tempHealth = 0

        self.inCombat = False
        self.combatStartFrame = 0

        self.lowHealth = False

        self.lastHitBy = None

        self.level = 0

    def __str__(self):
        if type(self) == Player:
            return f"Type : Player, x : {self.x}, y : {self.y}, momentum : {self.momentum}, health : {self.health}"
        elif type(self) == Enemy:
            return f"Type : Enemy, x : {self.x}, y : {self.y}, momentum : {self.momentum}, health : {self.health}"
        elif type(self) == Projectile:
            return f"Type : Projectile, x : {self.x}, y : {self.y}, momentum : {self.momentum}, range : {self.range}"

    def update(self):

        self.getConditions()

        self.baseUpdate()

        if self.tempHealth > 0 :
            self.tempHealthDecay()

        if hasattr(self, "inventory") and self.inventory.recalculateStats:
            self.getNewStats()

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

    def baseUpdate(self):
        pass


    def getConditions(self): #Basically just a bunch of booleans used to check whether or not an item's effect has to be triggered

        if self.inCombat and timer(self.combatStartFrame, 5*FPS, game_frame): #The player leaves combat if they haven't received or dealt damage in 5s
            self.inCombat = False

            if hasattr(self, "inventory"):
                self.heal += self.inventory.healLeftCombat
        

        if hasattr(self, "health"):
            statusLastFrame = self.lowHealth
            self.lowHealth = self.health <= int(self.maxHealth)/10 #The player is low health if they are at less than 10% of their max health

            if hasattr(self, "inventory") and  statusLastFrame is (not self.lowHealth): #Triggers if you enter or leave low health status
                self.inventory.recalculateStats = True



    def getNewStats(self):
        self.maxHealth = self.baseHealth + self.inventory.flatMaxHealth

        if hasattr(self, "maxSpeed"):
            if self.lowHealth :
                self.maxSpeed = self.baseSpeed * (1+(self.inventory.moveSpeedBoost)/100) * (1+(self.inventory.lowHealthMoveSpeed)/100)
            else:
                self.maxSpeed = self.baseSpeed * (1+(self.inventory.moveSpeedBoost)/100)

        if hasattr(self, "dashCooldown"):
            self.dashCooldown = self.baseDashCooldown * (1-(self.inventory.dashCooldownReduction)/100)

        self.inventory.critChance = self.inventory.baseCritChance + self.inventory.critChanceIncrease
        if self.inventory.critChance > 50 :
            self.inventory.critChance = 50


    def canDoActions(self):
        return (hasattr(self, "isHitStun") and not self.isHitStun) or not hasattr(self, "isHitStun")


    def tempHealthDecay(self):
        if on_tick(FPS):
            self.tempHealth -= math.ceil(self.tempHealth/10)


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
            next_X_1 = wallsMap[Y][new_X]
            if self.y != Y*TILE_SIZE:
                next_X_2 = wallsMap[Y+1][new_X]
            else:
                next_X_2 = 0
            #If there's enough space for the entity to move, it moves unimpeded
            if (next_X_1 != 1 or not collision(new_x, self.y, new_X*TILE_SIZE, Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])) and (next_X_2 != 1 or not collision(new_x, self.y, new_X*TILE_SIZE, (Y+1)*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])):
                self.x = new_x
            #Else If the movement puts the entity in the wall, we snap it back to the border to prevent clipping.
            elif (next_X_1 == 1 or next_X_2 == 1) and new_x+self.width>X*TILE_SIZE and (X+1)*TILE_SIZE>new_x:
                self.collidedWithWall = True
                self.x = (new_X-pyxel.sgn(vector[0]))*TILE_SIZE
        
        X = int(self.x//TILE_SIZE)

        #We calculate vertical movement in the same way we do horizontal movement

        new_y = self.y + vector[1]
        new_Y = Y+pyxel.sgn(vector[1])
        
        if new_y*pyxel.sgn(vector[1]) > new_Y*TILE_SIZE*pyxel.sgn(vector[1]):
            new_y = new_Y*TILE_SIZE

        
        if vector[1]!=0:
            next_Y_1 = wallsMap[new_Y][X]
            if self.x != X*TILE_SIZE:
                next_Y_2 = wallsMap[new_Y][X+1]
            else:
                next_Y_2 = 0
            
            if (next_Y_1 != 1 or not collision(self.x, new_y, X*TILE_SIZE, new_Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])) and (next_Y_2 != 1 or not collision(self.x, new_y, (X+1)*TILE_SIZE, new_Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])):
                self.y = new_y
            elif (next_Y_1 == 1 or next_Y_2 == 1) and new_y+self.height>Y*TILE_SIZE and (Y+1)*TILE_SIZE>new_y:
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
            if type(self) == Player:
                self.addAnimation(pos=[0,-TILE_SIZE],settings={'u':0,'v':2,'length':10,'duration':self.dashCooldown//5,'colkey':3},lifetime='1 cycle')
            self.isDashing = False
            self.dashStartFrame = game_frame
            self.momentum = [pyxel.sgn(self.dashVector[0])*self.dashSpeed, pyxel.sgn(self.dashVector[1])*self.dashSpeed]
            self.dashVector = [0,0]

    def dashOngoing(self):
        return not timer(self.dashStartFrame, self.dashDuration, game_frame)  


    def initDeath(self, spawnItem, spawnFuel, spawnWeapon):
        self.deathItemSpawn = spawnItem
        self.deathFuelSpawn = spawnFuel
        self.deathWeaponSpawn = spawnWeapon

        self.dead = False


    def initRangedAttack(self, priority):
        self.rangedAttackPriority = priority
        self.shotsFired = 0

        self.bulletList = []

        self.reloadedThisFrame = False

    def rangedAttack(self, hand, x, y):
        if self.canRangedAttack(hand):
            weapon = getattr(self.inventory, hand)

            self.currentActionPriority = self.rangedAttackPriority

            setattr(self.inventory, hand+"StartFrame", game_frame)

            weapon.magAmmo -= 1
            self.shotsFired += 1

            for i in range(weapon.bulletCount):
                horizontal = x - (self.x + self.width/2)
                vertical = y - (self.y + self.height/2)
                norm = math.sqrt(horizontal**2 + vertical**2)

                if norm != 0:
                    cos = horizontal/norm
                    sin = vertical/norm
                    angle = math.acos(cos) * pyxel.sgn(sin)
                    lowest_angle = angle - weapon.spread*(math.pi/180)
                    highest_angle = angle + weapon.spread*(math.pi/180)
                    angle = random.uniform(lowest_angle, highest_angle)
                    cos = math.cos(angle)
                    sin = math.sin(angle)
                else:
                    cos = 0
                    sin = 0

                bullet_shot = Projectile(weapon, self.x, self.y, [cos,sin], self, self.shotsFired)

                self.bulletList.append(bullet_shot)

    def canRangedAttack(self, hand):
        weapon = getattr(self.inventory, hand)
        startFrame = getattr(self.inventory, hand+"StartFrame")
        return self.rangedAttackPriority >= self.currentActionPriority and timer(startFrame, weapon.attackCooldown, game_frame) and weapon.magAmmo>0

    def reloadWeapon(self, hand):
        weapon = getattr(self.inventory, hand)
        if self.canReloadWeapon(hand):
            setattr(self.inventory, hand+"IsReloading", False)
            if weapon.reserveAmmo >= weapon.maxAmmo:
                weapon.magAmmo = weapon.maxAmmo
                weapon.reserveAmmo -= weapon.maxAmmo
            else:
                weapon.magAmmo = weapon.reserveAmmo
                weapon.reserveAmmo = 0
                setattr(self.inventory, hand+"CanNoLongerReload", True)
            self.reloadedThisFrame = True
            

    def canReloadWeapon(self, hand):
        weapon = getattr(self.inventory, hand)
        startFrame = getattr(self.inventory, hand+"StartFrame")
        return timer(startFrame, weapon.reloadTime, game_frame) and weapon.magAmmo==0 and weapon.name != "None"



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
        return type(entity) == Enemy and collisionObjects(self, entity) and ((hasattr(entity, "isHitStun") and not entity.isHitStun) or not hasattr(entity, "isHitStun"))


    def addAnimationHit(self,pos):
        self.addAnimation(pos=[pos[0],pos[1],False],settings={'u':0,'v':1,'length':5},lifetime='1 cycle')

    def addDamageNumber(self, target, value, colour):
        angle = random.uniform(0,2*math.pi)
        x_center = target.x+target.width/2
        y_center = target.y+target.height/2
        self.addAnimation(pos=[x_center+math.cos(angle)*1.5*target.width, y_center+math.sin(angle)*1.5*target.height, False], settings={"width":0, "height":0, "text":(str(value),7,colour,True), "movementVector":[math.cos(angle)*0.1, math.sin(angle)*0.1]}, lifetime=48)

    def addIgnoreDamageMarker(self, pos):
        self.addAnimation(pos=[pos[0], pos[1], False], settings={"width":0, "height":0, "text":("Blocked", 7, 7, True)}, lifetime=24)


    def addAnimation(self,pos=[0,0],settings=0,lifetime='1 cycle'):
        self.anims.append(Animation(pos,settings,lifetime))


    def sufferDamage(self, value):
        if self.tempHealth >= value:
            self.tempHealth -= value
        else:
            value -= self.tempHealth
            self.tempHealth = 0
            self.health -= value


    def initHitstun(self, duration, freezeFrame, invincibility):
        self.hitFreezeFrame = freezeFrame
        self.frozen = 0

        self.hitStunDuration = duration
        self.hitStunStartFrame = 0
        self.isHitStun = False

        self.hitBy = 0

        self.invincibilityDuration = invincibility
        self.invincibilityStartFrame = 0

    def isInvincible(self):
        return not timer(self.invincibilityStartFrame, self.invincibilityDuration, game_frame)

    def hitstun(self):
        if hasattr(self, "isHitStun"):

            if self.isHitStun:
                self.applyVector(self.momentum)
                self.speedDecrease()

            if timer(self.hitStunStartFrame, self.hitStunDuration, game_frame):
                self.isHitStun = False


    def triggerOnKillEffects(self):
        self.tempHealth += self.inventory.onKillTempHealth
        if self.tempHealth > self.maxHealth:
            self.tempHealth = self.maxHealth

        if random.randint(1,100) <= 10:
            if type(self.inventory.leftHand) == MeleeWeapon:
                pass #TODO : Implement this once we implement melee weapons
            else:
                self.inventory.leftHand.reserveAmmo = math.ceil(self.inventory.leftHand.reserveAmmo*(1+self.inventory.ressourceKillEffect/100))
            
            if type(self.inventory.rightHand) == MeleeWeapon:
                pass #TODO : Implement this once we implement melee weapons
            else:
                self.inventory.rightHand.reserveAmmo = math.ceil(self.inventory.rightHand.reserveAmmoffffffffffffffffffff*(1+self.inventory.ressourceKillEffect/100))

class Player(Entity): #Creates an entity that's controlled by the player
    def __init__(self, playerPos):
        super().__init__(x=playerPos[0], y=playerPos[1], width=TILE_SIZE, height=TILE_SIZE)

        self.characterName = "Scrapper"
        self.characterUpside1 = "This character has no upsides"
        self.characterUpside2 = "This character has no upsides"
        self.characterDownside1 = "This character has no downsides"
        self.characterDownside2 = "This character has no downsides"

        self.keyboard = 'zqsd'

        self.health = 80
        self.baseHealth = 80
        self.maxHealth = self.baseHealth

        self.baseSpeed = 0.8
        self.baseDashCooldown = 40

        self.initWalk(priority=0, maxSpeed=self.baseSpeed, speedChangeRate=20, knockbackCoef=1)
        self.initDash(priority=1, cooldown=self.baseDashCooldown, speed=1.5, duration=20)
        self.initRangedAttack(priority=0)
        self.initHitstun(duration=0*FPS, freezeFrame=1*FPS, invincibility=1*FPS)

        self.inventory = Inventory()
        self.inventory.addWeapon(RUSTY_PISTOL(), "leftHand", 0)
        
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

        self.fuel = 0

        self.level = 0 #TODO : Make this increase everytime the player escapes a bunker

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
            pyxel.rect(x=camera[0]+1,y=camera[1]+1,w=42,h=10,col=0)

            health_bar_size = int(40*(self.health/self.maxHealth))

            if self.lowHealth:
                pyxel.dither(0.5)
            pyxel.rect(x=camera[0]+2,y=camera[1]+2,w=health_bar_size,h=8,col=8)
            pyxel.dither(1)

            if self.tempHealth > 0 :
                pyxel.rect(x=camera[0]+1, y=camera[1]+12, w=42, h=10, col=0)
                temp_health_bar_size = int(40*(self.tempHealth/self.maxHealth))
                pyxel.dither(0.5)
                pyxel.rect(x=camera[0]+2, y=camera[1]+13, w=temp_health_bar_size, h=8, col=10)
                pyxel.dither(1)


            sized_text(x=camera[0]+12, y=camera[1]+3, s=str(self.health+self.tempHealth)+"/"+str(self.maxHealth),col=7,size=7)

            #Weapons
            pyxel.rectb(x=camera[0]+CAM_WIDTH-19, y=camera[1]+218, w=18, h=18, col=0)
            pyxel.rect(x=camera[0]+CAM_WIDTH-18, y=camera[1]+219, w=16, h=16, col=13)
            draw(x=camera[0]+CAM_WIDTH-18, y=camera[1]+219, img=0, u=self.inventory.leftHand.image[0], v=self.inventory.leftHand.image[1], w=self.inventory.leftHand.width, h=self.inventory.leftHand.height, colkey=11)
            if type(self.inventory.leftHand) == RangedWeapon:
                sized_text(x=camera[0]+CAM_WIDTH-58, y=camera[1]+224, s=str(self.inventory.leftHand.magAmmo)+"/"+str(self.inventory.leftHand.maxAmmo)+"("+str(self.inventory.leftHand.reserveAmmo)+")", col=7)
            else:
                pass #TODO : melee weapon info


            pyxel.rectb(x=camera[0]+CAM_WIDTH-19, y=camera[1]+237, w=18, h=18, col=0)
            pyxel.rect(x=camera[0]+CAM_WIDTH-18, y=camera[1]+238, w=16, h=16, col=13)
            draw(x=camera[0]+CAM_WIDTH-18, y=camera[1]+238, img=0, u=self.inventory.rightHand.image[0], v=self.inventory.rightHand.image[1], w=self.inventory.rightHand.width, h=self.inventory.rightHand.height, colkey=11)
            if type(self.inventory.rightHand) == RangedWeapon:
                sized_text(x=camera[0]+CAM_WIDTH-58, y=camera[1]+243, s=str(self.inventory.rightHand.magAmmo)+"/"+str(self.inventory.rightHand.maxAmmo)+"("+str(self.inventory.rightHand.reserveAmmo)+")", col=7)
            else:
                pass #TODO : melee weapon info

            #Combat Indicator #(You should probably change how it looks, this mostly for debug purposes so that I can know when the player is or isn't in combat)
            if self.inCombat:
                sized_text(x=camera[0]+50, y=camera[1]+1, s="In Combat", background=True)

            #Fuel
            sized_text(x=camera[0]+CAM_WIDTH-46, y=camera[1]+3, s="Fuel : "+str(self.fuel), col=7, size=7, background=True)

    def baseUpdate(self):
        if keyPress("INVENTORY","btnp"):
            self.inInventory = not self.inInventory

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
        level = getattr(self.inventory, hand+"Level")
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
        draw(x=x+5, y=y+14, img=0, u=weapon.image[0], v=weapon.image[1], w=TILE_SIZE, h=TILE_SIZE, colkey=11)
        if weapon.name != "None":
            sized_text(x=x+25, y=y+18, s=f"{weapon.name} (LVL {level})", col=7) #We'll have to change this part once we add scaling to the weapons
            
            if "backpack" not in hand and getattr(self.inventory, hand+"IsReloading"):
                sized_text(x=x+25, y=y+25, s="Reloading", col=7)
                current_frame = pyxel.frame_count%120
                if current_frame >= 30:
                    pyxel.pset(x=x+61, y=y+29, col=7)
                if current_frame >= 60:
                    pyxel.pset(x=x+65, y=y+29, col=7)
                if current_frame >= 90:
                    pyxel.pset(x=x+69, y=y+29, col=7)



            sized_text(x=x+4, y=y+34, s=f"Damage : {weapon.damage}", col=7)
            sized_text(x=x+4, y=y+41, s=f"Piercing : {weapon.piercing}", col=7)
            sized_text(x=x+4, y=y+48, s=f"Attack speed : {round(FPS/(weapon.attackCooldown),2)} ATK/s", col=7)
            sized_text(x=x+4, y=y+55, s=f"Reload time : {round((weapon.reloadTime)/FPS,2)}s", col=7)
            sized_text(x=x+4, y=y+62, s=f"Ammo : {weapon.magAmmo}/{weapon.maxAmmo} ({weapon.reserveAmmo})", col=7)
            sized_text(x=x+4, y=y+69, s=f"Bullet count : {weapon.bulletCount}", col=7)
            sized_text(x=x+4, y=y+76, s=f"Spread : {weapon.spread}°", col=7)
            sized_text(x=x+4, y=y+83, s=f"Range : {round(weapon.range/TILE_SIZE,2)}T", col=7)
        else:
            sized_text(x=x+25, y=y+18, s=f"{weapon.name}", col=7)

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

        item_x = 12
        item_y = 5
        hoveringOverAnItem = False
        for item in self.inventory.items.items():
            if item[1]>0:
                item_object = getItemFromName(item[0])
                pyxel.rectb(x=x+item_x, y=item_y, w=TILE_SIZE+2, h=TILE_SIZE+2, col=7)
                pyxel.rect(x=x+item_x+1, y=item_y+1, w=TILE_SIZE, h=TILE_SIZE, col=0)
                draw(x=x+item_x+1, y=item_y+1, img=0, u=item_object.image[0], v=item_object.image[1], w=TILE_SIZE, h=TILE_SIZE, colkey=11)
                pyxel.rect(x=x+item_x+18, y=item_y+1, w=13, h=TILE_SIZE, col=0)
                sized_text(x=x+item_x+20, y=item_y+5, s=f"*{item[1]}", col=7)

                if pyxel.mouse_x >= x+item_x and pyxel.mouse_x <= x+item_x+18 and pyxel.mouse_y >= item_y and pyxel.mouse_y <= item_y+18:
                    hoveringOverAnItem = True
                    sized_text(x=x+27, y=202, s=item[0], col=7, limit=x+230)
                    sized_text(x=x+27, y=212, s=item_object.longDescription, col=7, limit=x+230)

                item_x += 32
                if item_x >= 208:
                    item_x = 12
                    item_y += 20
        
        if not hoveringOverAnItem:
            sized_text(x=x+27, y=202, s="Description", col=7, limit=x+230)
            sized_text(x=x+27, y=212, s="Hover over an item to see its description", col=7, limit=x+230)
                


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
        if type(self.inventory.leftHand) == RangedWeapon:

            if keyPress("ATTACK_LEFT", "btn"):
                self.rangedAttack("leftHand", camera[0]+pyxel.mouse_x, camera[1]+pyxel.mouse_y)

            if keyPress("LEFT_HAND","btn") and keyPress("RELOAD","btn") and not self.inventory.leftHandIsReloading and not self.inventory.leftHandCanNoLongerReload:
                self.inventory.leftHand.magAmmo = 0
                self.inventory.leftHandStartFrame = game_frame
                self.inventory.leftHandIsReloading = True

            if self.inventory.leftHand.magAmmo == 0 and not self.inventory.leftHandIsReloading and not self.inventory.leftHandCanNoLongerReload:
                self.inventory.leftHandStartFrame = game_frame
                self.inventory.leftHandIsReloading = True

            self.reloadWeapon("leftHand")

        if type(self.inventory.rightHand) == RangedWeapon:

            if keyPress("ATTACK_RIGHT", "btn"):
                self.rangedAttack("rightHand", pyxel.mouse_x, pyxel.mouse_y)

            if keyPress("RIGHT_HAND","btn") and keyPress("RELOAD","btn") and not self.inventory.rightHandIsReloading and not self.inventory.rightHandCanNoLongerReload:
                self.inventory.rightHand.magAmmo = 0
                self.inventory.rightHandStartFrame = game_frame
                self.inventory.rightHandIsReloading = True

            if self.inventory.rightHand.magAmmo == 0 and not self.inventory.rightHandIsReloading and not self.inventory.rightHandCanNoLongerReload:
                self.inventory.rightHandStartFrame = game_frame
                self.inventory.rightHandIsReloading = True

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
    def __init__(self, x, y, template, level):
        super().__init__(x=x, y=y, width=template["width"], height=template["height"])

        self.originalImage = template["image"]
        self.image = template["image"]

        self.scale = template["scaling"]**level
        self.level = level

        self.health = math.ceil(template["health"]*self.scale)
        self.baseHealth = math.ceil(template["maxHealth"]*self.scale)
        self.maxHealth = math.ceil(template["maxHealth"]*self.scale)

        #We initialise all of the enemies abilities
        for ability in template["abilities"].items():
            
            initialiser = getattr(self, "init"+ability[0])
            parameters = ability[1].values()
            initialiser(*parameters)

            if ability[0] == "Walk":
                self.baseSpeed = ability[1]["maxSpeed"]
            elif ability[0] == "Dash":
                self.baseDashCooldown = ability[1]["cooldown"]


        self.inventory = Inventory()

        self.spawnedPickups = []

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

            if random.randint(1,100) <= self.deathItemSpawn:
                pickup = RARITY_TABLE.pickRandom(0)
                if pickup is not None:
                    self.spawnedPickups.append(Pickup(self.x, self.y, pickup))

            if hasattr(self.lastHitBy, "inventory"):
                if random.randint(1,100) <= self.deathFuelSpawn+self.lastHitBy.inventory.fuelKillChance:
                    pickup = FUEL_TABLE.pickRandom(self.lastHitBy.inventory.extraFuelKillChance)
                    self.spawnedPickups.append(Pickup(self.x, self.y, pickup))
            else:
                if random.randint(1,100) <= self.deathFuelSpawn+self.lastHitBy.inventory.fuelKillChancce:
                    pickup = FUEL_TABLE.pickRandom(0)
                    self.spawnedPickups.append(Pickup(self.x, self.y, pickup))

            if random.randint(1,100) <= self.deathWeaponSpawn:
                pickup = WEAPON_TABLE.pickRandom(0)
                self.spawnedPickups.append(Pickup(self.x, self.y, pickup))

            

            


class Inventory:
    def __init__(self):
        self.leftHand = NO_WEAPON().copy()
        self.leftHandOccupied = False
        self.leftHandStartFrame = 0
        self.leftHandIsReloading = False
        self.leftHandCanNoLongerReload = False
        self.leftHandLevel = 0

        self.rightHand = NO_WEAPON().copy()
        self.rightHandOccupied = False
        self.rightHandStartFrame = 0
        self.rightHandIsReloading = False
        self.rightHandCanNoLongerReload = False
        self.rightHandLevel = 0

        self.backpack1 = NO_WEAPON().copy()
        self.backpack1Occupied = False
        self.backpack1Level = 0

        self.canHaveTwoWeaponsInBackPack = True

        self.backpack2 = NO_WEAPON().copy()
        self.backpack2Occupied = False
        self.backpack2Level = 0

        self.baseCritChance = 5
        self.critChance = 5

        self.recalculateStats = False

        self.items = {}
        for item in ITEM_LIST:
            self.items[item.name] = 0
            for effect in item.effects:
                setattr(self, effect["stat"], 0)


    def addWeapon(self, weapon, hand, level): #Function used when the player picks up a weapon

        damage = math.ceil(weapon.damage*(weapon.scaling**level))
        new_weapon = weapon.copy()
        new_weapon.damage = damage

        setattr(self, hand, new_weapon.copy())
        setattr(self, hand+"Level", level)


        #We can almost definitely make this more efficient but this works and is understandable

        if not self.canHaveTwoWeaponsInBackPack:

            if self.backpack1.handNumber==1:

                setattr(self, hand+"Occupied", False)

                #We check wether or not its a two handed weapon to block off the other hand
                if weapon.handNumber==1:
                    setattr(self, self.oppositeHand(hand)+"Occupied", False)
                    if getattr(self, self.oppositeHand(hand)).handNumber==2:
                        setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                        setattr(self, self.oppositeHand(hand)+"Level", 0)

                elif weapon.handNumber==2:
                    setattr(self, self.oppositeHand(hand)+"Occupied", True)
                    setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                    setattr(self, self.oppositeHand(hand)+"Level", 0)

            elif self.backpack1.handNumber==2:

                if getattr(self, hand+"Occupied"):
                    self.backpack1 = NO_WEAPON().copy()
                    self.backpack1Level = 0
                    setattr(self, hand+"Occupied", False)

                    if weapon.handNumber==2:
                        setattr(self, self.oppositeHand(hand)+"Occupied", True)
                        setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                        setattr(self, self.oppositeHand(hand)+"Level", 0)

                else:
                    setattr(self, hand+"Occupied", False)
                    if weapon.handNumber==2:
                        setattr(self, self.oppositeHand(hand)+"Occupied", True)
                        setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                        setattr(self, self.oppositeHand(hand)+"Level", 0)
                        self.backpack1 = NO_WEAPON().copy()
                        self.backpack1Level = 0

        else:
            setattr(self, hand+"Occupied", False)
            #We check wether or not its a two handed weapon to block off the other hand
            if weapon.handNumber==1:
                setattr(self, self.oppositeHand(hand)+"Occupied", False)
                if getattr(self, self.oppositeHand(hand)).handNumber==2:
                    setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                    setattr(self, self.oppositeHand(hand)+"Level", 0)

            elif weapon.handNumber==2:
                setattr(self, self.oppositeHand(hand)+"Occupied", True)
                setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                setattr(self, self.oppositeHand(hand)+"Level", 0)

    def switchWeapon(self, hand): #Function used to switch hand-held weapons with ones stored in the backpack
        
        #This is also ugly, but its the best I'm gonna do right now

        if not self.canHaveTwoWeaponsInBackPack:

            if self.backpack1.handNumber==1:

                setattr(self, hand+"Occupied", False)
                
                if self.leftHand.handNumber==2:
                    weapon = self.leftHand
                    level = self.leftHandLevel
                    setattr(self, hand, self.backpack1)
                    setattr(self, hand+"Level", self.backpack1Level)
                    self.backpack1 = weapon
                    self.backpack1Level = level
                    

                    setattr(self, self.oppositeHand(hand)+"Occupied", True)
                    setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                    setattr(self, self.oppositeHand(hand)+"Level", 0)

                elif self.rightHand.handNumber==2:
                    weapon = self.rightHand
                    level = self.rightHandLevel
                    setattr(self, hand, self.backpack1)
                    setattr(self, hand+"Level", self.backpack1Level)
                    self.backpack1 = weapon
                    self.backpack1Level = level

                    setattr(self, self.oppositeHand(hand)+"Occupied", True)
                    setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                    setattr(self, self.oppositeHand(hand)+"Level", 0)

                else:
                    weapon = getattr(self, hand)
                    level = getattr(self, hand+"Level")
                    setattr(self, hand, self.backpack1)
                    setattr(self, hand+"Level", self.backpack1Level)
                    self.backpack1 = weapon
                    self.backpack1Level = level

            else:
                if getattr(self, hand+"Occupied"):
                    setattr(self, hand+"Occupied", False)

                    setattr(self, hand, self.backpack1)
                    setattr(self, hand+"Level", self.backpack1Level)
                    self.backpack1 = getattr(self, self.oppositeHand(hand))
                    self.backpack1Level = getattr(self, self.oppositeHand(hand)+"Level")

                    setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                    setattr(self, self.oppositeHand(hand)+"Occupied", True)
                    setattr(self, self.oppositeHand(hand)+"Level", 0)

                else:
                    weapon = getattr(self, hand)
                    level = getattr(self, hand+"Level")
                    setattr(self, hand, self.backpack1)
                    setattr(self, hand+"Level", self.backpack1Level)
                    self.backpack1 = weapon
                    self.backpack1Level = level

        else:
            
            if self.backpack1.handNumber==2:
                weapon = self.backpack1
                level = self.backpack1Level
                

                setattr(self, self.equivalentHand(hand), getattr(self, hand))
                setattr(sefl, self.equivalentHand(hand)+"Level", getattr(self, hand)+"Level")
                setattr(self, self.equivalentHand(self.oppositeHand(hand)), getattr(self, self.oppositeHand(hand)))
                setattr(self, self.equivalentHand(self.oppositeHand(hand))+"Level", getattr(self, self.oppositeHand(hand))+"Level")

                setattr(self, hand, weapon)
                setattr(self, hand, level)

                setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                setattr(self, self.oppositeHand(hand)+"Level", 0)
                setattr(self, hand+"Occupied", False)
                setattr(self, self.oppositeHand(hand)+"Occupied", True)

                if self.backpack1.handNumber==2:
                    self.backpack2Occupied = True
                else:
                    self.backpack2Occupied = False
                if self.backpack2.handNumber==2:
                    self.backpack1Occupied = True
                else:
                    self.backpack1Occupied = False

            elif self.backpack2.handNumber==2:
                weapon = self.backpack2
                level = self.backpack2Level
                
                setattr(self, self.equivalentHand(hand), getattr(self, hand))
                setattr(self, self.equivalenntHand(hand)+"Level", getattr(self, hand+"Level"))
                setattr(self, self.equivalentHand(self.oppositeHand(hand)), getattr(self, self.oppositeHand(hand)))
                setattr(self, self.equivalentHand(self.oppositeHand(hand)+"Level"), getattr(self, self.oppositeHand(hand)+"Level"))
                setattr(self, hand, weapon)
                setattr(self, hand, level)

                setattr(self, self.oppositeHand(hand), NO_WEAPON().copy())
                setattr(self, self.oppositeHand(hand)+"Level", 0)
                setattr(self, hand+"Occupied", False)
                setattr(self, self.oppositeHand(hand)+"Occupied", True)

                if self.backpack1.handNumber==2:
                    self.backpack2Occupied = True
                else:
                    self.backpack2Occupied = False
                if self.backpack2.handNumber==2:
                    self.backpack1Occupied = True
                else:
                    self.backpack1Occupied = False
            else:
                weapon1 = self.backpack1
                level1 = self.backpack1Level
                weapon2 = self.backpack2
                level2 = self.backpack2Level

                setattr(self, self.equivalentHand(hand), getattr(self, hand))
                setattr(self, self.equivalentHand(hand)+"Level", getattr(self, hand+"Level"))
                setattr(self, self.equivalentHand(self.oppositeHand(hand)), getattr(self, self.oppositeHand(hand)))
                setattr(self, self.equivalentHand(self.oppositeHand(hand))+"Level", getattr(self, self.oppositeHand(hand)+"Level"))

                setattr(self, hand, weapon1)
                setattr(self, hand, level1)
                setattr(self, self.oppositeHand(hand), weapon2)
                setattr(self, self.oppositeHand(hand), level2)

                self.leftHandOccupied = False
                self.rightHandOccupied = False

                if self.backpack1.handNumber==2:
                    self.backpack2Occupied = True
                else:
                    self.backpack2Occupied = False
                if self.backpack2.handNumber==2:
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


    def addItem(self, item):
        self.items[item.name]+=1

        for effect in item.effects:

            if effect["scaling"]=="constant":
                setattr(self, effect["stat"], effect["value"])

            elif effect["scaling"]=="arithmetic":
                setattr(self, effect["stat"], effect["initial_term"]+(self.items[item.name]-1)*effect["reason"])

            elif effect["scaling"]=="geometric":
                setattr(self, effect["stat"], effect["initial_term"]*(1-effect["reason"]**(self.items[item.name]))/(1-effect["reason"]))

            print(effect["stat"], getattr(self, effect["stat"]))
        
        self.recalculateStats = True



class Projectile(Entity) : #Creates a projectile that can hit other entitiesz
    def __init__(self, weapon, x, y, vector, owner, shot):
        super().__init__(x=x, y=y, width=weapon.bulletWidth, height=weapon.bulletHeight)

        self.momentum = vector

        self.image = weapon.bulletImage

        
        if owner is Enemy:
            self.baseDamage = weapon.damage*owner.scale
            self.damage = weapon.damage*owner.scale
        else:
            self.baseDamage = weapon.damage
            self.damage = weapon.damage

        self.piercing = weapon.piercing

        self.baseRange = weapon.range
        self.range = weapon.range

        self.fallOffCoef = weapon.fallOffCoef
        self.noFallOffArea = weapon.noFallOffArea

        self.owner = owner

        self.shot = shot

        if hasattr(owner, "inventory"):
            self.damageKnockbackCoef = weapon.knockbackCoef*(1+owner.inventory.rangedKnockback/100)
        else:
            self.damageKnockbackCoef = weapon.knockbackCoef

        self.initWalk(priority=0, maxSpeed=weapon.bulletSpeed, speedChangeRate=0, knockbackCoef=0)
        self.initDeath(spawnItem=0, spawnWeapon=0, spawnFuel=0)
        self.initialiseNewCollisions()
        

    def draw(self):
        draw(self.x, self.y, 0, self.image[0], self.image[1], self.width, self.height, colkey=11)

    def movement(self):
        self.walk([self.momentum[0]*self.maxSpeed, self.momentum[1]*self.maxSpeed])
        self.range -= math.sqrt((self.momentum[0]*self.maxSpeed)**2 + (self.momentum[1]*self.maxSpeed)**2)

        if self.range != 0 and self.range < (self.baseRange*self.noFallOffArea):
            if self.fallOffCoef >= 0 :
                self.damage = self.baseDamage*self.fallOffCoef*(self.range/(self.baseRange*self.noFallOffArea))
            else:
                self.damage = -self.baseDamage*self.fallOffCoef*(2 - self.range/(self.baseRange*self.noFallOffArea))
            self.initialiseNewCollisions()


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

    def initialiseNewCollisions(self):
        if type(self.owner)==Player:
            self.initCollision([0, 0, 0, 0], [self.damage, self.momentum, self.damageKnockbackCoef, self.piercing], [0, 0, 0, -1])
        elif type(self.owner)==Enemy:
            self.initCollision([0, 0, 0, 0], [0, 0, 0, -1], [self.damage, self.momentum, self.damageKnockbackCoef, self.piercing])

class Pickup:
    def __init__(self, x, y, pickup):
        self.x = x
        self.y = y

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.pickup = pickup

        self.pickedUp = False

    def draw(self):
        draw(x=self.x, y=self.y, img=0, u=self.pickup.image[0], v=self.pickup.image[1], w=self.width, h=self.height, colkey=11)

class Interactable:
    def __init__(self, x, y, template):
        self.x = x
        self.y = y

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.template = template

        self.interactedWith = False

    def draw(self):
        if self.interactedWith :
            pyxel.rect(x=self.x, y=self.y, w=self.width, h=self.height, col=0)
        else:
            draw(x=self.x, y=self.y, img=0, u=self.template["image"][0], v=self.template["image"][1], w=self.width, h=self.height, colkey=11)


class Blocks:
    WALLS = [(0,0),(1,0),(2,0),(3,0)]
    WALLS_DOWN = [(0,0),(1,0)]
    WALLS_UP = [(2,0),(3,0)]

    GROUND = [(0,1)]


class World:
    def __init__(self, playerPos):
        global wallsMap

        self.rooms = []
        self.exits = []
        self.showWalls = False
        self.constructor = Roombuild(playerPos)
        self.doneBuilding = False

        self.initBuild()

    def update(self):
        self.constructor.update()
        if not self.constructor.isBuilding and not self.doneBuilding:
            global wallsMap
            self.rooms = self.constructor.rooms
            self.exits = self.constructor.exits
            self.doneBuilding = True
            wallsMap = copy(self.constructor.wallsMap)
      
    def initBuild(self):
        self.isBuilding = False
        self.buildLoops = 0

    def draw(self):
        self.drawMap()
        if self.constructor.isBuilding:
            self.constructor.anim.draw(*camera)
    
    def drawMap(self):
        for room in self.rooms:
            room.draw()
            
        for exit in self.exits:
            exit.draw()

        


class Animation:
    def __init__(self,pos,settings,lifetime):
        self.start = pyxel.frame_count
        self.settings = settings
        self.lifetime = lifetime
        self.pos = pos
        self.posRelative = True
        self.colkey = 11
        self.default_set = {'u':0,'v':0,'width':TILE_SIZE,'height':TILE_SIZE,'imageVector':(1,0), 'text':('',6,7,False), 'length':3,'duration':10, 'colkey':11, 'movementVector':(0,0)}

        self.apply_settings()


        self.img = (self.settings['u'],self.settings['v'])
        self.kill = False

    def update(self):
        if not self.is_dead():
            self.get_img()
            self.pos[0] += self.settings["movementVector"][0]
            self.pos[1] += self.settings["movementVector"][1]
            
    def draw(self,x,y):
        if self.posRelative:
            draw(x=x + self.pos[0], y=y + self.pos[1], img=1, u=self.img[0]*self.settings["width"], v=self.img[1]*self.settings["height"], w=self.settings["width"], h=self.settings["height"], colkey=self.colkey)
            sized_text(x + self.pos[0], y + self.pos[1], self.settings["text"][0], size=self.settings["text"][1], col=self.settings["text"][2], background=self.settings["text"][3])
        else:
            draw(x=self.pos[0], y=self.pos[1], img=1, u=self.img[0]*self.settings["width"], v=self.img[1]*self.settings["height"], w=self.settings["width"], h=self.settings["height"], colkey=self.colkey)
            sized_text(self.pos[0], self.pos[1], self.settings["text"][0], size=self.settings["text"][1], col=self.settings["text"][2], background=self.settings["text"][3])
        
    def get_img(self):
        frame_anim = (self.frame() // self.settings['duration']) % self.settings['length']
        x = self.settings['u'] + self.settings['imageVector'][0]*frame_anim
        y = self.settings['v'] + self.settings['imageVector'][1]*frame_anim
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
            self.pos = [self.pos[0],self.pos[1]]

        self.colkey = self.settings['colkey']


    def is_dead(self):
        if self.lifetime == 1000:
            print(self.start, pyxel.frame_count)

        return pyxel.frame_count > self.start + self.lifetime or self.kill

    def frame(self):
        return pyxel.frame_count - self.start
      

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def distanceObjects(object1, object2):
    return math.sqrt((object1.x+object1.width - object2.x-object2.width)**2 + (object1.y+object1.height - object2.y-object2.height)**2)

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

def collisionObjects(object1, object2):
    return object1.x+object1.width>object2.x and object2.x+object2.width>object1.x and object1.y+object1.height>object2.y and object2.y+object2.height>object1.y

def show(x,y,img,colkey=11,save=0):
    pyxel.blt(x,y,save,img[0]*16,img[1]*16,16,16,colkey=colkey)

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

def sized_text(x, y, s, col=7, size=6, limit=CAM_WIDTH, background=False): #Like pyxel.text, but you can modify the size of the text
    x = math.ceil(x)
    y = math.ceil(y)
    if s != "":
        alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        other_characters = ["0","1","2","3","4","5","6","7","8","9",",","?",";",".",":","/","!","'","(",")","[","]","{","}","-","_","°","*","+","%"]

        current_x = x
        limit += camera[0]

        scale = size/6

        for i in range(len(s)):
            chr = s[i]

            if chr == "":
                break

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

            if chr == " " and background:
                pyxel.rect(x=current_x-1, y=y-1, w=int(5*scale), h=int(8*scale), col=0)

            if chr != " ":
                if background :
                    pyxel.rect(x=current_x-1, y=y-1, w=int(5*scale), h=int(8*scale), col=0)
                pyxel.pal(0,col)
                draw(current_x, y, 0, u, v, w, h, scale=scale, colkey=11)
                pyxel.pal()

            if not(chr==" " and current_x==x):
                current_x += int(4*scale)

            if current_x + 2*int(4*scale) >= limit: #Make the text wrap around if it goes past the limit
                if chr != " " and not (i<len(s)-1 and s[i+1]==" "):
                    if background :
                        pyxel.rect(x=current_x-1, y=y-1, w=int(5*scale), h=int(8*scale), col=0)
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

def getItemFromName(name):
    for item in ITEM_LIST:
        if item.name==name:
            return item


def getColor(hex):
    return int(hex, 16)
    
App()
