import pyxel, os, random, copy

class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(128,128)
        pyxel.load('../notascrap.pyxres')

        self.map = [[0 for x in range(32)] for y in range(32)]
        self.mob = Mob(self.map)

        pyxel.run(self.update,self.draw)

    def update(self):
        self.mob.update()
    def draw(self):
        pyxel.cls(1)

class Mob:
    def __init__(self,map):
        self.x = 0
        self.y = 0
        self.map = map
        self.image = (0,3)
        self.pathing = []
    def update(self):
        if on_tick(120):    
            self.new_path()
    def draw(self):
        show(self.x,self.y,self.image)
    
    def new_path(self):
        targetX = 100//16
        targetY = 100//16
        self.a_star_pathing(targetX,targetY)

    def a_star_pathing(self,x,y):
        posX = self.x //16
        posY = self.y //16
        map = copy.deepcopy(self.map)
        positions = [(posX,posY)]
        while (x,y) not in positions:
            for pos in positions:
                if pos[0]+1 in len(map):
                    pass
                
            


def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def show(x,y,img,colkey=11,save=0):
    pyxel.blt(x,y,save,img[0]*16,img[1]*16,16,16,colkey=11)
