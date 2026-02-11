from utility import *
from furniture import *
import toml

TILE_SIZE = 16

WID = 256
HEI = 256 

CAM_WIDTH = TILE_SIZE*20
CAM_HEIGHT = TILE_SIZE*20


camera = [0,0]

class Roombuild:
    def __init__(self, playerPos):
        self.camera = [0,0]
        self.rooms = []
        self.exits = []
        self.exitPos = (0,0)
        self.currentExitSide = 'N/A'
        self.roomIndex = 0
        self.playerPos = copy(playerPos)


        self.resetWallsMap()
        self.initBuild()
        self.buildStart()
        self.anim = Animation([CAM_WIDTH//2-2.5*TILE_SIZE,CAM_HEIGHT//3],{'u':0,'v':4,'width':5*TILE_SIZE,'height':3*TILE_SIZE, 'duration':20}, lifetime='30 cycles')

        self.margin = 1/4


    def resetWallsMap(self):
        self.wallsMap = [[0 for x in range(WID)] for y in range(HEI)]


    def update(self):
        self.editorUpdate()


    def editorUpdate(self):
        if self.isBuilding:
            self.buildContinue()
            self.anim.update()
        

        """ #TODO might change
        if len(self.rooms) != 0:
            self.rooms[self.roomIndex].update()
        """

    def addRoom(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE
        self.rooms.append(NewRoom(x,y,15,15))

    def loadRoom(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE

        path = '../rooms/finished_rooms.toml'
        file = openToml(path)
        settings = file['presetRooms'][random.randint(0,len(file['presetRooms'])-1)]

        self.rooms.append(LoadRoom(settings,x,y))
        self.buildWalls()
        self.getFloorTiles()
        self.roomIndex += 1

    def initBuild(self):
        self.isBuilding = False
        self.buildLoops = 0
        self.resetWallsMap()

    def buildStart(self):
        if len(self.rooms) == 0:
            room = findNextRoom('down', "room_TVRoom") #might switch this to a special beginning room
            x = self.playerPos[0]//TILE_SIZE-1
            y = self.playerPos[1]//TILE_SIZE-1

            self.resetWallsMap()

            self.rooms.append(LoadShip(x, y))
            self.buildWalls()
            self.getFloorTiles()
            self.nbRooms = 1
            self.isBuilding = True
        else:
            if self.isBuilding:
                self.buildContinue()

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

                self.rooms.append(LoadRoom(nextRoom, x, y))
                self.buildWalls()
                self.getFloorTiles()
                
                self.rooms[-1].exitsFree[sideInverse(side)] = False
                self.rooms[-1].previousRoom = self.roomIndex
                self.rooms[-1].index = len(self.rooms)-1
                self.rooms[-1].depth = self.rooms[self.roomIndex].depth + 1

                self.addDoors(exitX,exitY,entryX,entryY, side)
                
                self.addExit(exitX, exitY, side)

                self.roomIndex = len(self.rooms)-1

    
    def getFloorTiles(self):
        room = self.rooms[-1]
        floorTiles = []
        startX = room.x//TILE_SIZE
        startY = room.y//TILE_SIZE - 1
        for x in range(room.width//TILE_SIZE):
            for y in range(room.height//TILE_SIZE+1):
                if self.wallsMap[startY + y][startX + x] == 0:
                    floorTiles.append((x,y-1))

        self.rooms[-1].floorTiles = floorTiles

    def buildWalls(self):
        room = self.rooms[-1]
        
        x = room.x//TILE_SIZE
        y = room.y//TILE_SIZE
        for pos in room.walls['lowWalls']:
            self.wallsMap[y + pos[1]][x + pos[0]] = 1

        for pos in room.walls['highWalls']:
            self.wallsMap[y + pos[1]][x + pos[0]] = 2


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

        self.exits[-1].origin = self.roomIndex
        self.exits[-1].destination = len(self.rooms)-1

        self.addExitWalls(exitX, exitY, side)

    
    def addExitWalls(self, x, y, side):
        if side == 'up':
            self.wallsMap[y-3][x-1] = 1
            self.wallsMap[y-3][x+2] = 1
            self.wallsRect(x,y,2,-5,0)
        if side == 'down':
            self.wallsMap[y+2][x-1] = 1
            self.wallsMap[y+2][x+2] = 1
            self.wallsRect(x,y,2,5,0)

        if side == 'left':
            self.wallsMap[y-1][x-2] = 1
            self.wallsMap[y-1][x-3] = 1
            self.wallsMap[y+2][x-2] = 1
            self.wallsMap[y+2][x-3] = 1
            self.wallsRect(x,y,-5,2,0)
        if side == 'right':
            self.wallsMap[y-1][x+2] = 1
            self.wallsMap[y-1][x+3] = 1
            self.wallsMap[y+2][x+2] = 1
            self.wallsMap[y+2][x+3] = 1
            self.wallsRect(x,y,5,2,0)

    
    def wallsRect(self,x,y,w,h,wall):
        dW = pyxel.sgn(w)
        dH = pyxel.sgn(h)
        for inY in range(abs(h)):
            for inX in range(abs(w)):
                self.wallsMap[y+inY*dH][x+inX*dW] = wall #index * direction (neg or pos) + base pos to make rectangle


            
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
        self.hasSpawnedEnemies = False

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
        for y in range(self.height//TILE_SIZE):
            for x in range(self.width//TILE_SIZE):
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
        'walls':{'highWalls':[],'lowWalls':[]}, 'exitsPos':{'up':[],'down':[],'left':[],'right':[]},'assets':[{'name':'tableVertical','relativeX':48,'relativeY':48, 'reversed':False}]}
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


class LoadShip(LoadRoom):
    def __init__(self,x,y):
        path = '../rooms/finished_rooms.toml'
        file = openToml(path)
        settings = file['presetShip']

        super().__init__(settings,x,y)

        self.name = 'ship'
        
    def draw(self):
        draw(self.x,self.y,2,0,192,6*TILE_SIZE,4*TILE_SIZE,colkey=11)

        self.assetDraw()



class Exit:
    def __init__(self,x,y):
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self.width = 1*TILE_SIZE
        self.height = 1*TILE_SIZE

        self.direction = 'N/A'

        self.origin = 0
        self.destination = 0
    def draw(self):
        pyxel.rect(self.x,self.y,self.width,self.height,2)
        pyxel.rectb(self.x,self.y,self.width,self.height+1,6)

class ExitBaseHorizontal(Exit):
    def __init__(self,x,y):
        super().__init__(x=x,y=y)
        self.direction = 'Horizontal'
        self.width = 4*TILE_SIZE
        self.height = 2*TILE_SIZE

class ExitBaseVertical(Exit):
    def __init__(self,x,y):
        super().__init__(x=x,y=y)
        self.direction = 'Vertical'
        self.width = 2*TILE_SIZE
        self.height = 4*TILE_SIZE

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
    
    
def sized_text(x, y, s, col=7, size=6, limit=256, background=False): #Like pyxel.text, but you can modify the size of the text
    x = math.ceil(x)
    y = math.ceil(y)
    if s != "":
        alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        other_characters = ["0","1","2","3","4","5","6","7","8","9",",","?",";",".",":","/","!","'","(",")","[","]","{","}","-","_","°","*","+","%"]

        current_x = x

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
    path = '../rooms/finished_rooms.toml'
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
        

