import pyxel, os, random

class App:
    def __init__(self):
        pyxel.init(128,128,fps=120)
        pyxel.load('../notAScrap_8by8.pyxres')

        self.maker_mode = False
        self.button_list = []
        self.currently_drawing = 'N/A'
        self.colorpick = ColorPick(self.button_list)

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

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
                        self.button_list.append(Button(self.currently_drawing.color_nb,
                                                self.currently_drawing.x,
                                                self.currently_drawing.y,
                                                self.currently_drawing.width,
                                                self.currently_drawing.height)
                                                )                    
                    self.currently_drawing = 'N/A'

        for button in self.button_list:
            button.update()
        self.colorpick.update()
            


            
    def draw(self):
        pyxel.cls(0)

        if self.maker_mode:
            pyxel.text(0,0,'maker_mode',8)

        if self.currently_drawing != 'N/A':
            for y in range(self.currently_drawing.height):
                for x in range(self.currently_drawing.width):
                    pyxel.pset(self.currently_drawing.x + x,self.currently_drawing.y + y,self.currently_drawing.color_nb)

        for button in self.button_list:
            for y in range(button.height):
                for x in range(button.width):
                    pyxel.pset(button.x + x,button.y + y,button.color_nb)

        self.draw_mouse_pos()

    def draw_mouse_pos(self):
        pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(pyxel.mouse_x)+','+str(pyxel.mouse_y),7)

class ButtonDraw:
    def __init__(self,color_nb,mouse_x,mouse_y):
        self.color_nb = color_nb
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
    def __init__(self,color_nb,x,y,width,height):
        self.color_nb = color_nb
        self.name = 'color_'+str(color_nb)
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
                print(f'        self.color_buttons.append(Button({self.color_nb},self.x+{self.x},self.y+{self.y},{self.width},{self.height}))')

class ColorPick:
    def __init__(self,button_list):
        self.x = 50
        self.y = 0
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
                self.current_color = button.color_nb
                print(self.current_color)

    

App()
Button(1,1,1)