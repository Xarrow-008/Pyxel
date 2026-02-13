from utility import *
import toml

TILE_SIZE = 16

WID = 256
HEI = 256 

CAM_WIDTH = TILE_SIZE*20
CAM_HEIGHT = TILE_SIZE*20

FPS = 120


KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}

wallsMap = [[0 for x in range(WID)] for y in range(HEI)]

camera = [0,0]

class App:
    def __init__(self):
        pyxel.init(CAM_WIDTH, CAM_HEIGHT, fps=120)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[1] = get_color('232A4F')
        pyxel.colors[2] = get_color('740152')
        pyxel.colors[14] = get_color('C97777')

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
            if (next_X_1 == 0 or not collision(new_x, self.y, new_X*TILE_SIZE, Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])) and (next_X_2 == 0 or not collision(new_x, self.y, new_X*TILE_SIZE, (Y+1)*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])):
                self.x = new_x
            #Else If the movement puts the entity in the wall, we snap it back to the border to prevent clipping.
            elif (next_X_1 != 0 or next_X_2 != 0) and new_x+self.width>X*TILE_SIZE and (X+1)*TILE_SIZE>new_x:
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
            
            if (next_Y_1 == 0 or not collision(self.x, new_y, X*TILE_SIZE, new_Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])) and (next_Y_2 == 0 or not collision(self.x, new_y, (X+1)*TILE_SIZE, new_Y*TILE_SIZE, [self.width, self.height], [TILE_SIZE, TILE_SIZE])):
                self.y = new_y
            elif (next_Y_1 != 0 or next_Y_2 != 0) and new_y+self.height>Y*TILE_SIZE and (Y+1)*TILE_SIZE>new_y:
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

        self.img = (6,3)

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
            show(self.x,self.y,(10,8), TILE_SIZE=TILE_SIZE)



class Roombuild:
    def __init__(self):
        self.camera = [0,0]
        self.player = Player(WID*16//2,HEI*16//8)
        self.editor = WallsEditor()
        self.rooms = []
        self.exits = []
        self.exitPos = (0,0)
        self.currentExitSide = 'N/A'
        self.roomIndex = -1
        self.editWallsMode = False
        self.editRoomsMode = False
        self.menu = Menu()

        self.initBuild()
        self.anim = Animation([CAM_WIDTH//2-2.5*TILE_SIZE,CAM_HEIGHT//3],{'u':0,'v':4,'width':5*TILE_SIZE,'height':3*TILE_SIZE, 'duration':20}, lifetime='30 cycles')

        self.showWalls = False
        print('[T] then [LSHIFT] + [N] to build a building')

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

        if pyxel.btnp(pyxel.KEY_K):
            self.showWalls = True

        self.player.constructorHat = self.editRoomsMode
        if self.editRoomsMode:
            self.roomsUpdate()

        if self.isBuilding:
            self.buildContinue()
            self.anim.update()
        
        
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

        if not self.isBuilding:
            self.roomsDraw()
            self.exitsDraw()

            if self.showWalls:
                self.wallsDraw()

            self.player.draw()
            self.drawMouse()
        else:
            self.drawAnimation()

    def drawAnimation(self):
        self.anim.draw(*self.camera)

    def drawMouse(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE*TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE*TILE_SIZE
        pyxel.text(x,y-4,str(x)+ ', ' + str(y),15)

    def menuUpdate(self):
        self.menu.update()

        assetNumber = self.menu.assetPlace
        if assetNumber != 'N/A':
            if type(assetNumber) is int and assetNumber <= len(self.menu.assetsList)-1:
                self.assetAdd(self.roomIndex, assetNumber)
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
                if wallsMap[y][x] == 2:
                    pyxel.rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE ,3)

    def roomsUpdate(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.addRoom()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.loadRoom()

        if pyxel.btnp(pyxel.KEY_V):
            self.addShip()

        self.exitsActions()

        if pyxel.btnp(pyxel.KEY_N):
            if pyxel.btn(pyxel.KEY_LSHIFT):
                self.buildStart()
            else:
                self.extendRooms()
        if pyxel.btnp(pyxel.KEY_U):
            print(len(self.rooms))
            if len(self.rooms) != 0:
                print(self.rooms[-1].name)
            


        if len(self.rooms) != 0:
            self.rooms[self.roomIndex].update()

    def addShip(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE

        self.rooms.append(LoadShip(x,y))

    def exitsActions(self):
        global camera
        if pyxel.btnp(pyxel.KEY_F):
            x = (pyxel.mouse_x + camera[0])//TILE_SIZE
            y = (pyxel.mouse_y + camera[1])//TILE_SIZE

            room = self.rooms[self.roomIndex]

            if y == room.y//TILE_SIZE:
                self.currentExitSide = 'up'
            elif x == room.x//TILE_SIZE:
                self.currentExitSide = 'left'
            elif y == (room.y+room.height)//TILE_SIZE-1:
                self.currentExitSide = 'down'
            elif x == (room.x+room.width)//TILE_SIZE-1:
                self.currentExitSide = 'right'

            self.exitPos = [x - room.x//TILE_SIZE, y - room.y//TILE_SIZE]

            if self.currentExitSide != 'N/A':
                self.rooms[self.roomIndex].exitsPos[self.currentExitSide] = copy(self.exitPos)


                   
            self.currentExitSide = 'N/A'

    def roomsDraw(self):
        for room in self.rooms:
            room.draw()

    def exitsDraw(self):
        for exit in self.exits:
            exit.draw()

    def addRoom(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE
        self.rooms.append(NewRoom(x,y,15,15))

    def loadRoom(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE

        path = 'finished_rooms.toml'
        file = openToml(path)
        settings = file['presetRooms'][random.randint(0,len(file['presetRooms'])-1)]

        self.rooms.append(LoadRoom(settings,x,y))
        self.roomIndex += 1

    def savePresets(self):
        path = 'finished_rooms.toml'
        file = openToml(path)
        
        roomDic = self.rooms[self.roomIndex].convertDic()

        """ replace the room if name in file, else append in file"""
        index = None
        for i in range(len(file['presetRooms'])):
            if file['presetRooms'][i]['name'] == roomDic['name']:
                index = i
                print('found', index, roomDic['name'])
        
        if index != None:
            file['presetRooms'].pop(index)
            file['presetRooms'].insert(index,roomDic)
        else:
            file['presetRooms'].append(roomDic)

        
        dumpToml(path,file)

    def extendRooms(self):
        nb_rooms = len(self.rooms)

        for i in range(3):
            self.addNeighbor()
            if nb_rooms != len(self.rooms):
                break

        loops = 0
        while loops < 10:
            
            if nb_rooms == len(self.rooms):
                self.goBack()
                for i in range(3):
                    self.addNeighbor()
                    if nb_rooms != len(self.rooms):
                        break
            if nb_rooms != len(self.rooms):
                break

            loops += 1
            if loops == 10:
                print('gave up')

    def initBuild(self):
        self.isBuilding = False
        self.buildLoops = 0

    def buildStart(self):
        if len(self.rooms) == 0:
            x = self.player.x//TILE_SIZE-1
            y = self.player.y//TILE_SIZE-1

            self.rooms.append(LoadShip(x, y))
            self.nbRooms = 1
            self.isBuilding = True
        else:
            if self.isBuilding:
                self.buildContinue()
            else:
                print('cant build there // rooms already here')

    def buildContinue(self):
        nb_rooms = len(self.rooms)
        for i in range(3):
            self.addNeighbor()
            if nb_rooms != len(self.rooms):
                break
    
    
        if nb_rooms == len(self.rooms):
            if self.buildLoops <= 10:
                self.goBack()
                self.buildLoops += 1
            else:
                self.buildLoops = 0
                self.isBuilding = False
        else:
            self.buildLoops = 0
        
        if self.nbRooms >= 60 or len(self.rooms) >= 60:
            self.isBuilding = False
            print(self.nbRooms, len(self.rooms))



    def goBack(self):
        self.roomIndex = self.rooms[self.roomIndex].previousRoom
            

    def addNeighbor(self):
        room = self.rooms[self.roomIndex]
        side = pickRoomSide(room)

        # --- find a room that has the exit inversed to the one we have ---

        if side != 'N/A':
            nextRoom = findNextRoom(side, room.name)

            roomExitRelativeX = room.exitsPos[side][0]
            roomExitRelativeY = room.exitsPos[side][1]

            exitX = room.x//TILE_SIZE + roomExitRelativeX
            exitY = room.y//TILE_SIZE + roomExitRelativeY


            nextRoomExitX = nextRoom['exitsPos'][sideInverse(side)][0]
            nextRoomExitY = nextRoom['exitsPos'][sideInverse(side)][1]

            x = exitX - nextRoomExitX
            y = exitY - nextRoomExitY

            # --- change if new exits --- 

            if side == 'up':
                y += -5
            if side == 'down':
                y += 5
            if side == 'left':
                x += -5
            if side == 'right':
                x += 5

            entryX = x + nextRoomExitX
            entryY = y + nextRoomExitY

        
            self.rooms[self.roomIndex].exitsFree[side] = False

            if not self.isRoomColliding(x,y,15,13):

                depth = self.rooms[-1].depth + 1

                self.rooms.append(LoadRoom(nextRoom, x, y))

                self.rooms[-1].exitsFree[sideInverse(side)] = False
                self.rooms[-1].previousRoom = self.roomIndex
                self.rooms[-1].index = len(self.rooms)-1
                self.rooms[-1].depth = depth

                self.addDoors(exitX,exitY,entryX,entryY, side)
                
                self.addExit(exitX, exitY, side)

                self.roomIndex = len(self.rooms)-1


    def addDoors(self,exitX,exitY,entryX,entryY,side):
        door1 = findDoor(exitX,exitY, side)
        door2 = findDoor(entryX,entryY, sideInverse(side))

        self.rooms[self.roomIndex].assets.append(door1)
        self.rooms[-1].assets.append(door2)

    def addExit(self, exitX, exitY, side):
        if side == 'up':
            x = exitX
            y = exitY - 4
        if side == 'down':
            x = exitX
            y = exitY + 1
        if side == 'left':
            x = exitX - 4
            y = exitY
        if side == 'right':
            x = exitX + 1
            y = exitY

        if self.rooms[-2].name == 'ship':
            self.exits.append(ExitStairs(x,y))

        elif side == 'up' or side == 'down':
            self.exits.append(ExitBaseVertical(x,y))
        elif side == 'left' or side == 'right':
            self.exits.append(ExitBaseHorizontal(x,y))

        addExitWalls(exitX, exitY, side)
            
    def isRoomColliding(self,x1,y1,w1,h1):
        for room in self.rooms:
            x2 = room.x//TILE_SIZE
            y2 = room.y//TILE_SIZE
            w2 = room.width//TILE_SIZE
            h2 = room.height//TILE_SIZE
            if collision(x1-1,y1-3,x2,y2,(w1+2,h1+7),(w2,h2)):
                return True

        if x1 <= 0 or y1 <= 3 or x1 + w1 + 2 > WID or y1 + h1 + 2 > HEI:
            return True
        
        return False




class Room:
    def __init__(self,x,y,width,height):
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self.width = width*TILE_SIZE
        self.height = height*TILE_SIZE
        self.exitsPos = {'up':[],'down':[],'left':[],'right':[]}
        self.exitsFree = {'up':True,'down':True,'left':True,'right':True}
        self.floorTiles = []

        self.index = 0
        self.previousRoom = 0
        self.depth = 0 #distance to start

        self.isLeaf = False
        self.isBranch = False

    def convertDic(self):
        wallsIn = self.getWallsIn()
        dic = {'name':self.name,'width':self.width,'height':self.height,'walls':wallsIn, 'exitsPos':self.exitsPos,
                'assets':[asset.convertDic((self.x,self.y)) for asset in self.assets]}
        return dic

    def getWallsIn(self):
        global wallsMap
        wallsIn = {'highWalls':[],'lowWalls':[]}
        startX = self.x//TILE_SIZE-1
        startY = self.y//TILE_SIZE-2
        for y in range(self.height//TILE_SIZE+3):
            for x in range(self.width//TILE_SIZE+2):

                if wallsMap[startY + y][startX + x] == 1:
                    wallsIn['lowWalls'].append((x-1, y-2))

                if wallsMap[startY + y][startX + x] == 2:
                    wallsIn['highWalls'].append((x-1, y-2))                

        return wallsIn

    def getFloorTiles(self):
        startX = self.x//TILE_SIZE
        startY = self.y//TILE_SIZE
        for x in range(self.width//TILE_SIZE):
            for y in range(self.height//TILE_SIZE):
                if wallsMap[startY + y][startX + x] == 0:
                    self.floorTiles.append((x,y))

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
        pyxel.rect(self.x,self.y,self.width,self.height+1,2)
        self.floorPatternDraw()
        pyxel.rectb(self.x,self.y,self.width,self.height+1,6)

        self.assetDraw()

    def floorPatternDraw(self):
        pass

    def assetAppend(self, assetClass, pos, reversed=False):
        index = 0
        for i in range(len(self.assets)):
            if pos[1] > self.assets[i].y:
                index = i+1

        self.assets.insert(index,assetClass(*pos, reversed))

    def assetDraw(self):
        for asset in self.assets:
            asset.draw()

    def mouseIn(self):
        global camera
        return mouseInside(self.x,self.y-2*TILE_SIZE,self.width,self.height+2*TILE_SIZE,camera)
         
    def isExitUsable(self,side):
        return self.exitsPos[side] != [] and self.exitsFree[side] and not self.isLeaf



class NewRoom(Room):
    def __init__(self,x,y,width,height):
        super().__init__(x, y, width, height)
        self.loaded = False
        self.name = 'unnamed'

        self.assets = []
        self.assets.append(TableVertical(self.x+16,self.y+16))
        self.assets.append(TableVertical(self.x+64,self.y+16))


class LoadRoom(Room):
    def __init__(self,settings,x,y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.loaded = True
        self.settings = settings
        self.defaultSettings = {'name':'room_48','width':15*TILE_SIZE,'height':15*TILE_SIZE,
        'walls':[], 'exitsPos':{'up':[],'down':[],'left':[],'right':[]},'assets':[{'name':'tableVertical','relativeX':48,'relativeY':48, 'reversed':False}]}
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

                    self.assetAppend(classAsset,(self.x + asset['relativeX'],self.y + asset['relativeY']),asset['reversed'])

        self.buildWalls()
        self.getFloorTiles()

    def buildWalls(self):
        global wallsMap
        x = self.x//TILE_SIZE
        y = self.y//TILE_SIZE



        if type(self.walls) is dict:
            for pos in self.walls['lowWalls']:
                wallsMap[y + pos[1]][x + pos[0]] = 1

            for pos in self.walls['highWalls']:
                wallsMap[y + pos[1]][x + pos[0]] = 2


class LoadShip(LoadRoom):
    def __init__(self,x,y):
        path = '../rooms/finished_rooms.toml'
        file = openToml(path)
        settings = file['presetShip']

        super().__init__(settings,x,y)

        self.name = 'ship'
        
    def draw(self):
        draw(self.x,self.y,2,0,192,self.width,self.height,colkey=11)

        self.assetDraw()




class WallsEditor:
    def __init__(self):
        pass

    def update(self):
        self.editWalls()

    def editWalls(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mousePlaceBlock(1)

        if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            self.mousePlaceBlock(2)
            
        if pyxel.btn(pyxel.KEY_E):
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

class Exit:
    def __init__(self,x,y):
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self.direction = 'N/A'
    def draw(self):
        pyxel.rect(self.x,self.y,2*TILE_SIZE,2*TILE_SIZE,2)
        pyxel.rectb(self.x,self.y,2*TILE_SIZE,2*TILE_SIZE+1,6)

class ExitBaseHorizontal(Exit):
    def __init__(self,x,y):
        super().__init__(x=x,y=y)
        self.direction = 'Horizontal'
    def draw(self):
        pyxel.rect(self.x,self.y,4*TILE_SIZE,2*TILE_SIZE,2)
        pyxel.rectb(self.x,self.y,4*TILE_SIZE,2*TILE_SIZE+1,6)

class ExitBaseVertical(Exit):
    def __init__(self,x,y):
        super().__init__(x=x,y=y)
        self.direction = 'Vertical'
    def draw(self):
        pyxel.rect(self.x,self.y,2*TILE_SIZE,4*TILE_SIZE,2)
        pyxel.rectb(self.x,self.y,2*TILE_SIZE,4*TILE_SIZE+1,6)

class ExitStairs(Exit):
    def __init__(self,x,y):
        super().__init__(x=x,y=y)
        self.direction = 'Vertical'
    def draw(self):
        draw(self.x,self.y,2,208,192,2*TILE_SIZE,1*TILE_SIZE)
        draw(self.x,self.y+TILE_SIZE,2,208,192,2*TILE_SIZE,1*TILE_SIZE)
        draw(self.x,self.y+2*TILE_SIZE,2,208,192,2*TILE_SIZE,1*TILE_SIZE)
        draw(self.x,self.y+3*TILE_SIZE,2,208,192,2*TILE_SIZE,1*TILE_SIZE)



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
        else:
            draw(x=self.pos[0], y=self.pos[1], img=1, u=self.img[0]*self.settings["width"], v=self.img[1]*self.settings["height"], w=self.settings["width"], h=self.settings["height"], colkey=self.colkey)
        
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
    


class Asset:
    name = 'N/A'
    def __init__(self,x,y, reversed=False, interactable=False):
        self.x = x
        self.y = y
        self.img = (0,0)
        self.width = 2*TILE_SIZE
        self.height = 2*TILE_SIZE
        self.reversed = reversed
        self.removeSelf = False
        self.interactable = interactable

        if self.name in ['ClosetFront', 'ClosetBack']:
            if random.randint(0,1) == 0:
                self.interactable = True # TODO remove this paragraph when interactables implemented
                 


    def update(self):
        global camera
        if mouseInside(self.x,self.y,self.width,self.height,camera):
            if pyxel.btnp(pyxel.KEY_X):
                self.removeSelf = True
            if pyxel.btnp(pyxel.KEY_E):
                self.reversed = not self.reversed

    def draw(self):
        if not self.interactable:
            pyxel.pal(7,0)
        
        pyxel.blt(self.x,self.y,2,self.img[0]*TILE_SIZE,self.img[1]*TILE_SIZE,self.width * self.coeff(),self.height,11)
        pyxel.pal()

    def convertDic(self,pos):
        dic = {'name':self.name,'relativeX':self.x-pos[0],'relativeY':self.y-pos[1], 'reversed':self.reversed}
        return dic

    def coeff(self):
        if self.reversed:
            return -1
        else:
            return 1



class DoorHorizontal(Asset):
    name = 'DoorHorizontal'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class DoorVertical(Asset):
    name = 'DoorVertical'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (2,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class TableVertical(Asset):
    name = 'TableVertical'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (6,0)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE

class BedVertical(Asset):
    name = 'BedVertical'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (8,0)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE


class WallHorizontalInside(Asset):
    name = 'WallHorizontalInside'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (10,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class WallHorizontalStart(Asset):
    name = 'WallHorizontalStart'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (11,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE
        
class WallHorizontalEnd(Asset):
    name = 'WallHorizontalEnd'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (12,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE


class WallVerticalInside(Asset):
    name = 'WallVerticalInside'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (13,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class WallVerticalStart(Asset):
    name = 'WallVerticalStart'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (14,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class WallVerticalEnd(Asset):
    name = 'WallVerticalEnd'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (15,0)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class ClosetFront(Asset):
    name = 'ClosetFront'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (6,3)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE

class ClosetBack(Asset):
    name = 'ClosetBack'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (8,3)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE

class Dressing(Asset):
    name = 'Dressing'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (11,3)
        self.width = 3*TILE_SIZE
        self.height = 2*TILE_SIZE

class WallTelevision(Asset):
    name = 'WallTelevision'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (0,3)
        self.width = 2*TILE_SIZE
        self.height = 1*TILE_SIZE

class WallShelf(Asset):
    name = 'WallShelf'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (2,3)
        self.width = 2*TILE_SIZE
        self.height = 1*TILE_SIZE

class CouchFront(Asset):
    name = 'CouchFront'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (0,4)
        self.width = 3*TILE_SIZE
        self.height = 2*TILE_SIZE

class CouchBack(Asset):
    name = 'CouchBack'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (3,4)
        self.width = 3*TILE_SIZE
        self.height = 2*TILE_SIZE

class TableHorizontal(Asset):
    name = 'TableHorizontal'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (0,6)
        self.width = 3*TILE_SIZE
        self.height = 2*TILE_SIZE

class FridgeFront(Asset):
    name = 'FridgeFront'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (0,8)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class ShelfStorage(Asset):
    name = 'ShelfStorage'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (1,8)
        self.width = 1*TILE_SIZE
        self.height = 1*TILE_SIZE

class CounterTopDrawer(Asset):
    name = 'CounterTopDrawer'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (1,9)
        self.width = 1*TILE_SIZE
        self.height = 1*TILE_SIZE

class CounterTop(Asset):
    name = 'CounterTop'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (2,9)
        self.width = 1*TILE_SIZE
        self.height = 1*TILE_SIZE

class CounterTopSide(Asset):
    name = 'CounterTopSide'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (3,9)
        self.width = 1*TILE_SIZE
        self.height = 1*TILE_SIZE

class ChairFront(Asset):
    name = 'ChairFront'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (1,0)
        self.width = 1*TILE_SIZE
        self.height = 1*TILE_SIZE

class ChairBack(Asset):
    name = 'ChairBack'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (1,1)
        self.width = 1*TILE_SIZE
        self.height = 1*TILE_SIZE

class FloorLamp(Asset):
    name = 'FloorLamp'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (4,2)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE
        
class BarrelFront(Asset):
    name = 'BarrelFront'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (0,10)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE
        
class BarrelSide(Asset):
    name = 'BarrelSide'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (1,10)
        self.width = 1*TILE_SIZE
        self.height = 1*TILE_SIZE

class ShipChair(Asset):
    name = 'ShipChair'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (11,5)
        self.width = 1*TILE_SIZE
        self.height = 2*TILE_SIZE

class ShipTrapDoor(Asset):
    name = 'ShipTrapDoor'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (11,7)
        self.width = 2*TILE_SIZE
        self.height = 2*TILE_SIZE
        self.function = ["open/close", {'walls':((0,2),(1,2))}]
        self.interactTime = 1
        self.description = "Opens/closes ship entrance"
        self.coolDown = FPS/2
        self.lastUsed = -self.coolDown
        self.state = 'closed'

    def draw(self):
        if not self.interactable:
            pyxel.pal(7,0)

        if self.state == 'closed':
            stateImg = [0,0]
        else:
            stateImg = [0,32]

        pyxel.blt(self.x,self.y,2, self.img[0]*TILE_SIZE + stateImg[0], self.img[1]*TILE_SIZE + stateImg[1], self.width * self.coeff(),self.height,11)

        pyxel.pal()




class Menu:
    def __init__(self):
        self.allAssets = [DoorHorizontal, DoorVertical, CouchFront, CouchBack, TableVertical, TableHorizontal, 
                        ClosetFront, Dressing, WallTelevision, WallShelf, BedVertical, ClosetBack,
                        WallHorizontalInside,  WallHorizontalStart, WallHorizontalEnd,
                        WallVerticalInside, WallVerticalStart, WallVerticalEnd, BarrelFront, BarrelSide,
                        FridgeFront, ShelfStorage, CounterTop, CounterTopDrawer,CounterTopSide, ChairFront, ChairBack, FloorLamp,
                        ShipTrapDoor, ShipChair]

        self.assetsList = [DoorHorizontal, ChairFront, ChairBack, BarrelFront, BarrelSide, TableVertical, ClosetFront, TableHorizontal, BedVertical, ClosetBack,
                        WallHorizontalInside, FloorLamp, 
                        WallVerticalInside, DoorVertical, WallShelf, ShelfStorage, CounterTopDrawer, CounterTop, CounterTopSide,
                        ShipTrapDoor, ShipChair]

        self.allAssetsNames = [asset.name for asset in self.allAssets]
        self.assetsNames = [asset.name for asset in self.assetsList]
        self.assetPlace = 'N/A'

    def update(self):
        for i in range(9):
            if pyxel.btnp(getattr(pyxel,'KEY_'+str(i+1))):
                if pyxel.btn(pyxel.KEY_LSHIFT):
                    self.assetPlace = i+9
                else:
                    self.assetPlace = i


        if pyxel.btnp(pyxel.KEY_P):
            string = ''
            i=0
            for name in self.assetsNames:
                i += 1
                string += str(i)+': '+ name + ',   '
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
    raise TypeError(str(tab) + str(value))

def get_color(hex):
    return int(hex, 16)

def sideInverse(side):
    if side == 'up':
        return 'down'
    if side == 'down':
        return 'up'
    if side == 'left':
        return 'right'
    if side == 'right':
        return 'left'

def addExitWalls(x, y, side):
    global wallsMap
    if side == 'up':
        wallsMap[y-3][x-1] = 2
        wallsMap[y-3][x+2] = 2
        wallsRect(x,y,2,-5,0)
    if side == 'down':
        wallsMap[y+2][x-1] = 2
        wallsMap[y+2][x+2] = 2
        wallsMap[y+1][x-1] = 2
        wallsMap[y+1][x+2] = 2
        wallsRect(x,y,2,5,0)

    if side == 'left':
        wallsMap[y-1][x-2] = 2
        wallsMap[y-1][x-3] = 2
        wallsMap[y+2][x-2] = 2
        wallsMap[y+2][x-3] = 2
        wallsRect(x,y,-5,2,0)
    if side == 'right':
        wallsMap[y-1][x+2] = 2
        wallsMap[y-1][x+3] = 2
        wallsMap[y+2][x+2] = 2
        wallsMap[y+2][x+3] = 2
        wallsRect(x,y,5,2,0)

def wallsRect(x,y,w,h,wall):
    dW = pyxel.sgn(w)
    dH = pyxel.sgn(h)
    for inY in range(abs(h)):
        for inX in range(abs(w)):
            wallsMap[y+inY*dH][x+inX*dW] = wall #index * direction (neg or pos) + base pos to make rectangle

def pickRoomSide(room):
    sideList = []
    for side in room.exitsPos.keys():
        if room.isExitUsable(side):
            sideList.append(side)

    if len(sideList) != 0:
        side = random.choice(sideList)
    else:
        side = 'N/A'


    return side

def findDoor(x, y, side):
    reverse = False

    if side == 'left' or side == 'right':
        if random.randint(0,1) == 0:
            door = DoorHorizontal
            y += -1
        else:
            door = DoorVertical
            y += 1

        if side == 'right':
            reverse = True



    if side == 'down' or side == 'up':
        x += 2
        y += -1
        if side == 'down':
            door = DoorHorizontal

        if side == 'up':
            door = DoorVertical
        
        if random.randint(0,1) == 0:
            reverse = True
            x += -3
        

    return door(x*TILE_SIZE, y*TILE_SIZE, reverse)

def findNextRoom(side, roomName):
    path = 'finished_rooms.toml'
    file = openToml(path)
    roomsList = file['presetRooms']

    found = False
    while not found:
        nextRoom = random.choice(roomsList)
        for reroll in range(2):              #try to make it less likely to have same room multiple times in a row
            if nextRoom['name'] == roomName:
                nextRoom = random.choice(roomsList)
        
        if nextRoom['exitsPos'][sideInverse(side)] != []:
            found = True
        else:
            roomsList.remove(nextRoom)
    return nextRoom
        
def getRoom(side, newRoomName):
    path = 'finished_rooms.toml'
    file = openToml(path)
    roomsList = file['presetRooms']

    for room in roomsList:
        if room['name'] == newRoomName:
            if side == 'None' or room['exitsPos'][sideInverse(side)] != []:
                return room
    
    print('didnt find room / couldnt fit the exits')
    return findNextRoom(side, newRoomName)



if __name__ == '__main__':
    App()