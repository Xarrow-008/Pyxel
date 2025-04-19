import os # BEFORE ASYNC TESTS --AFTER-- ASYNC IS SHIT WITH THIS COUNT W 30frames/s

import pyxel #ça marche alélouia
from objects import Objects
from player import *
from world import *

class App:
    direction = [0,0]
    frame = 0
    timer = 0
    tickrate = 0.1
    walking_switch=False
    walking = False
    SLASH = {'x':0,'y':0,'placement+':[1,0],'ing':False,'playerStop':False,'directionX':0,'directionY':8,'moment':0,'frameHit':-60}
    #L'emplacement x+ y+ par rapport au joueur de où va etre placé le slash
    #Determine la direction du slash depuis les sprites de mygame                --à regarder-- pyxel edit mygame
    #determine l'étape a laquelle le slash est depuis les sprites de mygame (en gros ca fait un tableau entre la direction et l'etape dedans)


    def __init__(self):
        os.system('cls')
        pyxel.init(CAMERA_WIDTH,CAMERA_HEIGHT,title='AmogusKiller')
        pyxel.load('../mygame.pyxres')

        self.world = World(pyxel.tilemap(0))

        self.player = Player(self.world)

        self.objects = Objects()

        pyxel.run(self.update, self.draw) #ok mb ca carry tout banger ca prend que update et draw
    
    def update(self):
        
        facing = self.direction

        self.frame+=1

        if self.movement_keys_pressed() and not self.SLASH['playerStop']:
            self.walking = True
            if self.on_tick(self.tickrate):
                self.walking_switch = not self.walking_switch
        else:
            self.walking = False

        if self.walking_switch:
            facing[1] = 3
        else:
            facing[1] = 2
        if not self.walking:
            facing[1] = 4

        if not self.SLASH['playerStop']:

            self.player.update(facing)

            facing = self.player.facing

        
        if pyxel.btn(pyxel.KEY_SPACE):
            if not self.SLASH['ing']:
                self.SLASH['frameHit'] = self.frame
                self.SLASH['ing'] = True
                self.SLASH['placement+'] = self.facing_to_direction(facing)
                self.SLASH['directionX'] = facing[0]
                self.SLASH['x'] = self.player.x + self.SLASH['placement+'][0] * TILE_SIZE
                self.SLASH['y'] = self.player.y + self.SLASH['placement+'][1] * TILE_SIZE
                self.SLASH['playerStop'] = True
            
            
            for obj in self.objects.OBJs:
                if sprites_collide(obj['x'], obj['y'], self.SLASH['x'], self.SLASH['y']) and not obj['dead'] and not self.frame - obj['frameHit'] < 15:
                    obj['frameHit'] = self.frame
                    obj['hit'] += 1
                    if obj['hp'] - obj['hit'] <= 0:
                        obj['dead'] = True
                        obj['deathAnim'] = True
                    else:
                        obj['hitAnim'] = True



        if pyxel.btn(pyxel.KEY_R):
            self.reset()


        
        if self.SLASH['ing']:
            self.easy_frames_event([
            [True,[[self.SLASH,'moment',0]],0],
            [True,[[self.SLASH,'moment',1]],3], #at frame 3 of slash, change SLASH['moment'] to 1
            [True,[[self.SLASH,'playerStop',False]],6],
            [True,[[self.SLASH,'moment',2]],10],
            [True,[[self.SLASH,'moment',3]],12],
            [True,[[self.SLASH,'moment',0],[self.SLASH,'ing',False]],15]
            ],self.SLASH['frameHit'])
        
        for obj in self.objects.OBJs:
            if obj['deathAnim'] or obj['hitAnim']:
                if obj['name'] == 'lamp':
                    self.easy_frames_event([
                [obj['hitAnim'],[[obj,'v',obj['v']+1]],0],
                [True,[[obj,'moment',0]],0],
                [True,[[obj,'moment',1]],1],
                [True,[[obj,'moment',2]],6],
                [True,[[obj,'moment',3]],7],
                [True,[[obj,'moment',4]],8],
                [True,[[obj,'moment',5]],9],
                [True,[[obj,'moment',6]],10],
                [obj['hitAnim'],[[obj,'v',obj['v']-1],[obj,'moment',0]],11],
                [obj['deathAnim'],[[obj,'moment',7]],11],
                [True,[[obj,'deathAnim',False],[obj,'hitAnim',False]],11]
                ],obj['frameHit'])

                if obj['name'] == 'ghost':
                    self.easy_frames_event([
                [True,[[obj,'x',obj['x']-1],[obj,'v',15],[obj,'moment',0]],0],
                [True,[[obj,'x',obj['x']-1]],2],
                [True,[[obj,'x',obj['x']-1]],4],
                [True,[[obj,'x',obj['x']-1]],7],
                [obj['deathAnim'],[[obj,'moment',1]],10],
                [obj['deathAnim'],[[obj,'moment',2]],14],
                [obj['deathAnim'],[[obj,'moment',3]],18],
                [obj['deathAnim'],[[obj,'deathAnim',False],[obj,'dead',True]],19],
                [obj['hitAnim'],[[obj,'x',obj['x']+1],[obj,'hitAnim',False],[obj,'v',14]],8],
                ],obj['frameHit'])

                    if obj['dead'] and not obj['deathAnim']:
                        self.objects.OBJs.remove(obj)

        
        self.player.camera_movement(self.world.cameraPos, 1/8)
        

        if self.objects.OBJs[0]['deathAnim']:
            self.world.place_blocks(18,11,3,3,WorldItem.GRASS_AIR)


        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        self.direction = facing

    def draw(self):
        pyxel.cls(0)
        #print(self.world.cameraPos[0])
        pyxel.camera(self.world.cameraPos[0],self.world.cameraPos[1])

        AIR_LIST = [] #--ATTENTION-- On ne voit pas la différence entre blocs air et non air que jai mis dans l'editeur
        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                world_item = self.world.world_map[y][x]
                if world_item[1] >= 6 and world_item != (1,7): #Si c'est un bloc transparent
                    AIR_LIST.append([x,y,world_item]) #Mettre dans la list qui se dessine apres le joueur(par dessus)
                else:
                    world_item_draw(pyxel, x, y, world_item) #Sinon dessiner car derriere joueur
        
    
        for obj in self.objects.OBJs:
            pyxel.blt(
                obj['x'],
                obj['y'],
                self.player.IMG,
                obj['moment'] * TILE_SIZE,
                obj['v'] * TILE_SIZE,
                self.player.WIDTH,
                self.player.HEIGHT,
                colkey=15)

        
        pyxel.blt(  #dessiner joueur
            self.player.x,
            self.player.y,
            self.player.IMG,
            self.direction[0] * TILE_SIZE,
            self.direction[1] * TILE_SIZE,
            self.player.WIDTH,
            self.player.HEIGHT,
            colkey=0)

        
        for i in AIR_LIST: #liste de blocs au dessus du joueur
            world_item_draw(pyxel, i[0], i[1], i[2])
        
        if self.SLASH['ing']:
            pyxel.blt(  #dessiner slash
                self.SLASH['x'],
                self.SLASH['y'],
                self.player.IMG,
                self.SLASH['directionX'] * TILE_SIZE,
                (self.SLASH['directionY'] + self.SLASH['moment']) * TILE_SIZE,
                self.player.WIDTH,
                self.player.HEIGHT,
                colkey=11)
    
    def on_tick(self, tickrate = 0.5):
        if self.frame % (30 * tickrate) == 0:
            return True
        return False
    
    def movement_keys_pressed(self):
        if (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D)
            or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S)):
            return True
        else:
            return False
    
    def facing_to_direction(self,facing):
        if facing[0] == 0:
            return [1,0]
        if facing[0] == 1:
            return [-1,0]
        if facing[0] == 2:
            return [0,-1]
        if facing[0] == 3:
            return [0,1]
        if facing[0] == 4:
            return [1,-1]
        if facing[0] == 5:
            return [-1,-1]
        if facing[0] == 6:
            return [1,1]
        if facing[0] == 7:
            return [-1,1]

    def reset(self):
        for obj in self.objects.OBJs:
            obj['dead'] = False
            obj['moment'] = 0
            obj['hit'] = 0
            obj['frameHit'] = 0

    
    def easy_frames_event(self,tab,event_start): #tab sous la forme de [[condition1 and/or condition2,[action1(=list,value),action2...],à tel frames],...] et ca ecrit les if a ta place
        for event in tab:
            if event[0] and self.frame - event_start == event[2]:
                for action in event[1]: #event[1] = toutes les actions
                    action[0][action[1]] = action[2] # :Dans la liste des valeurs à changer, à l'index du num a sa droite, :Mettre la valeur a la fin 




App()