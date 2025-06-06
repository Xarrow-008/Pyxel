import pyxel,os,math,random

WIDTH = 32
HEIGHT = 32
TILE_SIZE = 16

class App:
    def __init__(self):
        pyxel.init(128,128,fps=120)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[2] = 5373971
        
        self.world = World()
        self.animation = Animation()
        pyxel.images[1].load(0, 0, "../palette.png")
        self.showing = 'screen'
        self.keyboard = 'zqsd'

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)
    def update(self):
        if pyxel.btnp(pyxel.KEY_A):
            self.world.__init__()
        if pyxel.btn(pyxel.KEY_A) and on_tick(60):
            self.world.__init__()
            
    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                block = self.world.map[y][x]
                draw_block(x*TILE_SIZE,y*TILE_SIZE,0,block)

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

class Animation:
    def __init__(self):
        self.image1 = (0,0)
        self.slide_pos = 0
    def loop(self,length,duration,u,v,direction):
        if on_tick(duration):
            for i in range(length):
                if pyxel.frame_count % (length*duration) == i*duration:
                    self.image1 = (u+direction[0]*i*8,v+direction[1]*i*8)
    def slide_anim(self,length,duration,blocks_list):
        if on_tick(duration):
            self.slide_pos += -1
            if self.slide_pos <= -8:
                self.slide.pop(0)
                self.slide.append(random.choice(blocks_list))
                self.slide_pos = 0

class Blocks:
    WALLS = [(0,0),(1,0),(2,0),(3,0)]
    WALLS_DOWN = [(0,0),(1,0)]
    WALLS_UP = [(2,0),(3,0)]

class World:
    def __init__(self):
        self.map = [[random.choice(Blocks.WALLS) for x in range(WIDTH)] for y in range(HEIGHT)]

def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def draw(x, y, img, u, v, w, h, colkey=None, rotate=None, scale=1):
    pyxel.blt(x+w//2*(scale-1), y+h//2*(scale-1), img, u, v, w, h, colkey=colkey, rotate=rotate, scale=scale)

App()
