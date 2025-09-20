import pyxel, os, random, copy

ASSETS = {'arrow_left':(0,0), 'arrow_right':(1,0), 'arrow_up':(2,0), 'arrow_down':(3,0), 'cursor':(4,0),
          'pause':(0,1), 'play':(1,1), 'minus':(2,1), 'plus':(3,1),
          'grid':(0,2), 'cross':(1,2),
          'border_UL':(0,3), 'border_UR':(1,3), 'border_BL':(2,3), 'border_BR':(3,3),
          'border_UP':(0,4), 'border_DOWN':(1,4), 'border_LEFT':(2,4), 'border_RIGHT':(3,4)}

BASE_CANVAS = [[0 for x in range(32)] for y in range(32)]

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
        pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(pyxel.mouse_x)+','+str(pyxel.mouse_y),15)
        #pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(self.desk.draw_area.mpos_on_canvas_x)+','+str(self.desk.draw_area.mpos_on_canvas_y),15)


class animation_desk:
    def __init__(self,button_list):
        self.button_list = button_list
        self.draw_area = DrawArea(1,1,95,95,BASE_CANVAS,button_list)
        self.playing = False
        self.start_frame = 0
        self.animation = []
        self.framerate = 10
        self.frames = [{'all_canvas':copy.deepcopy(self.draw_area.past_canvas),'index':0,'coming_back':False}]
        self.frames_index = 0
        self.button_list.append(Button(name='last_frame',color=5,x=26,y=100,width=10,height=10,icon='arrow_left'))
        self.button_list.append(Button('play/pause_anim',5,40,100,10,10,'pause/play'))
        self.button_list.append(Button('next_frame',5,54,100,10,10,'arrow_right'))
        self.button_list.append(Button('zoom_out',5,101,28,10,10,'minus'))
        self.button_list.append(Button('zoom_in',5,116,28,10,10,'plus'))
        self.button_list.append(Button('speed_down',5,101,48,10,10,'minus'))
        self.button_list.append(Button('speed_up',5,116,48,10,10,'plus'))
        self.button_list.append(Button('grid_on/off',5,101,3,10,10,'grid/crossed'))
        self.base_canvas = copy.deepcopy(self.frames[0]['all_canvas'])

    def update(self):
        self.draw_area.update()
        if is_pressed(self.button_list,'play/pause_anim') or pyxel.btnp(pyxel.KEY_LALT):
            self.playing = not self.playing
            if self.playing:
                self.save()
                self.animation = [frame['all_canvas'][frame['index']] for frame in self.frames]
                self.start_frame = pyxel.frame_count
            else:
                self.load()


        if not self.playing:
            if is_pressed(self.button_list,'last_frame') or pyxel.btnp(pyxel.KEY_1):
                self.save()
                if self.frames_index > 0:
                    self.frames_index -= 1
                    self.load()

            if is_pressed(self.button_list,'next_frame') or pyxel.btnp(pyxel.KEY_3):
                self.save()
                if self.frames_index >= len(self.frames)-1:
                    self.frames.append({'all_canvas':copy.deepcopy(self.base_canvas),'index':0,'coming_back':False})

                self.frames_index += 1
                self.load()
        
        else:
            frame = (pyxel.frame_count - self.start_frame)//self.framerate % len(self.animation)-1
            self.draw_area.canvas = self.animation[frame]
            
        if pyxel.btnp(pyxel.KEY_A):
            print(self.draw_area.canvas,flush=True)

        self.parameters_gestion()

    def save(self):
        self.frames[self.frames_index]['coming_back'] = self.draw_area.coming_back
        self.frames[self.frames_index]['index'] = self.draw_area.canvas_index
        self.draw_area.past_canvas[self.draw_area.canvas_index] = copy.deepcopy(self.draw_area.canvas)
        self.frames[self.frames_index]['all_canvas'] = copy.deepcopy(self.draw_area.past_canvas)

    def load(self):
        self.draw_area.coming_back = self.frames[self.frames_index]['coming_back']
        self.draw_area.canvas_index = self.frames[self.frames_index]['index']
        self.draw_area.past_canvas = copy.deepcopy(self.frames[self.frames_index]['all_canvas'])
        self.draw_area.canvas = copy.deepcopy(self.draw_area.past_canvas[self.draw_area.canvas_index])

    def parameters_gestion(self):
        if is_pressed(self.button_list,'grid_on/off'):
            self.draw_area.grid = not self.draw_area.grid
        if is_pressed(self.button_list,'zoom_out'):
            self.draw_area.zoom += -1
        if is_pressed(self.button_list,'zoom_in'):
            self.draw_area.zoom += 1
        if is_pressed(self.button_list,'speed_down'):
            self.framerate += 2
        if is_pressed(self.button_list,'speed_up'):
            self.framerate -= 2
        
        if self.draw_area.zoom <= 0:
            self.draw_area.zoom = 1
        if self.draw_area.zoom >= 6:
            self.draw_area.zoom = 5
        
        if self.framerate <= 0:
            self.framerate = 1
        if self.framerate > 180:
            self.framerate = 180

    def draw(self):
        pyxel.cls(7)

        self.draw_area.draw()
    
    def draw_over(self):
        for button in self.button_list:
            if button.icon != None:
                for key in ASSETS.keys():
                    if button.icon == key:
                        icon(button.x,button.y,img=0,asset_name=key)

            if button.name == 'grid_on/off':
                icon(button.x,button.y,img=0,asset_name='grid',crossed_condition=not self.draw_area.grid)
            if button.name == 'play/pause_anim':
                if self.playing:
                    icon(button.x,button.y,img=0,asset_name='pause')
                else:
                    icon(button.x,button.y,img=0,asset_name='play')

            if button.name == 'zoom_out':
                pyxel.text(button.x + 5,button.y - 7,'Zoom',col=6)

            if button.name == 'speed_down':
                pyxel.text(button.x + 3,button.y - 7,'Speed',col=6)


class DrawArea:
    def __init__(self,x,y,width,height,canvas,button_list):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas = canvas
        self.button_list = button_list

        self.colorpick = ColorPick(button_list,4,113)

        self.past_canvas = [copy.deepcopy(self.canvas)]
        self.canvas_index = 0
        self.coming_back = False
        self.change_canvas = False
        self.color = 0
        self.cam = [0,0]
        self.pencil_pos = (0,0) #position on the canvas
        self.last_pencil_pos = (0,0)
        self.zoom = 5
        self.lclick = False
        self.last_lclick = False
        self.canvas_hold_pos = (0,0)
        self.tool = 'brush'
        self.select_start = (0,0)
        self.select_zone = {'x':0, 'y':0,'w':0,'h':0,'content':[]}
        self.select_holding = False
        self.slide_holding = False
        self.grid = True
        self.grid_size = 8
    
    def update(self):
        self.colorpick.update()
        self.color = self.colorpick.current_color

        if mouse_inside(self.x,self.y,self.width,self.height):
            self.last_pencil_pos = (self.pencil_pos[0], self.pencil_pos[1])
            self.pencil_pos = self.canvas_pos((pyxel.mouse_x,pyxel.mouse_y))

            self.last_lclick = self.lclick    
            self.lclick = False
            self.change_canvas = False

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not pyxel.btn(pyxel.KEY_SPACE):
                self.lclick = True
            
            if self.tool == 'brush':
                if self.lclick:
                    self.paint(self.pencil_pos,self.color)
                    if self.last_lclick:
                        line_from_last_pos = pos_line(self.last_pencil_pos[0],self.last_pencil_pos[1],self.pencil_pos[0],self.pencil_pos[1])
                        for pos in line_from_last_pos:
                            self.paint(pos,self.color)

            elif self.tool == 'select':
                if self.lclick: 
                    if not self.select_holding: #first click
                        self.select_start = self.canvas_pos((pyxel.mouse_x,pyxel.mouse_y))
                        self.select_holding = True
                    else:
                        self.select_zone['x'], self.select_zone['y'] = copy.deepcopy(self.select_start)
                        self.select_zone['w'], self.select_zone['h'] = self.pencil_pos[0] - self.select_start[0], self.pencil_pos[1] - self.select_start[1] 
                else:
                    self.select_holding = False
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) or (pyxel.btnp(pyxel.KEY_X) and not pyxel.btn(pyxel.KEY_LCTRL)):
                self.colorpick.current_color = self.canvas[self.pencil_pos[1]][self.pencil_pos[0]]

            self.slide_canvas_gestion()
        
        if pyxel.btnp(pyxel.KEY_S) and not pyxel.btn(pyxel.KEY_CTRL):
            self.tool = 'select'
            self.lclick = False
        if pyxel.btnp(pyxel.KEY_B):
            self.tool = 'brush'
            self.lclick = False

        if self.tool == 'select':
            if pyxel.btn(pyxel.KEY_LCTRL) and pyxel.btnp(pyxel.KEY_C):
                self.copy_select()
            if pyxel.btn(pyxel.KEY_LCTRL) and pyxel.btnp(pyxel.KEY_X):
                self.copy_select()
                self.delete_select()
            if pyxel.btn(pyxel.KEY_LCTRL) and pyxel.btnp(pyxel.KEY_V):
                self.paste_select() 
                self.change_canvas = True
                
            if pyxel.btnp(pyxel.KEY_H):
                self.inverse_h()
                self.change_canvas = True
            
            if pyxel.btnp(pyxel.KEY_V):
                self.inverse_v()
                self.change_canvas = True
                
            if pyxel.btnp(pyxel.KEY_R):
                self.rotate_counter_clockw()
                self.change_canvas = True
            
            if pyxel.btnp(pyxel.KEY_T):
                self.rotate_clockw()
                self.change_canvas = True

        if self.last_lclick and not self.lclick:
            self.change_canvas = True


        if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.undo_gestion()
        
        self.apply_limits()

        if not mouse_inside(self.x,self.y,self.width,self.height):
            self.lclick = False
            self.last_lclick = False
    

    def draw(self):
        for y in range(self.height//self.zoom+1):
            for x in range(self.width//self.zoom+1):
                for size_y in range(self.zoom):
                    for size_x in range(self.zoom):
                        posx = self.x + x*self.zoom + size_x
                        posy = self.y + y*self.zoom + size_y
                        if point_inside(posx,posy,self.x,self.y,self.width,self.height):
                            if self.cam[1] + y < len(self.canvas) and self.cam[0] + x < len(self.canvas[0]):
                                pyxel.pset(posx, posy, self.canvas[self.cam[1] + y][self.cam[0] + x])
                            else:
                                pyxel.pset(posx, posy, 0)


        if self.grid:
            for x in range(1,len(self.canvas[0])//self.grid_size+1):
                xpos = self.x + (self.grid_size * x - self.cam[0]) * self.zoom
                if xpos >= self.x and xpos < self.x + self.width:
                    y_endline = self.y + min(self.height,(len(self.canvas)-self.cam[1])*self.zoom-1)
                    if is_within_length(xpos,self.canvas[0]*self.zoom) and xpos < self.width:
                        pyxel.line(xpos, self.y, xpos, y_endline, 5)

            for y in range(1,len(self.canvas)//self.grid_size+1):
                ypos = self.y + (self.grid_size * y - self.cam[1]) * self.zoom
                if ypos >= self.y and ypos < self.y + self.height:
                    x_endline = self.x + min(self.width,(len(self.canvas[0])-self.cam[0])*self.zoom-1)
                    if is_within_length(ypos,self.canvas*self.zoom) and ypos < self.height:
                        pyxel.line(self.x, ypos, x_endline, ypos, 5)                                    #starf :(
        
        
        if self.tool == 'select':
            for x in range((self.select_zone['w']+1) * self.zoom - 3):  # - 3 pour la taille de la bordure dans les assets
                self.draw_asset_in(self.x + self.select_zone['x'] * self.zoom + x - self.cam[0]*self.zoom,
                    self.y + self.select_zone['y'] * self.zoom - self.cam[1]*self.zoom, 0, 'border_UP')

                bottom = (self.select_zone['y']+self.select_zone['h'])*self.zoom -6 + self.zoom

                self.draw_asset_in(self.x + self.select_zone['x'] * self.zoom + x - self.cam[0]*self.zoom,
                    self.y + bottom - self.cam[1]*self.zoom, 0, 'border_DOWN')
            
            for y in range((self.select_zone['h']+1) * self.zoom - 3):
                self.draw_asset_in(self.x + self.select_zone['x'] * self.zoom - self.cam[0]*self.zoom,
                    self.y + self.select_zone['y'] * self.zoom + y - self.cam[1]*self.zoom, 0, 'border_LEFT')

                right = (self.select_zone['x']+self.select_zone['w'])*self.zoom -6 + self.zoom

                self.draw_asset_in(self.x + right - self.cam[0]*self.zoom,
                    self.y + self.select_zone['y'] * self.zoom + y - self.cam[1]*self.zoom, 0, 'border_RIGHT')
            
            
            self.draw_asset_in(self.x + self.select_zone['x'] * self.zoom - self.cam[0]*self.zoom,
                self.y + self.select_zone['y'] * self.zoom - self.cam[1]*self.zoom, 0, 'border_UL')

            self.draw_asset_in(self.x + (self.select_zone['x'] + self.select_zone['w']) * self.zoom -6 + self.zoom - self.cam[0]*self.zoom,
                self.y + self.select_zone['y'] * self.zoom - self.cam[1]*self.zoom, 0, 'border_UR')

            self.draw_asset_in(self.x + self.select_zone['x'] * self.zoom - self.cam[0]*self.zoom,
                self.y + (self.select_zone['y'] + self.select_zone['h']) * self.zoom -6 + self.zoom - self.cam[1]*self.zoom, 0, 'border_BL')
                
            self.draw_asset_in(self.x + (self.select_zone['x'] + self.select_zone['w']) * self.zoom -6 + self.zoom - self.cam[0]*self.zoom,
                self.y + (self.select_zone['y'] + self.select_zone['h']) * self.zoom -6 + self.zoom - self.cam[1]*self.zoom, 0, 'border_BR')

        
        self.colorpick.draw()

    
    def canvas_pos(self,pos=(0,0)):
        return( (pos[0] - self.x) // self.zoom + self.cam[0],
                (pos[1] - self.y) // self.zoom + self.cam[1]
        )
    
    def paint(self,pos,color):
        if is_within_length(pos[1],self.canvas) and is_within_length(pos[0],self.canvas[0]):
            self.canvas[pos[1]][pos[0]] = color

    def undo_gestion(self):
        if self.change_canvas:
            if len(self.past_canvas) > 16:
                self.past_canvas.pop(len(self.past_canvas)-1)
            if self.coming_back:
                for i in range(self.canvas_index):
                    self.past_canvas.pop(0)
                self.canvas_index = 0
            self.past_canvas.insert(0,copy.deepcopy(self.canvas))
            self.coming_back = False
        
        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_Z):
            if len(self.past_canvas) > 1 and self.canvas_index < len(self.past_canvas)-1:
                self.canvas_index += 1
                self.coming_back = True
                self.canvas = copy.deepcopy(self.past_canvas[self.canvas_index])

        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_Y):
            if self.canvas_index > 0:
                self.canvas_index += -1
                self.canvas = copy.deepcopy(self.past_canvas[self.canvas_index])
                self.coming_back = True

    def slide_canvas_gestion(self):
            if (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.btn(pyxel.KEY_SPACE)) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
                if not self.slide_holding:
                    self.canvas_hold_pos = (pyxel.mouse_x + self.cam[0] * self.zoom, pyxel.mouse_y + self.cam[1] * self.zoom)
                else:
                    self.cam = [(self.canvas_hold_pos[0] - pyxel.mouse_x) // self.zoom, 
                                (self.canvas_hold_pos[1] - pyxel.mouse_y) // self.zoom]

                    if self.cam[0]<0:
                        self.cam[0] = 0
                    if self.cam[0] > len(self.canvas[0]) - 4:
                        self.cam[0] = len(self.canvas[0]) - 4
                    if self.cam[1] < 0:
                        self.cam[1] = 0
                    if self.cam[1] > len(self.canvas) - 4:
                        self.cam[1] = len(self.canvas) - 4

                self.slide_holding = True
            else:
                self.slide_holding = False

    def copy_select(self):
        self.select_zone['content'] = [[0 for X in range(self.select_zone['w']+1)] for Y in range(self.select_zone['h']+1)]
        for y in range(self.select_zone['h']+1):
            for x in range(self.select_zone['w']+1):
                self.select_zone['content'][y][x] = self.canvas[self.select_zone['y'] + y][self.select_zone['x'] + x]

    def paste_select(self):
        for y in range(len(self.select_zone['content'])):
            if is_within_length(self.select_zone['y'] + y,self.canvas):
                for x in range(len(self.select_zone['content'][0])):
                    if is_within_length(self.select_zone['x'] + x,self.canvas[0]):
                        self.canvas[self.select_zone['y'] + y][self.select_zone['x'] + x] = self.select_zone['content'][y][x]

    def delete_select(self):
        for y in range(self.select_zone['h']+1):
            for x in range(self.select_zone['w']+1):
                self.canvas[self.select_zone['y'] + y][self.select_zone['x'] + x] = 0

    def inverse_h(self):
        self.copy_select()
        temp = []
        for row in self.select_zone['content']:
            temp.insert(0,row)
        self.select_zone['content'] = temp
        self.paste_select()

    def inverse_v(self):
        self.copy_select()
        temp = []
        for y in range(len(self.select_zone['content'])):
            temp.append([])
            for pixel in self.select_zone['content'][y]:
                temp[y].insert(0,pixel)
        self.select_zone['content'] = temp
        self.paste_select()

    def rotate_clockw(self): #clockwise
        self.copy_select()
        side = max(self.select_zone['h'], self.select_zone['w'])
        temp = []
        
        for x in range(self.select_zone['w']):
            temp.append([])
            for y in range(self.select_zone['h']):
                temp[x].append(self.select_zone['content'][-y-1][x])
        
        self.delete_select()

        self.select_zone['w'], self.select_zone['h'] = self.select_zone['h'], self.select_zone['w']
        self.select_zone['content'] = temp
        self.paste_select()

    def rotate_counter_clockw(self): #counter clockwise
        self.copy_select()
        side = max(self.select_zone['h'], self.select_zone['w'])
        temp = []
        
        for x in range(self.select_zone['w']):
            temp.append([])
            for y in range(self.select_zone['h']):
                temp[x].append(self.select_zone['content'][y][-x-1])
        
        self.delete_select()

        self.select_zone['w'], self.select_zone['h'] = self.select_zone['h'], self.select_zone['w']
        self.select_zone['content'] = temp
        self.paste_select()


    def draw_asset_in(self,x, y, img, asset_name):
        if (point_inside(x,y,self.x,self.y,self.width,self.height) and
            point_inside(x+3,y+3,self.x,self.y,self.width,self.height)):
            
            icon(x,y,img,asset_name)

    def apply_limits(self):
        if self.select_zone['w'] < 7//self.zoom:
            self.select_zone['w'] = 7//self.zoom
        if self.select_zone['h'] < 7//self.zoom:
            self.select_zone['h'] = 7//self.zoom


        if self.select_zone['x'] + 7//self.zoom > len(self.canvas[0])-1:
            self.select_zone['x'] = len(self.canvas[0])-1 - 7//self.zoom
            self.select_start = (len(self.canvas[0])-1 - 7//self.zoom, self.select_start[1])
            self.select_zone['w'] = 7//self.zoom

        if self.select_zone['y'] + 7//self.zoom > len(self.canvas)-1:
            self.select_zone['y'] = len(self.canvas)-1 - 7//self.zoom
            self.select_start = (self.select_start[0], len(self.canvas)-1 - 7//self.zoom)
            self.select_zone['h'] = 7//self.zoom


        if self.select_zone['x'] + self.select_zone['w'] > len(self.canvas[0])-1:
            self.select_zone['w'] = len(self.canvas[0])-1 - self.select_zone['x']

        if self.select_zone['y'] + self.select_zone['h'] > len(self.canvas)-1:
            self.select_zone['h'] = len(self.canvas)-1 - self.select_zone['y']


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
    def __init__(self,name,color,x,y,width,height,icon=None):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.icon = icon
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
        self.current_color = 7
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
    return point_inside(pyxel.mouse_x,pyxel.mouse_y,x,y,width,height)

def point_inside(point_x,point_y,area_x,area_y,width,height):
    return (point_x >= area_x and point_x <= area_x + width) and (
            point_y >= area_y and point_y <= area_y + height
            )

def show(x, y, img, asset, colkey=None, rotate=None, scale=1):
    pyxel.blt(x + 10//2*(scale-1), y + 10//2*(scale-1), img, asset[0]*11, asset[1]*11, 10, 10, colkey=colkey, rotate=rotate, scale=scale)

def icon(x, y, img, asset_name, crossed_condition=False, colkey=5, scale=1):
    show(x, y, img, ASSETS[asset_name],colkey=colkey, scale=scale)
    if crossed_condition:
        show(x, y, img, ASSETS['cross'],colkey=colkey,scale=scale)

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

def is_within_length(nb,list):
    return nb < len(list)

def rect_in_list(x, y, w, h): 
    all_pos = []
    for in_y in range(h):
        for in_x in range(w):
            all_pos.append((x+in_x,y+in_y))
    return all_pos

App()