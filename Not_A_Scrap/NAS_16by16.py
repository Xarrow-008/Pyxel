import pyxel,os,math,random,copy

KEYBINDS = {'zqsd':'zqsd', 'wasd':'wasd','arrows':['UP','LEFT','DOWN','RIGHT']}

WIDTH = 32
HEIGHT = 32
TILE_SIZE = 16

class App:
    def __init__(self):
        pyxel.init(128,128,fps=120)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[2] = 5373971
        
        self.player = Player()
        self.world = World()
        self.animation = Animation()
        self.showing = 'screen'
        self.keyboard = 'zqsd'

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.player.update()
            
    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                block = self.world.map[y][x]
                draw_block(x*TILE_SIZE,y*TILE_SIZE,0,block)
        self.player.draw()

class Player: #Everything relating to the player and its control
    def __init__(self):
        self.keyboard = 'zqsd'
        self.x = 10
        self.y = 10

        
        self.image = (6,3)
        self.facing = [1,0]
        self.last_facing = [1,0]

        self.walking = False
        self.step = False
        self.second_step = False
        self.step_frame = 0

    def update(self):
        self.movement()

        self.image_gestion()

        self.last_facing = copy.copy(self.facing)

    def draw(self):
        step_y = self.y
        second_step_y = self.y
        if self.step:
            step_y += -1
        if self.second_step:
            second_step_y += -1


        pyxel.blt(self.x, second_step_y, 0, (self.image[0] + self.facing[0]) * 16, (self.image[1] + self.facing[1] - 2) * 16, 16, 16, 11)
        pyxel.blt(self.x, step_y, 0, (self.image[0] + self.facing[0]) * 16, (self.image[1] + self.facing[1]) * 16, 16, 16, 11)
        pyxel.blt(self.x, second_step_y, 0, (self.image[0] + self.facing[0]) * 16, (self.image[1] + self.facing[1] + 2) * 16, 16, 16, 11)


    def movement(self):
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())):
            self.y += -0.5
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())):
            self.x += -0.5
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper())):
            self.y += 0.5
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())):
            self.x += 0.5
    
    def image_gestion(self):
        self.walking = False
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][0].upper())):
            self.facing = [0,1]
            self.walking = True
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][1].upper())):
            self.facing = [0,0]
            self.walking = True
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][2].upper())):
            self.facing = [1,1]
            self.walking = True
        if pyxel.btn(getattr(pyxel,'KEY_'+KEYBINDS[self.keyboard][3].upper())):
            self.facing = [1,0]
            self.walking = True
        
        if self.walking:
            if on_tick(120):
                self.step = not self.step
                self.step_frame = 0

        if self.second_step != self.step:
            self.step_frame += 1
            if self.step_frame >= 40:
                self.second_step = self.step
                self.step_frame = 0
    

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

    GROUND = [(0,1)]

class World:
    def __init__(self):
        self.map = [[random.choice(Blocks.GROUND) for x in range(WIDTH)] for y in range(HEIGHT)]

def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def draw(x, y, img, u, v, w, h, colkey=None, rotate=None, scale=1):
    pyxel.blt(x+w//2*(scale-1), y+h//2*(scale-1), img, u, v, w, h, colkey=colkey, rotate=rotate, scale=scale)

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

App()
