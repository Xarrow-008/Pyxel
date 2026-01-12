import toml, pyperclip, pathlib, zipfile, pyxel
from pynput.keyboard import Key, Listener
#from utility import *


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

def rect_in_list(x, y, w, h): 
    all_pos = []
    for in_y in range(h):
        for in_x in range(w):
            all_pos.append((x+in_x,y+in_y))
    return all_pos

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

"""
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
"""

def empty_save_anim():
    dic = {'animations':[{'width':16,'height':16,'name':'N/A','frames':[]}]}
    file = open('draw/save_anim.toml','w')
    toml.dump(dic,file)
    file.close()

def copy_press(txt):
    pyperclip.copy(txt)

canvas = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 2, 2, 2, 2, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 2, 2, 2, 2, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


#print(get_canvas('[[0,0],[0,1,2,3,2][0,9,8]]')[1])

def get_divider(file):
    divider = 0
    for i in range(len(file)):
        if file[i] == '/' or file[i] == "\\":
            divider = i+1
    return divider

def is_in_folder(dir,name):
    folder = pathlib.Path(dir)
    for item in folder.iterdir():
        if item.parts[-1] == name:
            return True
    return False
"""
print(is_in_folder(pather,'main.py'))
        
print(random.randint(0,1))

print(int('1556789'[:1])+2)
"""
#empty_save_anim()




def get_canvas(string):
    liste = []
    i = 1
    index = -1
    while i < len(string):
        char = string[i]
        if char == '[':
            liste.append([])
            index += 1
        elif char.isdigit():
            liste[index].append(get_int(string[i:]))
            while i < len(string) and string[i].isdigit():
                i += 1         
        i += 1
    return liste

def get_int(string):
    number = None
    for i in range(len(string)):
        if string[:i].isdigit():
            number = int(string[:i])
        elif number != None:
            break
    return number

def create_zip(name,path):
    zip = zipfile.ZipFile(name,'x')
    zip.write(path)
    zip.close()


def changeZipContent(name,path):
    file = zipfile.ZipFile(name)
    file.extractall()
    file.close()

    zip = zipfile.ZipFile(path,'w')
    zip.write('pyxel_resource.toml')
    zip.close()

#changeZipContent('rooms.pyxres','newtest.pyxres')

class Door:
    def __init__(self,x,y):
        self.name = 'door'
        self.x = x*10
        self.y = y*10

class Bed:
    def __init__(self,x,y):
        self.name = 'bed'
        self.x = x*10
        self.y = y*10


"""
classList = [Door, Bed]

usableClasses = []
print('in')
usableClasses.append(classList[0](3,1))
usableClasses.append(classList[1](7,1))


print(usableClasses[0].name,usableClasses[0].x )
print(usableClasses[1].name,usableClasses[1].x )
"""

def openToml(path):
    try:
        file = toml.load(path)
    except:
        return None
    else:
        return file

def dumpToml(path, content):
    file = open(path,'w')
    toml.dump(content, file)
    file.close()


"""
dic['presetRooms'].append(room1)


room2 = {'name':'room2','assets':[]}
asset1 = {'name':'doorHorizontal','relativeX':16,'relativeY':32}
room2['assets'].append(asset1)

         
dic = openToml(path)
path = 'rooms/preset_rooms.toml'  
dic = {'presetRooms':[]}
print(dic)

dumpToml(path,dic)
"""

class LoadRoom:
    def __init__(self,settings,x,y):
        self.loaded = True
        self.x = x
        self.y = y
        self.settings = settings
        self.defaultSettings = {'name':'room_48','width':15,'height':15,'assets':[{'name':'tableVertical','relativeX':48,'relativeY':48}]}
        self.assets = []

        self.initSettings()

    def initSettings(self):
        for setting in self.defaultSettings.keys():
            if setting != 'assets':

                if setting in self.settings.keys():
                    setattr(self,setting,copy(self.settings[setting]))
                else:
                    setattr(self,setting,copy(self.defaultSettings[setting]))

                


    def __str__(self):
        string = ''
        for attribute in self.__static_attributes__:
            string += str(attribute) + ': ' + str(getattr(self,attribute)) + '\n'
        return string

settings = {'width':10}


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





"""
SELECT login
FROM Joueurs

SELECT login, mot_de_passe
FROM Joueurs

SELECT gold
FROM Joueurs
WHERE login = 'Yphe'

SELECT login, mot_de_passe
FROM Joueurs

SELECT SUM(gold) AS somme_gold
FROM Joueurs

SELECT DISTINCT lieu_travail AS lieu_travail_distinct
FROM Metiers

SELECT COUNT(*)
FROM Metiers

SELECT COUNT(*)
FROM Metiers
WHERE remuneration > 1000

SELECT nom_faction
FROM Factions
ORDER BY nom_faction ASC

SELECT AVG(remunaeration)
FROM Metiers



SELECT login
FROM Joueurs
JOIN Metiers ON Metiers.id_metier = Joueurs.id_metiers
WHERE nom_metier = 'tailleur'

SELECT login
FROM Joueurs
JOIN Factions ON factions.id_faction = Joueurs.id_faction
WHERE nom_faction = 'Mage'


SELECT login
FROM Joueurs
JOIN Faction ON Faction.id_faction = Joueurs.id_faction
JOIN Metiers ON Metiers.id_metier = Joueur.id_metier
WHERE nom_faction = 'Assassin'
AND nom_metier = 'Paysan'

SELECT login
FROM Reputation
JOIN Joueurs ON Joueurs.login = Reputation.login
JOIN Faction ON Faction.id_faction = Joueurs.id_faction
JOIN Metiers ON Metiers.id_metier = Joueur.id_metier
JOIN Peuple ON Peuple.id_peuple = Reputation.idPeuple
WHERE nom_faction = 'Sorcier'
AND nom_metier = 'Mineur'
AND reputation > 5
AND nom_peuple = 'Orc'

"""
BLEU='\033[94m'
ROUGE='\033[91m'
VERT='\033[92m'
JAUNE='\033[93m'


print(ROUGE + 'test' +JAUNE)



def findDoor(relX, relY, side):
    x = relX
    y = relY
    reverse = False

    if side == 'left' or side == 'right':
        if random.randint(0,1) == 0:
            door = DoorVertical
        else:
            door = DoorHorizontal
            y += 2
        
        if side == 'right':
            reverse = True

    if side == 'up':
        door = DoorVertical
        if random.randint(0,1) == 0:
            reverse = True
            x += -1
        else:
            x += 2

    if side == 'down':
        door = DoorHorizontal
        if random.randint(0,1) == 0:
            reverse = True
            x += -1
        else:
            x += 2

    return door(x,y,reverse)

pyxel.