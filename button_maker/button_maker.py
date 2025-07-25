import pyxel, os, random

ASSETS = {'arrow_left':(0,0),'arrow_right':(1,0),'arrow_up':(2,0),'arrow_down':(3,0),'pause':(0,1),'start':(1,1)}

class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(128,128,fps=120)
        pyxel.load('../makers_asset.pyxres')

        self.button_list = []
        self.desk = animation_desk(self.button_list)
        #self.desk = button_maker_desk(self.button_list)

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.desk.update()

        for button in self.button_list:
            button.update()

    def draw(self):
        self.desk.draw()
        
        for button in self.button_list:
            pyxel.rect(button.x, button.y, button.width, button.height, button.name)

        self.draw_mouse_pos()

    def draw_mouse_pos(self):
        pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(pyxel.mouse_x)+','+str(pyxel.mouse_y),15)


class animation_desk:
    def __init__(self,button_list):
        self.button_list = button_list
        self.colorpick = ColorPick(button_list,2,114)
        self.button_list.append(Button(5,26,100,10,10))
        self.button_list.append(Button(5,40,100,10,10))
        self.button_list.append(Button(5,54,100,10,10))

    def update(self):
        self.colorpick.update()

    def draw(self):
        pyxel.cls(7)
        pyxel.rect(1,1,98,98,11)

        self.colorpick.draw()
    
    def draw_over(self):
        show(x=26,y=100,img=0,asset=ASSETS['arrow_left'])
        show(x=54,y=100,img=0,asset=ASSETS['arrow_right'])
        show(x=40,y=100,img=0,asset=ASSETS['arrow_left'])


class button_maker_desk:
    def __init__(self,button_list):
        self.button_list = button_list
        self.maker_mode = False
        self.colorpick = ColorPick(button_list,72,2)
        self.currently_drawing = 'N/A'

    def update(self):
        if pyxel.btnp(pyxel.KEY_A):
            self.maker_mode = not self.maker_mode
        
        
        if self.maker_mode:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.currently_drawing = ButtonDraw(self.colorpick.current_color,pyxel.mouse_x,pyxel.mouse_y)
            
            if self.currently_drawing != 'N/A':
                self.currently_drawing.update()
                if not self.currently_drawing.is_drawing:
                    if self.currently_drawing.width > 1 and self.currently_drawing.height > 1:
                        self.button_list.append(Button(self.currently_drawing.name,
                                                self.currently_drawing.x,
                                                self.currently_drawing.y,
                                                self.currently_drawing.width,
                                                self.currently_drawing.height)
                                                )                    
                    self.currently_drawing = 'N/A'
        
        self.colorpick.update()
    
    def draw(self):
        pyxel.cls(0)
        if self.maker_mode:
            pyxel.text(0,0,'maker_mode',8)
        pyxel.text(0,123,'A to switch on/off maker mode',7)

        if self.currently_drawing != 'N/A':
            for y in range(self.currently_drawing.height):
                for x in range(self.currently_drawing.width):
                    pyxel.pset(self.currently_drawing.x + x,self.currently_drawing.y + y,self.currently_drawing.name)
        
        self.colorpick.draw()


class ButtonDraw:
    def __init__(self,name,mouse_x,mouse_y):
        self.name = name
        self.x = mouse_x
        self.y = mouse_y
        self.width = 0
        self.height = 0
        self.is_drawing = True
    
    def update(self):
        if self.is_drawing:
            self.width = pyxel.mouse_x - self.x
            self.height = pyxel.mouse_y - self.y
            if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.is_drawing = False
        

class Button:
    def __init__(self,name,x,y,width,height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pressed = False
    
    def update(self):
        if (pyxel.mouse_x > self.x and pyxel.mouse_x < self.x + self.width) and (
            pyxel.mouse_y > self.y and pyxel.mouse_y < self.y + self.height
        ):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.pressed = True
            else:
                self.pressed = False
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                print(f'        self.button_list.append(Button({self.name},{self.x},{self.y},{self.width},{self.height}))')


class ColorPick:
    def __init__(self,button_list,x,y):
        self.x = x
        self.y = y
        self.width = 58
        self.height = 16
        self.current_color = 0
        self.button_list = button_list
        self.color_buttons = []
        self.color_buttons.append(Button(0,self.x+0,self.y+0,5,5))
        self.color_buttons.append(Button(1,self.x+7,self.y+0,5,5))
        self.color_buttons.append(Button(2,self.x+14,self.y+0,5,5))
        self.color_buttons.append(Button(3,self.x+21,self.y+0,5,5))
        self.color_buttons.append(Button(4,self.x+28,self.y+0,5,5))
        self.color_buttons.append(Button(5,self.x+35,self.y+0,5,5))
        self.color_buttons.append(Button(6,self.x+42,self.y+0,5,5))
        self.color_buttons.append(Button(7,self.x+49,self.y+0,5,5))
        self.color_buttons.append(Button(8,self.x+0,self.y+7,5,5))
        self.color_buttons.append(Button(9,self.x+7,self.y+7,5,5))
        self.color_buttons.append(Button(10,self.x+14,self.y+7,5,5))
        self.color_buttons.append(Button(11,self.x+21,self.y+7,5,5))
        self.color_buttons.append(Button(12,self.x+28,self.y+7,5,5))
        self.color_buttons.append(Button(13,self.x+35,self.y+7,5,5))
        self.color_buttons.append(Button(14,self.x+42,self.y+7,5,5))
        self.color_buttons.append(Button(15,self.x+49,self.y+7,5,5))
        for button in self.color_buttons:
            self.button_list.append(button)
    
    def update(self):
        for button in self.color_buttons:
            if button.pressed:
                self.current_color = button.name
                print(self.current_color)

    def draw(self):
        corners = [(self.x-2,self.y-2),(self.x-3+self.width,self.y-2),(self.x-3+self.width,self.y-3+self.height),(self.x-2,self.y-3+self.height)]
        color_below_corners = [pyxel.pget(corner[0],corner[1]) for corner in corners]
        pyxel.rect(self.x-2,self.y-2,self.width,self.height,1)
        for i in range(len(corners)):
            pyxel.pset(corners[i][0],corners[i][1],color_below_corners[i])
    

def show(x, y, img, asset, colkey=None, rotate=None, scale=1):
    pyxel.blt(x + w//2*(scale-1), y + h//2*(scale-1), img, asset[0], asset[1], 10, 10, colkey=colkey, rotate=rotate, scale=scale)
App()