from utility import *
from rooms import *

PATH = 'finished_rooms.toml'

class App:
    def __init__(self):
        pyxel.init(CAM_WIDTH, CAM_HEIGHT, fps=120)
        pyxel.load('../rooms.pyxres')
        pyxel.colors[2] = get_color('740152')
        pyxel.colors[14] = get_color('C97777')

        self.show = MazeBuild()

        pyxel.mouse(visible=True)

        pyxel.run(self.update,self.draw)

    def update(self):
        self.show.update()

    def draw(self):
        self.show.draw()


        
class MazeBuild:
    def __init__(self):
        self.camera = [0,0]
        self.player = Player(TILE_SIZE,6*TILE_SIZE)
        self.editor = WallsEditor()
        self.roomsRoot = Entry(4,4)
        self.rooms = []
        self.rooms.append(copy(self.roomsRoot))
        self.editWallsMode = False

        self.showWalls = False

        self.margin = 1/4

    def update(self):
        self.cameraUpdate()
        self.player.update()
        self.editorUpdate()

        self.actionsCheck()

    def actionsCheck(self):
        pass

    def editorUpdate(self):
        if pyxel.btnp(pyxel.KEY_LALT):
            self.editWallsMode = not self.editWallsMode
            self.showWalls = not self.showWalls

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.editWallsMode = False
            self.showWalls = False
        
        
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

    def wallsDraw(self):
        global wallsMap
        for y in range(len(wallsMap)):
            for x in range(len(wallsMap[y])):
                if wallsMap[y][x] == 1:
                    pyxel.rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE ,8)

    def roomsDraw(self):
        for room in self.rooms:
            room.draw()

    def loadRoom(self):
        x = (pyxel.mouse_x + self.camera[0])//TILE_SIZE
        y = (pyxel.mouse_y + self.camera[1])//TILE_SIZE

        path = 'finished_rooms.toml'
        file = openToml(path)
        settings = file['presetRooms'][random.randint(0,len(file['presetRooms'])-1)]

        self.rooms.append(LoadRoom(settings,x,y))


class Area:
    def __init__(self, x, y, settings):
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self.assets = []
        self.settings = settings
        self.defaultSettings = {'name':'room_48','width':15*TILE_SIZE,'height':15*TILE_SIZE,
        'walls':[], 'exitsFree':{'up':[],'down':[],'left':[],'right':[]},'assets':[{'name':'tableVertical','relativeX':48,'relativeY':48, 'reversed':False}]}
        self.exit_up = None
        self.exit_left = None
        self.exit_down = None
        self.exit_right = None

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

    def buildWalls(self):
        global wallsMap
        x = self.x//TILE_SIZE
        y = self.y//TILE_SIZE
        for pos in self.walls:
            wallsMap[y + pos[1]][x + pos[0]] = 1

    def __str__(self):
        string = ''
        for attribute in self.__static_attributes__:
            string += str(attribute) + ': ' + str(getattr(self,attribute)) + '\n'
        return string

    def assetAppend(self, assetClass, pos, reversed=False):
        index = 0
        for i in range(len(self.assets)):
            if pos[1] > self.assets[i].y:
                index = i+1

        self.assets.insert(index,assetClass(*pos, reversed))

    def assetDraw(self):
        for asset in self.assets:
            asset.draw()

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



class Entry(Area):
    name = 'room_entry'
    def __init__(self, x, y):
        self.getRoom()
        super().__init__(x, y, self.settings)

    def getRoom(self):
        rooms = openToml(PATH)['presetRooms']
        for room in rooms:
            if room['name'] == self.name:
                self.settings = room
                break
        


if __name__ == '__main__':
    App()
