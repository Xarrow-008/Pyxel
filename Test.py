import pyxel, os, random
from pynput.keyboard import Key, Listener


"""
def draw_palette(x, y, col):
    rgb = pyxel.colors[col]
    hex = f"#{rgb:06X}"
    dec = f"{rgb >> 16},{(rgb >> 8) & 0xFF},{rgb & 0xFF}"

    pyxel.rect(x, y, 13, 13, col)
    pyxel.text(x + 16, y + 1, hex, 7)
    pyxel.text(x + 16, y + 8, dec, 7)
    pyxel.text(x + 5 - (col // 10) * 2, y + 4, f"{col}", 7 if col < 6 else 0)

    if col == 0:
        pyxel.rectb(x, y, 13, 13, 13)


pyxel.init(255, 81, title="Pyxel Color Palette")
pyxel.cls(0)
old_colors = pyxel.colors.to_list()
pyxel.colors.from_list([0x111111, 0x222222, 0x333333])
pyxel.colors[15] = 0x112233

for i in range(16):
    draw_palette(2 + (i % 4) * 64, 4 + (i // 4) * 20, i)

pyxel.show()
"""
os.system('cls')
canvas = [['.' for x in range(20)] for y in range(20)]

digits = [0,1,2,3,4,5,6,7,8,9]
"""
def draw_line(x0,y0,x1,y1):
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


class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(width=128,height=128,fps=120)

        self.tab = []
        self.number = 0
        self.index = 0
        self.coming_back = False
        self.last_lclick = False
        self.lclick = False

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)
    
    def update(self):

        self.last_lclick = self.lclick
        self.lclick = False

        for i in range(10):
            if pyxel.btnp(getattr(pyxel,'KEY_'+str(i))):
                self.number = i
                self.lclick = True
        
        if self.last_lclick and not self.lclick:
            if self.coming_back:
                for i in range(self.index):
                    self.tab.pop(0)
                self.index = 0
            self.tab.insert(0,self.number)
            self.coming_back = False
        
        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_Z):
            if self.index < len(self.tab)-1:
                self.index += 1
                self.coming_back = True
                self.number = self.tab[self.index]

        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_Y):
            if self.index > 0:
                self.index += -1
                self.number = self.tab[self.index]
                self.coming_back = True

        if pyxel.btnp(pyxel.KEY_A):
            print(self.tab, self.index, self.number, self.coming_back)

        #                                                  //\\CAN ERASE CODE - NO PROBLEM//\\
    def draw(self):
        pyxel.cls(0)
        pyxel.text(10,10,str(self.tab),7)
        pyxel.text(14+12*self.index,13,'_',11)
        pyxel.text(18,20,str(self.number),3)

App()
"""

def string_to_list(string):
    final = []
    for i in range(len(string)-1):
        char = string[i]
        if char != ' ' and char != ',' and char != '[' and char != ']':
            if int(char) in digits:
                final.append(int(char))
    return final

def str_to_int(string):
    number = 0
    in_number = False
    for char in string:
        if int(char) in digits:
            if not in_number:
                in_number = True
                number = int(char)
            else:
                number *= 10
                number += int(char)
        elif in_number:
            return number
    return number

        

#print(string_to_list('[1,2,3,4,5,18]'))


#print(str_to_int('jdnbvdfdgzhsnb15j dcbjghkhedj'))
liste = [[8,8,8],[8,8,8],[8,8,8],[8,8,8],[8,8,8],[8,8,8]]

def rect_in_list(x, y, w, h): 
    all_pos = []
    for in_y in range(h):
        for in_x in range(w):
            all_pos.append((x+in_x,y+in_y))
    return all_pos

"""
for y in liste:
    print(y)

dic['x'], dic['y'] = tup



tab1 = [0,1,2,3]

def depiler(tab):
    tab.append(3)

tab = []

def on_press(key):
    print('{0} pressed'.format(key))
    if key == Key.f7:
        draw.App()



def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
"""
for i in range(1):
    print('yaa')