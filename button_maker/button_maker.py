import pyxel, os, random

class App:
    def __init__(self):
        pyxel.init(128,128,fps=120)
        pyxel.load('../notAScrap_8by8.pyxres')

        self.maker_mode = False
        self.button_list = []
        self.currently_drawing = 'N/A'
        ColorPick(self.button_list)
        print(self.button_list)

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_A):
            self.maker_mode = not self.maker_mode
        
        if self.maker_mode:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.currently_drawing = ButtonDraw(len(self.button_list),pyxel.mouse_x,pyxel.mouse_y)
            
            if self.currently_drawing != 'N/A':
                if not self.currently_drawing.drawing:
                    self.button_list.append(Button(self.currently_drawing.x,self.currently_drawing.y,self.currently_drawing.width,self.currently_drawing.height))
        
        for button in self.button_list:
            button.update()


            
    def draw(self):
        pyxel.cls(0)

        if self.maker_mode:
            pyxel.text(0,0,'maker_mode',8)
        
        if self.currently_drawing != 'N/A':
            

        color_counter = 0
        for button in self.button_list:
            for y in range(button.height):
                for x in range(button.width):
                    pyxel.pset(button.x + x,button.y + y,color_counter)
            color_counter+=1
            if color_counter > 16:
                color_counter = 0

        self.draw_mouse_pos()

    def draw_mouse_pos(self):
        pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(pyxel.mouse_x)+','+str(pyxel.mouse_y),7)

class ButtonDraw:
    def __init__(self,name,mouse_x,mouse_y):
        self.name = name
        self.x = mouse_x
        self.y = mouse_y
        self.drawing = True
    
    def update(self):
        if self.drawing:
            self.width = pyxel.mouse_x - self.x
            self.height = pyxel.mouse_y - self.y
            if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.drawing = False
                print('button '+str(self.name)+' done!')
        

class Button:
    def __init__(self,name,x,y,width,length):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class ColorPick:
    def __init__(self,button_list):
        self.x = 0
        self.y = 0
        self.current_color = 0
        self.button_list = button_list
        self.color_dic = {}
    
    def update(self):
        pass

    

App()