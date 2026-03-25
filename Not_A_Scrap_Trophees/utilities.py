import math, random, os, pyxel
from copy import deepcopy as copy


class Button:
    def __init__(self,name,color,x,y,width,height,icon=None):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.icon = icon
        self.pressed = False
        self.showName = False

    def __str__(self):
        return self.name + str(self.x) + str(self.y)
    
    def update(self):
        if mouseInside(self.x,self.y,self.width,self.height):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.pressed = True
            else:
                self.pressed = False
    
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

class TextZone:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.text = ''
        self.current_key = ''
        self.enter = False
        self.LETTERS = 'AZERTYUIOPQSDFGHJKLMWXCVBN'
        self.PONCTUATION = [' ', ',', ';', ':', '!', '&', '', '"', "'", '(', '-', '', '_', '', '', ')', '=']
        self.PONC_SHIFT = [' ', '?', '.', '/', '§', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '', '+']
        self.PONC_ALT = [' ', '', '', '', '', '', '', '', "{", '[', '|', '`', '', '', '', ']', '}']
        self.PONC_PYXEL = ['SPACE','COMMA','SEMICOLON','COLON','EXCLAIM','1','2','3','4','5','6','7','8','9','0','RIGHTPAREN','EQUALS']
        self.KEYS = list(self.LETTERS)+self.PONCTUATION

    def update(self):
        self.current_key = ''
        for letter in self.LETTERS:
            if pyxel.btnp(getattr(pyxel,'KEY_'+letter)):
                if pyxel.btn(pyxel.KEY_SHIFT):
                    self.current_key = letter
                else:
                    self.current_key = letter.lower()

        for i in range(len(self.PONC_PYXEL)):
            if pyxel.btnp(getattr(pyxel,'KEY_'+self.PONC_PYXEL[i])):
                if pyxel.btn(pyxel.KEY_SHIFT):
                    self.current_key = self.PONC_SHIFT[i]
                elif pyxel.btn(pyxel.KEY_RALT):
                    self.current_key = self.PONC_ALT[i]
                
                else:
                    self.current_key = self.PONCTUATION[i]
        
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.text = self.text[:-1]
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.enter = True

        if len(self.text) < self.length:
            self.text += self.current_key

    def draw(self):
        pyxel.rect(self.x,self.y,self.length*4 + 1,7,0)
        pyxel.text(self.x+1,self.y+1,self.text,9)

    def draw_over(self):
        pass


def isPressed(button_list,name,pos='N/A'):
    for button in button_list:
        if button.pressed and button.name == name:
            if pos == 'N/A':
                return True
            else:
                if pos == (button.x,button.y):
                    return True
    return False

def onTick(tickrate=60,delay=0): #allows the computer to make operations only on certain times to not do everything 120 times a second / delay ideally not a diviseur of FPS
    return (pyxel.frame_count - delay) % tickrate == 0

def draw(x, y, img, u, v, w, h, colkey=None, rotate=None, scale=1):
    pyxel.blt(x+w//2*(scale-1), y+h//2*(scale-1), img, u, v, w, h, colkey=colkey, rotate=rotate, scale=scale)

def show(x,y,img,colkey=11,save=0, TILE_SIZE=16):
    draw(x,y,save,img[0]*TILE_SIZE,img[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE,colkey=colkey)

def mouseInside(x,y,width,height,cam=(0,0)):
    return pointInside(pyxel.mouse_x+cam[0],pyxel.mouse_y+cam[1],x,y,width,height)

def pointInside(point_x,point_y,area_x,area_y,width,height):
    return (point_x >= area_x and point_x <= area_x + width) and (
            point_y >= area_y and point_y <= area_y + height
            )

def collision(x1, y1, x2, y2, size1, size2): #Checks if object1 and object2 are colliding with each other
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1

def distance(x1,y1,x2,y2): #looks at distance with pythagorean theorem
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def posLine(x0,y0,x1,y1): #not exactly bresenham's algorithm because i dont understand it all yet but ill change it when i do
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
    return positions

__all__ = ['math', 'random', 'os', 'pyxel', 'copy', 'Button', 'TextZone',
           'isPressed', 'onTick', 'draw', 'show', 'mouseInside', 'pointInside', 'collision', 'distance', 'posLine']

