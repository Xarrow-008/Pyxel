import pyxel, os, random

ASSETS = {'arrow_left':(0,0),'arrow_right':(1,0),'arrow_up':(2,0),'arrow_down':(3,0),'pause':(0,1),'play':(1,1)}

class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(width=128,height=128,fps=120)
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
            pyxel.rect(button.x, button.y, button.width, button.height, button.color)
        
        self.desk.draw_over()

        self.draw_mouse_pos()

    def draw_mouse_pos(self):
        #pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(pyxel.mouse_x)+','+str(pyxel.mouse_y),15)
        pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(self.desk.draw_area.mpos_on_canvas_x)+','+str(self.desk.draw_area.mpos_on_canvas_y),15)


class animation_desk:
    def __init__(self,button_list):
        self.button_list = button_list
        self.colorpick = ColorPick(button_list,4,113)
        self.draw_area = DrawArea(1,1,98,98)
        self.playing = False
        self.button_list.append(Button(name='previous_frame',color=5,x=26,y=100,width=10,height=10))
        self.button_list.append(Button('play/pause_anim',5,40,100,10,10))
        self.button_list.append(Button('next_frame',5,54,100,10,10))

    def update(self):
        self.colorpick.update()
        self.draw_area.update(self.colorpick.current_color)
        if is_pressed(self.button_list,'play/pause_anim'):
            self.playing = not self.playing

    def draw(self):
        pyxel.cls(7)
        pyxel.rect(1,1,98,98,col=11)

        self.draw_area.draw()
        self.colorpick.draw()
    
    def draw_over(self):
        show(x=26,y=100,img=0,asset=ASSETS['arrow_left'])
        show(x=54,y=100,img=0,asset=ASSETS['arrow_right'])
        if self.playing:
            show(x=40,y=100,img=0,asset=ASSETS['pause'])
        else:
            show(x=40,y=100,img=0,asset=ASSETS['play'])


class DrawArea:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas = [[2 for x in range(256)] for y in range(256)]
        self.color = 0
        self.cam_x = 0
        self.cam_y = 0
        self.mpos_on_canvas_x = 0
        self.mpos_on_canvas_y = 0
        self.last_mpos_on_canvas_x = 0
        self.last_mpos_on_canvas_y = 0
        self.lclick = False
        self.last_lclick = False
        self.canvas_hold_pos = (0,0)
        self.holding = False
    def update(self,color):
        self.color = color
        if mouse_inside(self.x,self.y,self.width,self.height):
            self.last_mpos_on_canvas_x = self.mpos_on_canvas_x
            self.last_mpos_on_canvas_y = self.mpos_on_canvas_y
            self.mpos_on_canvas_x = pyxel.mouse_x + self.cam_x - self.x
            self.mpos_on_canvas_y = pyxel.mouse_y + self.cam_y - self.y

            if self.lclick:
                self.last_lclick = True
            self.lclick = False
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not pyxel.btn(pyxel.KEY_SPACE):
                self.canvas[self.mpos_on_canvas_y][self.mpos_on_canvas_x] = self.color
                self.lclick = True
                if self.last_lclick:
                    line_from_last_pos = pos_line(self.last_mpos_on_canvas_x,self.last_mpos_on_canvas_y,self.mpos_on_canvas_x,self.mpos_on_canvas_y)
                    for pos in line_from_last_pos:
                        self.canvas[pos[1]][pos[0]] = self.color

            if (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.btn(pyxel.KEY_SPACE)) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
                if not self.holding:
                    self.canvas_hold_pos = (self.cam_x + pyxel.mouse_x,self.cam_y + pyxel.mouse_y)
                else:
                    self.cam_x = self.canvas_hold_pos[0] - pyxel.mouse_x
                    self.cam_y = self.canvas_hold_pos[1] - pyxel.mouse_y
                    if self.cam_x<0:
                        self.cam_x = 0
                    if self.cam_x + self.width > 255:
                        self.cam_x = 255 - self.width
                    if self.cam_y<0:
                        self.cam_y = 0
                    if self.cam_y + self.height > 255:
                        self.cam_y = 255 - self.height

                self.holding = True
            else:
                self.holding = False
        
        if not mouse_inside(self.x,self.y,self.width,self.height):
            self.lclick = False
            self.last_lclick = False
    
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                pyxel.pset(self.x + x, self.y + y, self.canvas[self.cam_y + y][self.cam_x + x])


class button_maker_desk:
    def __init__(self,button_list):
        self.button_list = button_list
        self.maker_mode = False
        self.colorpick = ColorPick(button_list,x=72,y=2)
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
                        self.button_list.append(Button('color_select',
                                                self.currently_drawing.color,
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
            pyxel.text(x=0,y=0,s='maker_mode',col=8)
        pyxel.text(x=0,y=123,s='A to switch on/off maker mode',col=7)

        if self.currently_drawing != 'N/A':
            for y in range(self.currently_drawing.height):
                for x in range(self.currently_drawing.width):
                    pyxel.pset(self.currently_drawing.x + x,self.currently_drawing.y + y,self.currently_drawing.color)
        
        self.colorpick.draw()

    def draw_over(self):
        pass


class ButtonDraw:
    def __init__(self,color,mouse_x,mouse_y):
        self.color = color
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
    def __init__(self,name,color,x,y,width,height):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pressed = False
    
    def update(self):
        if mouse_inside(self.x,self.y,self.width,self.height):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.pressed = True
            else:
                self.pressed = False
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                print(f'        self.button_list.append(Button("color_select",{self.name},{self.x},{self.y},{self.width},{self.height}))')


class ColorPick:
    def __init__(self,button_list,x,y):
        self.x = x
        self.y = y
        self.width = 58
        self.height = 16
        self.current_color = 0
        self.button_list = button_list
        self.color_buttons = []
        self.color_buttons.append(Button(name='color_select',color=0,x=self.x+0,y=self.y+0,width=5,height=5))
        self.color_buttons.append(Button('color_select',1,self.x+7,self.y+0,5,5))
        self.color_buttons.append(Button('color_select',2,self.x+14,self.y+0,5,5))
        self.color_buttons.append(Button('color_select',3,self.x+21,self.y+0,5,5))
        self.color_buttons.append(Button('color_select',4,self.x+28,self.y+0,5,5))
        self.color_buttons.append(Button('color_select',5,self.x+35,self.y+0,5,5))
        self.color_buttons.append(Button('color_select',6,self.x+42,self.y+0,5,5))
        self.color_buttons.append(Button('color_select',7,self.x+49,self.y+0,5,5))
        self.color_buttons.append(Button('color_select',8,self.x+0,self.y+7,5,5))
        self.color_buttons.append(Button('color_select',9,self.x+7,self.y+7,5,5))
        self.color_buttons.append(Button('color_select',10,self.x+14,self.y+7,5,5))
        self.color_buttons.append(Button('color_select',11,self.x+21,self.y+7,5,5))
        self.color_buttons.append(Button('color_select',12,self.x+28,self.y+7,5,5))
        self.color_buttons.append(Button('color_select',13,self.x+35,self.y+7,5,5))
        self.color_buttons.append(Button('color_select',14,self.x+42,self.y+7,5,5))
        self.color_buttons.append(Button('color_select',15,self.x+49,self.y+7,5,5))
        for button in self.color_buttons:
            self.button_list.append(button)
    
    def update(self):
        for button in self.color_buttons:
            if button.pressed:
                self.current_color = button.color
                print(self.current_color)

    def draw(self):
        corners = [(self.x-2,self.y-2),(self.x-3+self.width,self.y-2),(self.x-3+self.width,self.y-3+self.height),(self.x-2,self.y-3+self.height)]
        color_below_corners = [pyxel.pget(corner[0],corner[1]) for corner in corners]
        pyxel.rect(self.x-2,self.y-2,self.width,self.height,1)
        for i in range(len(corners)):
            pyxel.pset(corners[i][0],corners[i][1],color_below_corners[i])
    

def is_pressed(button_list,name,pos='N/A'):
    for button in button_list:
        if button.pressed and button.name == name:
            if pos == 'N/A':
                return True
            else:
                if pos == (button.x,button.y):
                    return True
    return False

def mouse_inside(x,y,width,height):
    if (pyxel.mouse_x >= x and pyxel.mouse_x <= x + width) and (
            pyxel.mouse_y >= y and pyxel.mouse_y <= y + height
        ):
        return True
    else:
        return False

def show(x, y, img, asset, colkey=None, rotate=None, scale=1):
    pyxel.blt(x + 10//2*(scale-1), y + 10//2*(scale-1), img, asset[0]*11, asset[1]*11, 10, 10, colkey=colkey, rotate=rotate, scale=scale)

def on_tick(tickrate=60,delay=0): #allows the computer to make operations only on certain times to not do averything 120 times a second
    return (pyxel.frame_count % tickrate)-delay == 0

def pos_line(x0,y0,x1,y1): #not exactly bresenham's algorithm because i dont understand it all yet but ill change it when i do
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


App()