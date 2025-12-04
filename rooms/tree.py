from utility import *

CAM_WIDTH = 256
CAM_HEIGHT = 256


buttonList = []
zoom = 1


class App:
    def __init__(self):
        pyxel.init(CAM_WIDTH,CAM_HEIGHT,fps=60)

        self.show = Tree()

        self.camera = [0,0]
        self.camSpeed = 4

        pyxel.mouse(True)

        pyxel.run(self.update,self.draw)

    def update(self):
        self.show.update()
        self.cameraUpdate()

    def draw(self):
        self.show.draw()

    def cameraUpdate(self):
        global zoom
        if pyxel.btn(pyxel.KEY_Q):
            self.camera[0] += -self.camSpeed
        if pyxel.btn(pyxel.KEY_D):
            self.camera[0] += self.camSpeed
        if pyxel.btn(pyxel.KEY_Z):
            self.camera[1] += -self.camSpeed
        if pyxel.btn(pyxel.KEY_S):
            self.camera[1] += self.camSpeed


        if pyxel.mouse_wheel == 1:
            zoom *= 2
            self.camera[0] *= 2
            self.camera[1] *= 2
        if pyxel.mouse_wheel == -1:
            zoom /= 2
            self.camera[0] /= 2
            self.camera[1] /= 2


        if pyxel.btnp(pyxel.KEY_SPACE):
            self.camera = [0,0]
            zoom = 1

        pyxel.camera(*self.camera)

class Tree:
    def __init__(self):
        self.posTree = (64,0)
        self.selected = 'root'

        self.root = Node(size=1,pos=self.posTree)

    def update(self):
        if pyxel.btnp(pyxel.KEY_A):
            print(self.root.length())

        self.root.update(self.posTree)

    def draw(self):
        pyxel.cls(0)
        self.root.draw()

class NodeSet:
    def __init__(self, size, child1=None, child2=None):
        self.size = size
        self.child1 = child1
        self.child2 = child2

        if self.size < 8: #stop at 4 and do *2 every length
            self.child1 = Node(self.size*2)
            self.child2 = Node(self.size*2)

    def length(self):
        childrenLength = 0
        if self.child1 != None:
            childrenLength += self.child1.length()
        if self.child2 != None:
            childrenLength += self.child2.length()
        return 1 + childrenLength

    def update(self):
        pass

    def draw(self,pos):
        size = 128//(self.size)

        rectangle(pos[0], pos[1], size, size, 1)
        rectangleBlank(pos[0], pos[1], size, size, 6)

        text(pos[0]+size//2-2,pos[1]+size//2-2,str(self.size),8)


        if self.child1 != None:
            self.child1.draw((pos[0],pos[1]+size))
        if self.child2 != None:
            self.child2.draw((pos[0]+size//2,pos[1]+size))


class Node:
    def __init__(self, size, pos=[0,0], children=[]):
        global buttonList
        self.size = size
        self.children = copy(children)
        self.pos = copy(pos)


        if self.size < 28:
            for i in range(3):
                position = (self.pos[0]+i*self.boundaries()/3, self.pos[1]+self.boundaries())
                self.children.append(Node(self.size*3, pos=position))

    def length(self):
        childrenLength = 0
        for child in self.children:
            childrenLength += child.length()
        return 1 + childrenLength

    def nbKids(self):
        return len(self.children)

    def update(self,pos=[0,0]):
        self.pos = copy(pos)


    def boundaries(self):
        return 128/(self.size)

    def draw(self):
        rectangle(self.pos[0]+self.boundaries()/4, self.pos[1]+self.boundaries()/2, self.boundaries()/2, self.boundaries()/2, 1)


        rectangleBlank(self.pos[0], self.pos[1], self.boundaries(), self.boundaries(), 6)
        #text(self.pos[0]+self.boundaries()//2-2,self.pos[1]+self.boundaries()//2-2,str(self.size),8)

        for i in range(self.nbKids()):
            self.children[i].draw()



def rectangle(x, y, w, h, col):
    pyxel.rect(x*zoom, y*zoom, w*zoom, h*zoom, col)

def rectangleBlank(x, y, w, h, col):
    pyxel.rectb(x*zoom, y*zoom, w*zoom, h*zoom, col)

def text(x, y, string, col):
    pyxel.text(x*zoom,y*zoom,string,col)


App()
