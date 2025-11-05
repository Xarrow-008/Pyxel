import math, os, random, pyxel
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

    def __str__(self):
        return self.name + str(self.x) + str(self.y)
    
    def update(self):
        if mouse_inside(self.x,self.y,self.width,self.height):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.pressed = True
            else:
                self.pressed = False
    
    def draw(self):
        pyxel.rect(self.x,self.y,self.width,self.height,self.color)

class text_zone:
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


def is_pressed(button_list,name,pos='N/A'):
    for button in button_list:
        if button.pressed and button.name == name:
            if pos == 'N/A':
                return True
            else:
                if pos == (button.x,button.y):
                    return True
    return False

def on_tick(tickrate=60,delay=0): #allows the computer to make operations only on certain times to not do everything 120 times a second
    return (pyxel.frame_count % tickrate)-delay == 0
