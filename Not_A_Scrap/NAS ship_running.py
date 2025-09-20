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
        self.menu = ChoiceKeys()

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)
    def update(self):
        if self.showing == 'screen':
            self.animation.loop(6,10,32,24,[0,1])
            self.animation.slide_random([128,105],18,2,FLOORS,[-1,0])
        elif self.showing == 'menu':
            self.menu.update()
            self.keyboard = self.menu.keyboard
        
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
        self.draw_mouse_pos()

    def draw_test(self):
        draw(0,0,0,0,96,16,16,scale=2)

    def draw_ship(self):
        pyxel.cls(0)
        waves = (math.cos(pyxel.frame_count/50)+1)/2
        pyxel.dither(waves/2+0.3125)
        draw_screen(48,0,0,0)
        for i in range(len(self.animation.slide_blocks)-1):
            pyxel.blt(
                self.animation.slide_start[0] + self.animation.slide_direction[0]*(8*i+self.animation.slide_pos),
                self.animation.slide_start[1] + self.animation.slide_direction[1]*(8*i+self.animation.slide_pos),
                0,
                self.animation.slide_blocks[i][0]*8,
                self.animation.slide_blocks[i][1]*8,
                8,
                8
                )
        pyxel.dither(1)
        
        pyxel.blt(40,55,1,32,0,5*TILE_SIZE,3*TILE_SIZE,colkey=11,scale=2)
        pyxel.blt(
            40,95,1,
            self.animation.loop_image[0],
            self.animation.loop_image[1],
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

    def draw_mouse_pos(self):
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

def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def draw(x, y, img, u, v, w, h, colkey=None, rotate=None, scale=1):
    pyxel.blt(x+w//2*(scale-1), y+h//2*(scale-1), img, u, v, w, h, colkey=colkey, rotate=rotate, scale=scale)

App()