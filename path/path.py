import os,random,pyxel
from copy import deepcopy as copy




class App:
    def __init__(self):

        os.system('cls')
        pyxel.init(100,100,fps=20)
        pyxel.load('../notAScrap.pyxres')
        pyxel.colors[2] = 5373971
        
        self.entity = Path()

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.entity.update()
    
    def draw(self):
        pyxel.cls(0)
        self.entity.draw()
        

class Path:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.targetx = 8
        self.targety = 0

        self.border = [(self.x,self.y)]
        self.new_border = []
        self.checked = []
        self.path_check = [[self.border[0]]]
        self.finished = False

        self.map = [[0 for x in range(10)] for y in range(10)]

        for y in range(6):
            self.map[y][5] = 7

    def update(self):
        cross = [(0,-1),(0,1),(-1,0),(1,0)]
        if (self.targetx,self.targety) not in self.checked:
            for pos in self.border:
                for addon in cross:
                    new_pos = (pos[0]+addon[0],pos[1]+addon[1])
                    if new_pos not in self.checked:
                        if is_inside_map(new_pos, self.map):
                            if self.map[new_pos[1]][new_pos[0]] == 0:
                                if new_pos not in self.new_border:
                                    self.new_border.append(new_pos)
                self.checked.append(pos)
            print(self.border)
            self.border = copy(self.new_border)
            self.new_border = []
            
                
    def draw(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                color = self.map[y][x]
                pyxel.rect(x*10,y*10,10,10,color)

        for pos in self.checked:
            pyxel.rect(pos[0]*10,pos[1]*10,10,10,6)

        if self.finished:
            pyxel.rect(self.targetx*10,self.targety*10,10,10,11)
        else:
            pyxel.rect(self.targetx*10,self.targety*10,10,10,9)


def is_inside_map(pos,map):
    if pos[0] >= len(map[0]) or pos[1] >= len(map):
        return False
    if pos[0] < 0 or pos[1] < 0:
        return False
    return True
    
def remove_doubles(list):
    new_list = []
    for element in list:
        if not element in new_list:
            new_list.append(element)
    return new_list





App()