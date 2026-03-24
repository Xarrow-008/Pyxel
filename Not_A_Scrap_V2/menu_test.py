import pyxel,os,math,random, csv, utility
from weapons import*
from items import*
from interactables import*
from furniture import*
from construct import*
from copy import deepcopy as copy

WID = 256
HEI = 256 

CAM_WIDTH = TILE_SIZE*22
CAM_HEIGHT = TILE_SIZE*16

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
        
        self.state = Menu()      

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.state.update()
            
    def draw(self):
        pyxel.cls(0)
        self.state.draw()


class Menu:
    def __init__(self):
        self.buttons = ButtonList()
        self.switch = Switch()

        self.placeButtons()

    def placeButtons(self):
        self.buttons.add(Button('Play',1,10,60,200,30),'play')
        self.buttons.add(Button('Controls',1,10,100,200,30),'controls')
        self.buttons.add(Button('Quit',1,10,140,200,30),'quit')


        for button in self.buttons.list():
            button.showName = True 


    def update(self):

        self.checkActions()

        self.quitGame()

    def draw(self):
        for button in self.buttons.list():
            button.draw()


    def checkActions(self):
        self.checkControls()


    def checkControls(self):
        if self.buttons.controls.pressed():
            self.switch = {}

    def quitGame(self):
        if self.buttons.quit.pressed():
            pyxel.quit()

class Switch:
    ready = False
    to = ''
    arguments = []






class ButtonList:
    attrList = []
    def list(self):
        return [getattr(self,attr) for attr in self.attrList] #self.list -> [button1, button2, button3 ...]

    def add(self, button, name): 
        setattr(self, name, button) #self.name = button
        self.attrList.append(name)




class Button:
    def __init__(self,name,color,x,y,width,height,icon=None):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.icon = icon
        self.showName = False

    def __str__(self):
        return self.name + str(self.x) + str(self.y)
    
    def pressed(self):
        return mouseInside(self.x,self.y,self.width,self.height) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
    
    def draw(self):
        pyxel.rect(self.x,self.y,self.width,self.height,self.color)
        if self.showName:
            size = len(self.name)
            width = self.width-2
            if width > size*4:
                pyxel.text(self.x + 1 + (width - size*4)/2, self.y + 5, self.name, 9)
            else:
                string = self.name
                for i in range(4*size//width+1):
                    pyxel.text(self.x + 1, self.y + 5 + 7*i, string[:width//4], 9)
                    string = string[width//4:]



def getColor(hex):
    return int(hex, 16)

if __name__ == '__main__':
    App()