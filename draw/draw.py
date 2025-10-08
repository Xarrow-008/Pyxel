import pyxel, os, random, copy, toml, zipfile, csv

ASSETS = {'arrow_left':(0,0), 'arrow_right':(1,0), 'arrow_up':(2,0), 'arrow_down':(3,0), 'cursor':(4,0),
          'pause':(0,1), 'play':(1,1), 'minus':(2,1), 'plus':(3,1),
          'grid':(0,2), 'cross':(1,2),
          'border_UL':(0,3), 'border_UR':(1,3), 'border_BL':(2,3), 'border_BR':(3,3),
          'border_UP':(0,4), 'border_DOWN':(1,4), 'border_LEFT':(2,4), 'border_RIGHT':(3,4)}

BASE_CANVAS = [[0 for x in range(32)] for y in range(32)]

LETTERS = 'AZERTYUIOPQSDFGHJKLMWXCVBN'
PONCTUATION = [' ', ',', ';', ':', '!', '&', '', '"', "'", '(', '-', '', '_', '', '', ')', '=']
PONC_SHIFT = [' ', '?', '.', '/', '§', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '', '+']
PONC_ALT = [' ', '', '', '', '', '', '', '', "{", '[', '|', '`', '', '', '', ']', '}']
PONC_PYXEL = ['SPACE','COMMA','SEMICOLON','COLON','EXCLAIM','1','2','3','4','5','6','7','8','9','0','RIGHTPAREN','EQUALS']
KEYS = list(LETTERS)+PONCTUATION


class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(width=128,height=128,fps=120)
        pyxel.load('../makers_asset.pyxres')

        #self.save = toml.load('save.toml')

        self.button_list = []
        #self.desk = animation_desk(self.button_list)
        #self.desk = button_maker_desk(self.button_list)
        self.desk = folders_desk(self.button_list)

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):

        self.desk.update()
        self.desk_msg_update()
        for button in self.button_list:
            button.update()

        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_A):
            self.desk.quick_save()
            self.desk.switch = {'to':'folders','argument':{}}
        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_S):
            self.desk.quick_save()
            if self.desk.can_save:
                self.desk.msg = {'txt':'saved','time':3}
        
        self.switch_desk_gestion()


    def draw(self):

        self.desk.draw()
        
        for button in self.button_list:
            pyxel.rect(button.x, button.y, button.width, button.height, button.color)
        
        self.desk.draw_over()
        self.draw_over()

        #self.draw_mouse_pos()

    def draw_over(self):
        for button in self.button_list:
            if button.icon != None:
                for key in ASSETS.keys():
                    if button.icon == key:
                        icon(button.x,button.y,img=0,asset_name=key)

            if button.name == 'grid_on/off':
                icon(button.x,button.y,img=0,asset_name='grid',crossed_condition=not self.desk.draw_area.grid)
            if button.name == 'play/pause_anim':
                try:
                    if self.desk.playing:
                        icon(button.x,button.y,img=0,asset_name='pause')
                    else:
                        icon(button.x,button.y,img=0,asset_name='play')
                except:
                    pass

            if button.name == 'zoom_out':
                pyxel.text(button.x + 5,button.y - 7,'Zoom',col=self.desk.bg_color-1)

            if button.name == 'speed_down':
                pyxel.text(button.x + 3,button.y - 7,'Speed',col=self.desk.bg_color-1)

    def draw_mouse_pos(self):
        pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(pyxel.mouse_x)+','+str(pyxel.mouse_y),15)
        #pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(self.desk.draw_area.mpos_on_canvas_x)+','+str(self.desk.draw_area.mpos_on_canvas_y),15)

    def switch_desk_gestion(self):
        if self.desk.switch != {}:
            self.button_list = []
            argument = self.desk.switch['argument']
            if self.desk.switch['to'] == 'folders':
                self.desk = folders_desk(self.button_list)
                
            elif self.desk.switch['to'] == 'drawing':
                if 'file_canvas' in argument['file_info'].keys():
                    self.desk = draw_desk(self.button_list,argument['file_info'])
                else:
                    self.desk = load_desk(self.button_list,argument['file_info'],self.desk.switch['to'])

            self.desk.switch = {}

    def desk_msg_update(self):
        if self.desk.msg['time'] > 0:
            if on_tick(120):
                self.desk.msg['time'] += -1      


class example_desk:
    def __init__(self,button_list):
        self.switch = {}
        self.can_save = False
        self.msg = {'txt':'','time':0}
        self.button_list = button_list
        self.bg_color = 6
    def update(self):
        pass
    def draw(self):
        pass
    def draw_over(self):
        pass
    def quick_save(self):
        pass


class folders_desk:
    def __init__(self,button_list,argument={'menu':'open'}):
        self.switch = {}
        self.can_save = False
        self.button_list = button_list
        self.argument = argument
        self.text_zone = text_zone(x=10,y=10,length=20)
        self.file_info = {'file_path':'','file_data':{},'file_pyxres_name':'','file_index':0}
        self.open_to = 'drawing'
        
        self.bg_color = 6
        self.msg = {'txt':'','time':0}
    
    def update(self):
        self.text_zone.update()
        
        if self.text_zone.enter:
            self.open_file()
            self.text_zone.enter = False
  

    def draw(self):
        pyxel.cls(self.bg_color)
        self.text_zone.draw()
        if self.msg['time'] > 0:
            pyxel.text(self.text_zone.x,self.text_zone.y + 8,self.msg['txt'],8)

    def draw_over(self):
        pass
    
    def open_file(self):

        extension_add = ['', '.pyxres', '.toml']

        found = False
        for extension in extension_add:
            if not found:
                try:
                    file = toml.load(self.text_zone.text + extension)
                except:
                    try:
                        file = zipfile.ZipFile(self.text_zone.text + extension)
                    except:
                        pass
                    else:
                        found = True
                        file.extractall()
                        file.close()
                        self.file_info['file_path'] = 'pyxel_resource.toml'
                        self.file_info['file_pyxres_name'] = self.text_zone.text + extension
                        print(self.text_zone.text + extension)
                else:
                    found = True 
                    self.file_info['file_path'] = self.text_zone.text + extension
                print('try')

        if not found:
            self.msg = {'txt':'Wrong file name','time': 4}
        else:
            self.switch = {'to':self.open_to, 'argument':{'file_info':self.file_info}}
            print('end')

        
    def quick_save(self):
        pass


class load_desk:
    def __init__(self,button_list,file_info,next_desk):
        self.switch = {}
        self.button_list = button_list
        self.can_save = False
        self.msg = {'txt':'','time':0}
        self.file_info = file_info #{'file_path':'','file_data':{},'file_pyxres_name':'','file_index':0}
        self.file_data = toml.load(file_info['file_path'])
        self.next_desk = next_desk
        self.selected_save = 0
        self.bg_color = 6

        
        self.nb_saves = len(self.file_data['images'])
        self.ecart = 10
        if self.nb_saves == 1:
            self.ecart = 0
        else:
            self.ecart = 75//(self.nb_saves-1)
        for i in range(self.nb_saves):
            if self.file_data['images'][i]['data'] == [[0]]:
                self.file_data['images'][i]['data'] = BASE_CANVAS
            
            self.button_list.append(Button(name='save '+str(i),color=2,x=10,y=15 + self.ecart*i,width=30,height=10))
            self.button_list.append(Button(name='preview '+str(i), color=0, x=10 + 40, y=15 + self.ecart*i, width=self.ecart-10, height=self.ecart-10))

    def update(self):

        for button in self.button_list:
            if button.pressed:
                self.selected_save = int(button.name[-1:])

        if pyxel.btnp(pyxel.KEY_DOWN) and self.selected_save < len(self.file_data['images'])-1:
            self.selected_save += 1
        if pyxel.btnp(pyxel.KEY_UP) and self.selected_save > 0:
            self.selected_save += -1

        
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.file_info['file_index'] = self.selected_save
            self.save_canvas()
            self.switch = {'to':self.next_desk,'argument':{'file_info':self.file_info}}
    
    def draw(self):
        pyxel.cls(self.bg_color)
        if self.file_info['file_pyxres_name'] != '':
            text = self.file_info['file_pyxres_name']
        else:
            text = self.file_info['file_path']
        
        pyxel.text(64-2*len(text),4,text,0)
    
    def draw_preview(self,index,x,y,w,h):
        canvas = self.file_data['images'][index]['data']
        for in_y in range(h):
            for in_x in range(w):
                try:
                    pyxel.pset(x + in_x, y + in_y, canvas[in_y][in_x])
                except:
                    pyxel.pset(x + in_x, y + in_y, 0)
    



    def draw_over(self):
        self.draw_button_name()
        self.draw_button_highlight()

        for button in self.button_list:
            if button.name[:7] != 'preview':
                self.draw_preview(int(button.name[-1]), button.x + 40, button.y, self.ecart-10, self.ecart-10)

    def draw_button_name(self):
        for button in self.button_list:
            if button.name[:7] != 'preview':
                pyxel.text(button.x + 1, button.y + 1, button.name, 9)
    
    def draw_button_highlight(self):
        for button in self.button_list:
            if int(button.name[-1:]) == self.selected_save:
                draw_rectangle(button.x, button.y, button.width-1, button.height-1)
            
    
    def save_canvas(self):
        self.file_info['file_canvas'] = self.file_data['images'][self.selected_save]['data']

    def quick_save(self):
        pass



class draw_desk:
    def __init__(self,button_list,file_info={'file_path':'save.toml','file_canvas':None}):
        self.switch = {}
        self.button_list = button_list
        self.can_save = True
        self.parameters_pos = {'colorpick':(4,113),'zoom':(64,116),'grid':(95,116)}
        self.file_info = file_info
        self.file_data = toml.load(self.file_info['file_path'])

        if file_info['file_canvas'] != None or file_info['file_canvas'] == [[0]]:
            self.starting_canvas = file_info['file_canvas']
        else:
            self.starting_canvas = BASE_CANVAS
            self.find_save()
        self.draw_area = DrawArea(1,1,125,102,self.starting_canvas,self.parameters_pos,button_list)
        self.bg_color = 6
        self.msg = {'txt':'','time':0}
    
    def update(self):
        self.draw_area.update()
        
    def draw(self):
        pyxel.cls(6)

        self.draw_area.draw()

        if self.msg['time'] > 0:
            pyxel.text(102,105,self.msg['txt'],1)
    
    def draw_over(self):
        self.draw_area.draw_over()


    def quick_save(self):
        self.file_data['images'][self.file_info['file_index']]['data'] = self.draw_area.canvas
        file = open(self.file_info['file_path'],'w')
        toml.dump(self.file_data,file)
        file.close()
        if self.file_info['file_pyxres_name'] != '':
            zip = zipfile.ZipFile(self.file_info['file_pyxres_name'],'w')
            zip.write(self.file_info['file_path'])
            zip.close()
 
    def find_save(self):
        if not 'file_index' in self.file_info.keys():
            for i in range(len(self.file_data['images'])):
                if self.file_data['images'][i]['data'] == [[0]]:
                    self.file_info['file_index'] = i
        if not 'file_index' in self.file_info.keys():
            self.file_data['images'].append({'width': 256, 'height': 256, 'imgsrc': 0, 'data': BASE_CANVAS})
            self.file_info['file_index'] = len(self.file_data['images']) - 1
        

class animation_desk:
    def __init__(self,button_list,file_info={'file_path':'save.toml','file_canvas':None}):
        self.switch = {}
        self.button_list = button_list
        self.starting_canvas = BASE_CANVAS
        self.parameters_pos = {'colorpick':(4,113),'zoom':(101,28),'grid':(101,3)}
        self.file_info = file_info
        
        if file_info['file_canvas'] != None or file_info['file_canvas'] == [[0]]:
            self.starting_canvas = file_info['file_canvas']
        else:
            self.starting_canvas = BASE_CANVAS
        self.draw_area = DrawArea(1,1,95,95,self.starting_canvas,self.parameters_pos,button_list)

        self.playing = False
        self.start_frame = 0
        self.animation = []
        self.framerate = 10
        self.frames = [{'all_canvas':copy.deepcopy(self.draw_area.past_canvas),'index':0,'coming_back':False}]
        self.frames_index = 0

        self.button_list.append(Button(name='last_frame',color=5,x=26,y=100,width=10,height=10,icon='arrow_left'))
        self.button_list.append(Button('play/pause_anim',5,40,100,10,10,'pause/play'))
        self.button_list.append(Button('next_frame',5,54,100,10,10,'arrow_right'))
        self.button_list.append(Button('speed_down',5,101,48,10,10,'minus'))
        self.button_list.append(Button('speed_up',5,116,48,10,10,'plus'))
        self.base_canvas = copy.deepcopy(self.frames[0]['all_canvas'])
        self.bg_color = 7

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
        if is_pressed(self.button_list,'speed_down'):
            self.framerate += 2
        if is_pressed(self.button_list,'speed_up'):
            self.framerate -= 2
        
        
        if self.framerate <= 0:
            self.framerate = 1
        if self.framerate > 180:
            self.framerate = 180

    def draw(self):
        pyxel.cls(7)

        self.draw_area.draw()
    
    def draw_over(self):
        self.draw_area.draw_over()


class button_maker_desk:
    def __init__(self,button_list):
        self.button_list = button_list
        self.maker_mode = False
        self.colorpick = ColorPick(button_list,x=72,y=2)
        self.currently_drawing = 'N/A'
        self.switch = {}

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

    def quick_save(self):
        pass


class DrawArea:
    def __init__(self,x,y,width,height,canvas,parameters_pos,button_list,grid_color=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_list = button_list
        self.grid_color = grid_color
        self.canvas = canvas
        self.canvas_width = 256
        self.canvas_height = 256
        self.canvas = canvas_size_fix(self.canvas)

        self.colorpick = ColorPick(button_list, parameters_pos['colorpick'][0], parameters_pos['colorpick'][1])
        self.color = 0
        self.zoom = 5
        self.button_list.append(Button('zoom_out',5, parameters_pos['zoom'][0], parameters_pos['zoom'][1],10,10,'minus'))
        self.button_list.append(Button('zoom_in',5, parameters_pos['zoom'][0] + 15, parameters_pos['zoom'][1],10,10,'plus'))
        self.button_list.append(Button('grid_on/off',5,parameters_pos['grid'][0],parameters_pos['grid'][1],10,10,'grid/crossed'))
        self.grid = True
        self.grid_size = 8
        self.canvas_hold_pos = (0,0)
        self.cam = [0,0]
        self.slide_holding = False

        self.past_canvas = [copy.deepcopy(self.canvas)]
        self.canvas_index = 0
        self.change_canvas = False
        self.coming_back = False

        self.tool = 'brush'
        self.pencil_pos = (0,0) #position on the canvas
        self.last_pencil_pos = (0,0)
        self.select_start = (0,0)
        self.select_zone = {'x':0, 'y':0,'w':0,'h':0,'content':[]}
        self.select_holding = False
        self.lclick = False
        self.last_lclick = False
    
    def update(self):

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
                        self.brush_stroke()

            elif self.tool == 'select':
                self.set_select_zone()
            
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

            if not pyxel.btn(pyxel.KEY_LCTRL):
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
        
        self.parameters_gestion()
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
                            try:
                                pyxel.pset(posx, posy, self.canvas[self.cam[1] + y][self.cam[0] + x])
                            except:
                                pyxel.pset(posx, posy, 0)


        if self.grid:
            for x in range(1,self.canvas_width//self.grid_size+1):
                xpos = self.x + (self.grid_size * x - self.cam[0]) * self.zoom
                if xpos >= self.x and xpos < self.x + self.width:
                    y_endline = self.y + min(self.height,(self.canvas_height-self.cam[1])*self.zoom-1)
                    if xpos < self.canvas_width*self.zoom and xpos < self.width:
                        pyxel.line(xpos, self.y, xpos, y_endline, self.grid_color)

            for y in range(1,self.canvas_height//self.grid_size+1):
                ypos = self.y + (self.grid_size * y - self.cam[1]) * self.zoom
                if ypos >= self.y and ypos < self.y + self.height:
                    x_endline = self.x + min(self.width,(self.canvas_width-self.cam[0])*self.zoom-1)
                    if ypos < self.canvas_height*self.zoom and ypos < self.height:
                        pyxel.line(self.x, ypos, x_endline, ypos, self.grid_color)                                    #starf :(
        
        
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

    def draw_over(self):
        if mouse_inside(self.x,self.y,self.width,self.height):
            pyxel.text(pyxel.mouse_x,pyxel.mouse_y+10,str(self.pencil_pos[0])+','+str(self.pencil_pos[1]),15)


    def canvas_pos(self,pos=(0,0)):
        return( (pos[0] - self.x) // self.zoom + self.cam[0],
                (pos[1] - self.y) // self.zoom + self.cam[1]
        )
    
    def paint(self,pos,color):
        if pos[1] < self.canvas_height and pos[0] < self.canvas_width:
            self.canvas[pos[1]][pos[0]] = color

    def brush_stroke(self):
        line_from_last_pos = pos_line(self.last_pencil_pos[0],self.last_pencil_pos[1],self.pencil_pos[0],self.pencil_pos[1])
        for pos in line_from_last_pos:
            self.paint(pos,self.color)

    def slide_canvas_gestion(self):
            if (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.btn(pyxel.KEY_SPACE)) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
                if not self.slide_holding:
                    self.canvas_hold_pos = (pyxel.mouse_x + self.cam[0] * self.zoom, pyxel.mouse_y + self.cam[1] * self.zoom)
                else:
                    self.cam = [(self.canvas_hold_pos[0] - pyxel.mouse_x) // self.zoom, 
                                (self.canvas_hold_pos[1] - pyxel.mouse_y) // self.zoom]

                    if self.cam[0]<0:
                        self.cam[0] = 0
                    if self.cam[0] > self.canvas_width - 4:
                        self.cam[0] = self.canvas_width - 4
                    if self.cam[1] < 0:
                        self.cam[1] = 0
                    if self.cam[1] > self.canvas_height - 4:
                        self.cam[1] = self.canvas_height - 4

                self.slide_holding = True
            else:
                self.slide_holding = False


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


    def set_select_zone(self):
        if self.lclick: 
            if not self.select_holding: #first click
                self.select_start = copy.deepcopy(self.pencil_pos)
                self.select_holding = True
            else:
                self.select_zone['x'], self.select_zone['y'] = copy.deepcopy(self.select_start)
                self.select_zone['w'], self.select_zone['h'] = self.pencil_pos[0] - self.select_start[0], self.pencil_pos[1] - self.select_start[1]
        else:
            self.select_holding = False 

    def copy_select(self):
        self.select_zone['content'] = [[0 for X in range(self.select_zone['w']+1)] for Y in range(self.select_zone['h']+1)]
        for y in range(self.select_zone['h']+1):
            for x in range(self.select_zone['w']+1):
                self.select_zone['content'][y][x] = self.canvas[self.select_zone['y'] + y][self.select_zone['x'] + x]

    def paste_select(self):
        for y in range(len(self.select_zone['content'])):
            if self.select_zone['y'] + y < self.canvas_height:
                for x in range(len(self.select_zone['content'][0])):
                    if self.select_zone['x'] + x < self.canvas_width:
                        self.canvas[self.select_zone['y'] + y][self.select_zone['x'] + x] = self.select_zone['content'][y][x]

    def delete_select(self):
        for y in range(self.select_zone['h']+1):
            for x in range(self.select_zone['w']+1):
                self.canvas[self.select_zone['y'] + y][self.select_zone['x'] + x] = 0

    def inverse_v(self):
        self.copy_select()
        temp = []
        for row in self.select_zone['content']:
            temp.insert(0,row)
        self.select_zone['content'] = temp
        self.paste_select()

    def inverse_h(self):
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


    def parameters_gestion(self):
        if is_pressed(self.button_list,'zoom_out'):
            self.zoom += -1
        if is_pressed(self.button_list,'zoom_in'):
            self.zoom += 1
        if is_pressed(self.button_list,'grid_on/off'):
            self.grid = not self.grid

        self.colorpick.update()

    def apply_limits(self): 
        if self.zoom <= 0:
            self.zoom = 1
        if self.zoom >= 6:
            self.zoom = 5

        if self.select_zone['w'] < 7//self.zoom:
            self.select_zone['w'] = 7//self.zoom
        if self.select_zone['h'] < 7//self.zoom:
            self.select_zone['h'] = 7//self.zoom


        if self.select_zone['x'] + 7//self.zoom > self.canvas_width-1:
            self.select_zone['x'] = self.canvas_width-1 - 7//self.zoom
            self.select_start = (self.canvas_width-1 - 7//self.zoom, self.select_start[1])
            self.select_zone['w'] = 7//self.zoom

        if self.select_zone['y'] + 7//self.zoom > self.canvas_height-1:
            self.select_zone['y'] = self.canvas_height-1 - 7//self.zoom
            self.select_start = (self.select_start[0], self.canvas_height-1 - 7//self.zoom)
            self.select_zone['h'] = 7//self.zoom


        if self.select_zone['x'] + self.select_zone['w'] > self.canvas_width-1:
            self.select_zone['w'] = self.canvas_width-1 - self.select_zone['x']

        if self.select_zone['y'] + self.select_zone['h'] > self.canvas_height-1:
            self.select_zone['h'] = self.canvas_height-1 - self.select_zone['y']


class text_zone:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.text = ''
        self.current_key = ''
        self.enter = False

    def update(self):
        self.current_key = ''
        for letter in LETTERS:
            if pyxel.btnp(getattr(pyxel,'KEY_'+letter)):
                if pyxel.btn(pyxel.KEY_SHIFT):
                    self.current_key = letter
                else:
                    self.current_key = letter.lower()

        for i in range(len(PONC_PYXEL)):
            if pyxel.btnp(getattr(pyxel,'KEY_'+PONC_PYXEL[i])):
                if pyxel.btn(pyxel.KEY_SHIFT):
                    self.current_key = PONC_SHIFT[i]
                elif pyxel.btn(pyxel.KEY_RALT):
                    self.current_key = PONC_ALT[i]
                
                else:
                    self.current_key = PONCTUATION[i]
        
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.text = self.text[:-1]
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.enter = True

        if len(self.text) < self.length:
            self.text += self.current_key

    def draw(self):
        pyxel.rect(self.x,self.y,self.length*4 + 1,7,0)
        pyxel.text(self.x+1,self.y+1,self.text,9)

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

def rect_in_list(x, y, w, h): 
    all_pos = []
    for in_y in range(h):
        for in_x in range(w):
            all_pos.append((x+in_x,y+in_y))
    return all_pos

def is_canvas(canvas):
    if not type(canvas) is list:
        return False
    else:
        for row in canvas:
            if not type(row) is list:
                return False
            else:
                for color in row:
                    if not type(color) is int:
                        return False
    return True

def draw_rectangle(x,y,w,h,col=7):
    pyxel.line(x, y, x + w, y, col)
    pyxel.line(x, y, x, y + h, col)
    pyxel.line(x, y + h, x + w, y + h, col)
    pyxel.line(x + w, y, x + w, y + h, col)

def canvas_max_width(canvas):
    max = 0
    for line in canvas:
        if len(line) > max:
            max = len(line)
    return max

def canvas_fix(canvas,width):
    new_canvas = canvas
    for y in range(len(canvas)):
        if len(canvas[y]) < width:
            missing_x = width - len(canvas[y])
            for x in range(missing_x):
                new_canvas[y].append(canvas[y][-1])
    return new_canvas

def canvas_size_fix(canvas):
    new_canvas = canvas
    if len(canvas) < 256:
        missing_y = 256 - len(canvas)
        for x in range(missing_y):
            new_canvas.append([0 for x in range(256)])

    for y in range(len(canvas)):
        if len(canvas[y]) < 256:
            missing_x = 256 - len(canvas[y])
            for x in range(missing_x):
                new_canvas[y].append(canvas[y][-1])
    return new_canvas

App()