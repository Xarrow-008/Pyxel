import pyxel,os,math,random
FLOOR = (0,3)
FLOORS = [(3,0),(2,1),(3,1)]
TILE_SIZE = 8

class App:
    def __init__(self):
        pyxel.init(128,128,fps=120)
        pyxel.load('../notAScrap_8by8.pyxres')

        self.animation = Animation()
        self.showing = 'screen'
        self.keyboard = 'zqsd'

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)
    def update(self):
        if self.showing == 'screen':
            self.animation.loop(6,10,32,24,[0,1])
            self.animation.slide_anim(10,3,FLOORS)
        elif self.showing == 'menu':
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

        if on_tick(60):
            print(pyxel.mouse_x,pyxel.mouse_y)
        
        if pyxel.btnp(pyxel.KEY_F):
            if self.showing == 'screen':
                self.showing = 'menu'
            elif self.showing == 'menu':
                self.showing = 'screen'
        
            
    def draw(self):
        if self.showing == 'screen':
            self.draw_ship()
        elif self.showing == 'menu':
            self.draw_menu()
            self.draw_highlight()
        self.draw_test()

    def draw_test(self):
        draw(0,0,0,0,96,16,16,scale=2)

    def draw_ship(self):
        pyxel.cls(0)
        waves = (math.cos(pyxel.frame_count/50)+1)/2
        pyxel.dither(waves/2+0.3125)
        draw_screen(48,0,0,0)
        for i in range(len(self.animation.slide)-1):
            pyxel.blt(
                self.animation.slide_pos + i*8,
                105,
                0,
                self.animation.slide[i][0]*8,
                self.animation.slide[i][1]*8,
                8,
                8
                )
        pyxel.dither(1)
        
        pyxel.blt(40,55,1,32,0,5*TILE_SIZE,3*TILE_SIZE,colkey=11,scale=2)
        pyxel.blt(
            40,95,1,
            self.animation.image1[0],
            self.animation.image1[1],
            40,
            8,
            scale=2,
            colkey=11
        )

    def draw_menu(self):
        pyxel.cls(0)
        draw(0,0,1,112,0,16,16,scale=8)
        pyxel.blt(48,48,1,128,0,32,32,scale=2,colkey=12)
        
    def draw_highlight(self):
        if self.showing == 'menu':
            if self.keyboard == 'arrows':
                pyxel.blt(56,40,1,160,16,16,16,scale=2,colkey=12)
            elif self.keyboard == 'wasd':
                pyxel.blt(40,72,1,160,16,16,16,scale=2,colkey=12)
            elif self.keyboard == 'zqsd':
                pyxel.blt(72,72,1,160,16,16,16,scale=2,colkey=12)

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
        self.slide  = [random.choice(FLOORS) for i in range(18)]
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
        
def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def draw(x, y, img, u, v, w, h, colkey=None, rotate=None, scale=1):
    pyxel.blt(x+w//2*(scale-1), y+h//2*(scale-1), img, u, v, w, h, colkey=colkey, rotate=rotate, scale=scale)

App()