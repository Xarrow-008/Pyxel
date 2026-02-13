import pyxel
from lootTables import *
from utility import *

TILE_SIZE = 16
FPS = 120


class Asset:
    name = 'N/A'
    def __init__(self,x,y, reversed=False):
        self.x = x
        self.y = y
        self.img = (0,0)
        self.width = 2*TILE_SIZE
        self.height = 2*TILE_SIZE
        self.reversed = reversed


        self.interactable = False
        self.interactTime = 0
        self.interactProgress = 0
        self.anim = [0,0]
        self.function = []
        self.description = 'N/A'
        self.dropPos = (0,0)
        self.imgUsed = [0,0]
        self.used = False


    def update(self):
        pass

    def draw(self):
        if not self.interactable:
            pyxel.pal(7,0)

        if not self.used:
            pyxel.blt(self.x,self.y,2, self.img[0]*TILE_SIZE + self.anim[0]*self.width, self.img[1]*TILE_SIZE + self.anim[1]*self.height, self.width * self.coeff(),self.height,11)
        else:
            pyxel.blt(self.x,self.y,2, self.imgUsed[0]*TILE_SIZE, self.imgUsed[1]*TILE_SIZE, self.width * self.coeff(),self.height,11)

        pyxel.pal()

    def convertDic(self,pos):
        dic = {'name':self.name,'relativeX':self.x-pos[0],'relativeY':self.y-pos[1], 'reversed':self.reversed}
        return dic

    def coeff(self):
        if self.reversed:
            return -1
        else:
            return 1

    def collision(self,x,y,size):
        return collision(self.x-TILE_SIZE,self.y-TILE_SIZE,x,y,(self.width+2*TILE_SIZE,self.height+2*TILE_SIZE),size)



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
        self.function = ["drop", GENERAL_TABLE]
        self.interactTime = 2*FPS
        self.description = "Contains either fuel, an item, or a weapon"
        self.dropPos = (0,3*TILE_SIZE)
        self.imgUsed = (6,12)

class ClosetBack(Asset):
    name = 'ClosetBack'
    def __init__(self,x,y,reversed=False):
        super().__init__(x,y,reversed=reversed)
        self.img = (8,3)
        self.width = 2*TILE_SIZE
        self.height = 3*TILE_SIZE
        self.function = ["drop", GENERAL_TABLE]
        self.interactTime = 2*FPS
        self.description = "Contains either fuel, an item, or a weapon"
        self.dropPos = (0,-TILE_SIZE)
        self.imgUsed = (8,12)

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
    
    
    def collision(self,x,y,size):
        return collision(self.x,self.y-TILE_SIZE+1,x,y,(self.width,self.height),size)


class Menu:
    def __init__(self):
        self.allAssets = [DoorHorizontal, DoorVertical, CouchFront, CouchBack, TableVertical, TableHorizontal, 
                        ClosetFront, Dressing, WallTelevision, WallShelf, BedVertical, ClosetBack,
                        WallHorizontalInside,  WallHorizontalStart, WallHorizontalEnd,
                        WallVerticalInside, WallVerticalStart, WallVerticalEnd,
                        FridgeFront, ShelfStorage, CounterTop, CounterTopDrawer,CounterTopSide, ChairFront, ChairBack, FloorLamp, BarrelFront, BarrelSide,
                        ShipTrapDoor, ShipChair]

        self.assetsList = [DoorHorizontal, ChairFront, ChairBack, CouchFront, CouchBack, TableVertical, ClosetFront, TableHorizontal, BedVertical, ClosetBack,
                        WallHorizontalInside, FloorLamp, 
                        WallVerticalInside, DoorVertical, WallShelf, FridgeFront, ShelfStorage, CounterTopDrawer, CounterTop, CounterTopSide]

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
