from utility import *
import toml

TILE_SIZE = 16

WID = 256
HEI = 256 

CAM_WIDTH = TILE_SIZE*14
CAM_HEIGHT = TILE_SIZE*14


KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}

wallsMap = [[0 for x in range(WID)] for y in range(HEI)]

camera = [0,0]

class App:
    def __init__(self):
        pyxel.init(CAM_WIDTH, CAM_HEIGHT, fps=120)
        pyxel.load('../rooms.pyxres')

        self.show = Roombuild()

        pyxel.mouse(visible=True)

        pyxel.run(self.update,self.draw)

    def update(self):
        self.show.update()

    def draw(self):
        self.show.draw()


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
        
        if self.x + self.width > (WID*TILE_SIZE)-1:
            self.x = (WID*TILE_SIZE) - self.width -1
        if self.y + self.height > (HEI*TILE_SIZE) -1:
            self.y = (HEI*TILE_SIZE) - self.height -1


class Player(Entity):
    def __init__(self,x,y):
        super().__init__(x=x, y=y, width=TILE_SIZE, height=TILE_SIZE)

        self.img = (14,1)

        self.keyboard = 'zqsd'
        self.direction = [0,0]
        
        self.initWalk(priority=1,maxSpeed=2,speedChangeRate=20,knockbackCoef=1)

        self.constructorHat = False

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
        if self.constructorHat:
            show(self.x,self.y,(15,1), TILE_SIZE=TILE_SIZE)



class Roombuild:
    def __init__(self):
        self.camera = [0,0]
        self.player = Player(TILE_SIZE,TILE_SIZE)
        self.editor = WallsEditor()
        self.rooms = []
        self.selectedRoom = 0
        self.editWallsMode = False
        self.editRoomsMode = False
        self.menu = Menu()

        self.showWalls = False

        self.margin = 1/4

    def update(self):
        self.cameraUpdate()
        self.player.update()
        self.editorUpdate()
        self.menuUpdate()

        self.actionsCheck()

    def actionsCheck(self):
        if pyxel.btn(pyxel.KEY_LCTRL) and pyxel.btnp(pyxel.KEY_S):
            self.savePresets()

    def savePresets(self):
        path = 'preset_rooms.toml'
        file = openToml(path)
        
        dic = self.rooms[0].convertDic(nbName=0)

        file['presetRooms'].append(dic)
        dumpToml(path,file)

    def editorUpdate(self):
        if pyxel.btnp(pyxel.KEY_LALT):
            self.editWallsMode = not self.editWallsMode
            self.showWalls = not self.showWalls
            self.editRoomsMode = False

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.editWallsMode = False
            self.showWalls = False
            self.editRoomsMode = False

        if pyxel.btnp(pyxel.KEY_T):
            self.editRoomsMode = not self.editRoomsMode
            self.editWallsMode = False
            self.showWalls = False

        self.player.constructorHat = self.editRoomsMode
        if self.editRoomsMode:
            self.roomsUpdate()
        
        
        if self.editWallsMode:
            self.editor.update()

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

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0,0,0,0,0,256,256)

        self.roomsDraw()

        if self.showWalls:
            self.wallsDraw()

        self.player.draw()
        self.drawMouse()

    def drawMouse(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE*TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE*TILE_SIZE
        pyxel.text(x,y-4,str(x)+ ', ' + str(y),15)

    def menuUpdate(self):
        self.menu.update()

        assetNumber = self.menu.assetPlace
        if assetNumber != 'N/A':
            if type(assetNumber) is int and assetNumber <= 9:
                self.assetAdd(self.selectedRoom, assetNumber)
            self.menu.assetPlace = 'N/A'

    def assetAdd(self, room, assetNb):
        if self.rooms[room].mouseIn():
            x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
            y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE
            pos = (x*TILE_SIZE,y*TILE_SIZE)
            newAsset = self.menu.assetsList[assetNb]
            self.rooms[room].assetAppend(newAsset, pos)

    def wallsDraw(self):
        global wallsMap
        for y in range(len(wallsMap)):
            for x in range(len(wallsMap[y])):
                if wallsMap[y][x] == 1:
                    pyxel.rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE ,8)

    def roomsUpdate(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.addRoom()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.loadRoom()

        if len(self.rooms) != 0:
            self.rooms[self.selectedRoom].update()

    def roomsDraw(self):
        for room in self.rooms:
            room.draw()

    def addRoom(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE
        self.rooms.append(NewRoom(x,y,15,15))

    def loadRoom(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE

        path = 'preset_rooms.toml'
        file = openToml(path)
        settings = file['presetRooms'][-1]

        self.rooms.append(LoadRoom(settings,x,y))


class Room:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def convertDic(self,nbName):
        wallsIn = self.getWallsIn()
        dic = {'name':'room_'+str(nbName),'width':self.width,'height':self.height,'walls':wallsIn,'assets':[asset.convertDic((self.x,self.y)) for asset in self.assets]}
        return dic

    def getWallsIn(self):
        global wallsMap
        wallsIn = []
        startX = self.x//TILE_SIZE-1
        startY = self.y//TILE_SIZE-2
        for y in range(self.height//TILE_SIZE+3):
            for x in range(self.width//TILE_SIZE+2):
                if wallsMap[startY + y][startX + x] == 1:
                    wallsIn.append((x-1, y-2))

        return wallsIn




    def __str__(self):
        string = ''
        for attribute in self.__static_attributes__:
            string += str(attribute) + ': ' + str(getattr(self,attribute)) + '\n'
        return string

    def update(self):
        self.assetsUpdate()

    def assetsUpdate(self):
        for asset in self.assets:
            asset.update()

            if asset.removeSelf:
                self.assets.remove(asset)

    def draw(self):
        pyxel.rect(self.x,self.y-2.5*TILE_SIZE,self.width,2.5*TILE_SIZE,5)
        pyxel.rectb(self.x,self.y-2.5*TILE_SIZE,self.width,2.5*TILE_SIZE+1,6)
        pyxel.rect(self.x,self.y,self.width,self.height,2)
        self.floorPatternDraw()
        pyxel.rectb(self.x,self.y,self.width,self.height,6)

        self.assetDraw()

    def floorPatternDraw(self):
        for y in range(self.height//TILE_SIZE):
            for x in range(self.width//TILE_SIZE):
                pass

    def assetAppend(self, assetClass, pos):
        index = 0
        for i in range(len(self.assets)):
            if pos[1] > self.assets[i].y:
                index = i+1

        self.assets.insert(index,assetClass(*pos))

    def assetDraw(self):
        for asset in self.assets:
            asset.draw()

    def mouseIn(self):
        global camera
        return mouseInside(self.x,self.y-2*TILE_SIZE,self.width,self.height+2*TILE_SIZE,camera)
         



class NewRoom(Room):
    def __init__(self,x,y,width,height):
        self.loaded = False
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self.width = width*TILE_SIZE
        self.height = height*TILE_SIZE

        self.assets = []
        self.assets.append(TableVertical(self.x+16,self.y+16))
        self.assets.append(TableVertical(self.x+64,self.y+16))


class LoadRoom(Room):
    def __init__(self,settings,x,y):
        self.loaded = True
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self.settings = settings
        self.defaultSettings = {'name':'room_48','width':15*TILE_SIZE,'height':15*TILE_SIZE,'walls':[],'assets':[{'name':'tableVertical','relativeX':48,'relativeY':48}]}
        self.assets = []

        self.initSettings()

    def initSettings(self):
        for setting in self.defaultSettings.keys():

            if type(self.settings) is dict and setting in self.settings.keys():
                settingValue = copy(self.settings[setting])
            else:
                settingValue = copy(self.defaultSettings[setting])
            

            if setting != 'assets':
                setattr(self,setting,settingValue)
            else:
                menu = Menu()
                for asset in settingValue:
                    classIndex = getIndex(menu.allAssetsNames,asset['name'])
                    classAsset = menu.allAssets[classIndex]

                    self.assetAppend(classAsset,(self.x + asset['relativeX'],self.y + asset['relativeY']))

        self.buildWalls()

    def buildWalls(self):
        global wallsMap
        x = self.x//TILE_SIZE
        y = self.y//TILE_SIZE
        for pos in self.walls:
            wallsMap[y + pos[1]][x + pos[0]] = 1


class WallsEditor:
    def __init__(self):
        pass

    def update(self):
        self.editWalls()

    def editWalls(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mousePlaceBlock(1)

        if pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            self.mousePlaceBlock(0)


    def mousePlaceBlock(self,block):
        global wallsMap, camera
        x = (pyxel.mouse_x + camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + camera[1])//TILE_SIZE
        try:
            wallsMap[y][x] = block
        except:
            pass

    def draw(self):
        pass



class Asset:
    name = 'N/A'
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = (0,0)
        self.width = 2*TILE_SIZE
        self.height = 2*TILE_SIZE
        self.removeSelf = False


    def update(self):
        global camera
        if mouseInside(self.x,self.y,self.width,self.height,camera):
            if pyxel.btnp(pyxel.KEY_X):
                self.removeSelf = True

    def draw(self):
        pyxel.blt(self.x,self.y,1,self.img[0]*TILE_SIZE,self.img[1]*TILE_SIZE,self.width,self.height,11)

    def convertDic(self,pos):
        dic = {'name':self.name,'relativeX':self.x-pos[0],'relativeY':self.y-pos[1]}
        return dic



class DoorHorizontal(Asset):
    name = 'DoorHorizontal'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class DoorVertical(Asset):
    name = 'DoorVertical'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (2,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class TableVertical(Asset):
    name = 'TableVertical'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (6,0)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE

class BedVertical(Asset):
    name = 'BedVertical'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (8,0)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE


class WallHorizontalInside(Asset):
    name = 'WallHorizontalInside'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (10,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class WallHorizontalStart(Asset):
    name = 'WallHorizontalStart'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (11,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE
        
class WallHorizontalEnd(Asset):
    name = 'WallHorizontalEnd'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (12,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE


class WallVerticalInside(Asset):
    name = 'WallVerticalInside'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (13,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class WallVerticalStart(Asset):
    name = 'WallVerticalStart'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (14,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class WallVerticalEnd(Asset):
    name = 'WallVerticalEnd'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (15,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class ClosetFront(Asset):
    name = 'ClosetFront'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (6,3)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE

class ClosetBack(Asset):
    name = 'ClosetBack'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (6,6)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE

class Dressing(Asset):
    name = 'Dressing'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (8,3)
        self.width = 3*TILE_SIZE
        self.height = 2*TILE_SIZE

class WallTelevision(Asset):
    name = 'WallTelevision'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (0,3)
        self.width = 2*TILE_SIZE
        self.height = 1*TILE_SIZE

class WallShelf(Asset):
    name = 'WallShelf'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (2,3)
        self.width = 2*TILE_SIZE
        self.height = 1*TILE_SIZE

class CouchFront(Asset):
    name = 'CouchFront'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (0,4)
        self.width = 3*TILE_SIZE
        self.height = 2*TILE_SIZE

class TableHorizontal(Asset):
    name = 'TableHorizontal'
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = (0,6)
        self.width = 3*TILE_SIZE
        self.height = 2*TILE_SIZE



class Menu:
    def __init__(self):
        self.allAssets = [DoorHorizontal, DoorVertical, CouchFront, TableVertical, TableHorizontal, 
                        ClosetFront, Dressing, WallTelevision, WallShelf, BedVertical, ClosetBack,
                        WallHorizontalInside,  WallHorizontalStart, WallHorizontalEnd,
                        WallVerticalInside, WallVerticalStart, WallVerticalEnd]

        self.assetsList = [DoorHorizontal, CouchFront, TableVertical, ClosetFront, Dressing, WallTelevision, TableHorizontal, BedVertical, ClosetBack,
                        WallHorizontalInside, 
                        WallVerticalInside,]

        self.allAssetsNames = [asset.name for asset in self.allAssets]
        self.assetsNames = [asset.name for asset in self.assetsList]
        self.assetPlace = 'N/A'

    def update(self):
        for i in range(9):
            if pyxel.btnp(getattr(pyxel,'KEY_'+str(i+1))):
                self.assetPlace = i

        if pyxel.btnp(pyxel.KEY_P):
            string = ''
            i=0
            for name in self.assetsNames:
                i += 1
                string += str(i)+': '+name + ',   '
            print(string)

    def draw(self):
        pass


def openToml(path):
    return toml.load(path)

def dumpToml(path, content):
    file = open(path,'w')
    toml.dump(content, file)
    file.close()

def getIndex(tab, value):
    for i in range(len(tab)):
        if tab[i] == value:
            return i
    return None


if __name__ == '__main__':
    App()