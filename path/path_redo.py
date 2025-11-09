import sys

from utility.py import *

WID = 256
HEI = 256
TILE_SIZE = 16

FPS = 120

map = [[0 for x in range(HEI//TILE_SIZE)] for y in range(WID//TILE_SIZE)]


class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(WID,HEI,fps=FPS)
        pyxel.load('pather.pyxres')
        pyxel.colors[2] = 5373971
        
        self.empty_space()

        self.controller = Controller()
        self.mapper = Mapper()

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.update_map()
        self.update_entities()

    
    def draw(self):
        pyxel.cls(0)
        self.draw_map()
        self.draw_entities()

    def update_map(self):
        self.mapper.update()
        if self.mapper.needs_re_init:
            self.mapper.needs_re_init = False
            self.controller.reinitialize()

    def update_entities(self):
        if self.mapper.can_run():
            self.controller.update()

    def draw_map(self):
        self.mapper.draw()

    def draw_entities(self):
        self.controller.draw()
    


class Mapper:
    def __init__(self):
        global map
        self.needs_re_init = False

    def update(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mouse_place_block(7)

        if pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            self.mouse_place_block(0)

    def mouse_place_block(self,block):
        x = pyxel.mouse_x//TILE_SIZE
        y = pyxel.mouse_y//TILE_SIZE
        try:
            map[y][x] = block
        except:
            pass
        self.needs_re_init = True

    def draw(self):
        self.draw_walls()

    def draw_walls(self):
        for y in range(len(map)):
            for x in range(len(map[y])):
                color = self.map[y][x]
                pyxel.rect(x*10,y*10,10,10,color)

    def can_run(self):
        return not (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT))


        
class Controller:
    def __init__(self):
        self.hider = Hider()
        self.pather = Pather()

    def update(self):
        self.pather.update(self.hider.x,self.hider.y)
        self.check_interactions()
        self.hider.update()


    def draw(self):
        self.pather.draw()
        self.hider.draw()

    def check_interactions(self):
        if self.hider.stun_around:
            self.hider.stun_around = False
            if distance(self.hider.x,self.hider.y,self.pather.x,self.pather.y) < 20:
                self.pather.stun(120)
    
    def reinitialize(self):
        self.pather.__init__()
        self.hider.__init__()
        

    
class Pather:
    def __init__(self):
        self.x = TILE_SIZE
        self.y = TILE_SIZE

        self.anims = []
    
    def update(self,target):
        if self.can_move():
            self.movement(target)
        
        self.update_anims()

    def movement(self,target):
        if self.needs_path():
            self.move_path()
        else:
            self.move_towards_target(target)

    def needs_path(self):
        pass


class Blocks:
    WALLS = [7]
    GROUND = [0]



App()