import pyxel,os,math,random
FLOOR = (0,3)
FLOORS = [(3,0),(2,1),(3,1)]
KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':''}
TILE_SIZE = 8

WIDTH = 256
HEIGHT = 256
TILE_SIZE = 8

CAM_WIDTH = 16*8
CAM_HEIGHT = 16*8

FPS = 120

loadedEntities = []

class App:
    def __init__(self):
        pyxel.init(128,128,fps=120)
        pyxel.load('../notAScrap_8by8.pyxres')

        self.button_list = []

        self.player = Player()
        self.screen = Menu(self.button_list)

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.screen.update()
            
        for button in self.button_list:
            button.update()

    def draw(self):
        self.screen.draw()

        for button in self.button_list:
            pyxel.rect(button.x, button.y, button.width, button.height, button.color)

        draw_mouse_pos()


class Button:
    def __init__(self,name,color,x,y,width,height):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pressed = False
    
    def update(self):
        if mouse_inside(self.x,self.y,self.width,self.height):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.pressed = True
            else:
                self.pressed = False

class Player: #Everything relating to the player and its control
    def __init__(self):
        self.keyboard = 'zqsd'
        self.x = 10
        self.y = 10
    def update(self):
        pass
    def draw(self):
        pass


    def movement(self):
        if pyxel.btn(getattr(pyxel,'KEY'+KEYBINDS[self.keyboard][0])):
            self.y += -1
        if pyxel.btn(getattr(pyxel,'KEY'+KEYBINDS[self.keyboard][1])):
            self.x += -1
        if pyxel.btn(getattr(pyxel,'KEY'+KEYBINDS[self.keyboard][2])):
            self.y += 1
        if pyxel.btn(getattr(pyxel,'KEY'+KEYBINDS[self.keyboard][3])):
            self.x += 1

class Animation:
    def __init__(self):
        self.loop_image = (0,0)
        self.slide_blocks  = []
        self.slide_pos = 0
        self.slide_start = [0,0]
    def loop(self,length,duration,u,v,direction):
        if on_tick(duration):
            for i in range(length):
                if pyxel.frame_count % (length*duration) == i*duration:
                    self.loop_image = (u+direction[0]*i*8,v+direction[1]*i*8)

    def slide_random(self,start,length,duration,blocks_list,direction):
        self.slide_direction = direction
        self.slide_start = start
        if len(self.slide_blocks) == 0:
            self.slide_blocks = [random.choice(blocks_list) for i in range(length)]
        if on_tick(duration):
            self.slide_pos += 1
            if self.slide_pos >= 8:
                self.slide_blocks.pop(len(self.slide_blocks)-1)
                self.slide_blocks.insert(0,random.choice(blocks_list))
                self.slide_pos = 0
    
class ChoiceKeys:
    def __init__(self):
        self.keyboard = 'zqsd'
    def update(self):
        if in_perimeter(64,48,pyxel.mouse_x,pyxel.mouse_y,14):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.keyboard = 'arrows'
                print('changed to arrows')
        elif in_perimeter(48,80,pyxel.mouse_x,pyxel.mouse_y,14):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.keyboard = 'wasd'
                print('changed to wasd')

        elif in_perimeter(80,80,pyxel.mouse_x,pyxel.mouse_y,14):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.keyboard = 'zqsd'
                print('changed to zqsd')
    def draw(self):
        pass

class Menu:
    def __init__(self,btn_list):
        self.button_list = btn_list
        self.button_list.append(Button('play',3,3,20,70,10))
        self.button_list.append(Button('keybinds',3,3,35,70,10))
    def update(self):
        pass
    def draw(self):
        pyxel.cls(0)
        #draw(0,0,1,112,0,16,16,scale=8)
        #pyxel.blt(48,48,1,128,0,32,32,scale=2,colkey=12)
        
    def draw_highlight(self):
        if self.showing == 'menu':
            if self.keyboard == 'arrows':
                pyxel.blt(56,40,1,160,16,16,16,scale=2,colkey=12)
            elif self.keyboard == 'wasd':
                pyxel.blt(40,72,1,160,16,16,16,scale=2,colkey=12)
            elif self.keyboard == 'zqsd':
                pyxel.blt(72,72,1,160,16,16,16,scale=2,colkey=12)


def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def draw_mouse_pos():
    pyxel.text(pyxel.mouse_x-8,pyxel.mouse_y-8,str(pyxel.mouse_x)+','+str(pyxel.mouse_y),7)

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

def is_pressed(button_list,name,pos='N/A'):
    for button in button_list:
        if button.pressed and button.name == name:
            if pos == 'N/A':
                return True
            elif pos == (button.x,button.y):
                    return True
    return False

def mouse_inside(x,y,width,height):
    return point_inside(pyxel.mouse_x,pyxel.mouse_y,x,y,width,height)

def point_inside(point_x,point_y,area_x,area_y,width,height):
    return (point_x >= area_x and point_x <= area_x + width) and (
            point_y >= area_y and point_y <= area_y + height
            )

def show(x, y, img, asset, colkey=None, rotate=None, scale=1):
    pyxel.blt(x + 10//2*(scale-1), y + 10//2*(scale-1), img, asset[0]*11, asset[1]*11, 10, 10, colkey=colkey, rotate=rotate, scale=scale)

def icon(x, y, img, asset_name, crossed_condition=False, colkey=5, scale=1):
    show(x, y, img, ASSETS[asset_name],colkey=colkey, scale=scale)
    if crossed_condition:
        show(x, y, img, ASSETS['cross'],colkey=colkey,scale=scale)

def on_tick(tickrate=60,delay=0): #allows the computer to make operations only on certain times to not do averything 120 times a second
    return (pyxel.frame_count % tickrate)-delay == 0

def pos_line(x0,y0,x1,y1): #not exactly bresenham's algorithm because i dont understand it all yet but ill change it when i do
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

def is_within_length(nb,list):
    return nb < len(list)

def draw(x, y, img, u, v, w, h, colkey=None, rotate=None, scale=1):
    pyxel.blt(x+w//2*(scale-1), y+h//2*(scale-1), img, u, v, w, h, colkey=colkey, rotate=rotate, scale=scale)

App()