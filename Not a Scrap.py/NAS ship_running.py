import pyxel,os,math,random
FLOOR = (0,3)
FLOORS = [(3,0),(2,1),(3,1)]


class App:
    def __init__(self):
        pyxel.init(128,128,fps=120)
        pyxel.load('../notAScrap.pyxres')

        self.animation = Animation()

        pyxel.run(self.update,self.draw)
    def update(self):
        self.animation.loop(6,10,32,24,[0,1])
        self.animation.slide_anim(10,3,FLOORS)
    def draw(self):
        pyxel.cls(0)
        waves = (math.cos(pyxel.frame_count/40)+1)/2
        pyxel.dither(waves/2+0.32)
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
        
        pyxel.blt(
            20,95,1,
            self.animation.image1[0],
            self.animation.image1[1],
            16,
            8,
            scale=2
        )


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

App()