import pyxel, os, random, math, csv

WIDTH = 256
HEIGHT = 256
TILE_SIZE = 8

CAM_WIDTH = 16*8
CAM_HEIGHT = 16*8

FPS = 120

loadedEntities = []

class App: #Puts EVERYTHING together
    def __init__(self):
        os.system('cls')
        pyxel.init(CAM_WIDTH,CAM_HEIGHT,title='Not a Scrap', fps=FPS)
        pyxel.load('../notAScrap_8by8.pyxres')

        self.save = import_csv("save.csv")

        self.world = World(pyxel.tilemaps[0],RoomBuild(0,WIDTH//2,10),'ship',-1)
        self.rooms = self.world.roombuild.rooms
        self.camera = Camera()
        self.itemList = ItemList()
        self.info = Info()
        self.player = Player(self)
        self.effects = ScreenEffect(self.player)
        self.anim = Animation()
        
        

        self.game_state = 'start'
        
        pyxel.mouse(True)

        pyxel.run(self.update,self.draw)
    

    def update(self):
        self.camera.update(self.player)
        if self.game_state == "start":
            self.update_in_start()
        elif self.game_state == 'bunker':
            self.update_in_bunker()
        elif self.game_state == 'ship':
            self.update_in_ship()
        elif self.game_state == "death":
            self.update_death()
    
    def draw(self):
        pyxel.cls(0)
        if self.game_state == "start":
            self.draw_start_screen()

        elif self.game_state == 'bunker':
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if in_camera(x,y,self.camera.x,self.camera.y):
                        block = self.world.world_map[y][x]
                        world_item_draw(pyxel,x,y,block)
            
            pyxel.blt(WIDTH*TILE_SIZE//2 - TILE_SIZE//2,4*TILE_SIZE,1,72,0,5*TILE_SIZE,4*TILE_SIZE,colkey=11,scale=2)

            self.draw_entities()
            self.draw_player()
            self.draw_effects()
            self.draw_screen_effects()
            self.draw_stats()
            self.draw_description()
            self.draw_timer_bar()

        elif self.game_state == 'ship':
            self.draw_ship_outside()
            self.draw_ship()
            self.draw_player()
            self.draw_description()

        elif self.game_state == "death":
            self.draw_death()
    
    def draw_start_screen(self):
        pyxel.text(self.camera.x, self.camera.y, "Press [Enter] to start the game", 1)
        pyxel.text(self.camera.x, self.camera.y+20, "Press [F1] to reset save file", 1)

    def draw_death(self):
        pyxel.text(self.camera.x,self.camera.y, "You died. Press [Enter] to try again", 1)
        pyxel.text(self.camera.x,self.camera.y+20, "Press [Escape] to quit", 1)
        
        if self.bunkers_highscore_this_run:
            pyxel.text(self.camera.x,self.camera.y+30, "Bunkers explored : "+str(self.bunkers_explored)+" (New Highscore !)", 1)
        else:
            pyxel.text(self.camera.x,self.camera.y+30, "Bunkers explored : "+str(self.bunkers_explored)+" (Highscore : "+str(self.save[0]["bunkers_highscore"]+")"), 1)
        
        if self.kills_highscore_this_run:
            pyxel.text(self.camera.x,self.camera.y+40, "Enemies killed : "+str(self.player.enemiesKilled)+" (New Highscore !)", 1)
        else:
            pyxel.text(self.camera.x,self.camera.y+40, "Enemies killed : "+str(self.player.enemiesKilled)+" (Highscore : "+str(self.save[0]["kills_highscore"]+")"), 1)
        
        if self.items_highscore_this_run:
            pyxel.text(self.camera.x,self.camera.y+50, "Items picked up : "+str(self.player.itemsPickedUp)+" (New Highscore !)", 1)
        else:
            pyxel.text(self.camera.x,self.camera.y+50, "Items picked up : "+str(self.player.itemsPickedUp)+" (Highscore : "+str(self.save[0]["items_highscore"]+")"), 1)
    
    def draw_entities(self):
        for entity in loadedEntities:
            if in_camera(entity.x//TILE_SIZE,entity.y//TILE_SIZE,self.camera.x,self.camera.y):
                pyxel.blt(entity.x,
                        entity.y,
                        0,
                        entity.image[0],
                        entity.image[1],
                        entity.width,
                        entity.height,
                        colkey=11,
                        scale=entity.scale)
    
    def draw_player(self):
        pyxel.blt(
            self.player.x,
            self.player.y,
            0,
            self.player.image[0]*TILE_SIZE,
            self.player.image[1]*TILE_SIZE,
            self.player.width,
            self.player.height,
            colkey=11
        )

    def draw_effects(self):
        for slash in self.world.effects:
            pyxel.blt(
                slash['x'],
                slash['y'],
                0,
                slash['image'][0]*TILE_SIZE,
                slash['image'][1]*TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
                colkey=11,
                scale=slash['scale']
            )

    def draw_screen_effects(self):
        if self.effects.redscreen:
            pyxel.dither(self.effects.red_dither)
            draw_screen(
                0,
                16,
                self.camera.x,
                self.camera.y)
        if self.game_state == 'bunker' and self.effects.explo_screen:
            pyxel.dither(self.effects.explo_dither)
            draw_screen(
                0,
                48,
                self.camera.x,
                self.camera.y
            )
            
        pyxel.dither(1)

    def draw_timer_bar(self):
        pyxel.blt(self.camera.x + 96,self.camera.y,1,0,32,32,4)
        pyxel.blt(self.camera.x + 96,self.camera.y,1,0,36,self.explosion_bar+1,4)
        if self.enemy_bar>0:
            pyxel.blt(self.camera.x + 96,self.camera.y,1,0,40,self.enemy_bar+1,4)

    def draw_stats(self):
        pyxel.text(self.camera.x+1, self.camera.y+1, "Health:"+str(self.player.health)+"/"+str(self.player.max_health),8)
        pyxel.text(self.camera.x+1, self.camera.y+7, "Weapon:"+str(self.player.gun["name"]),7)
        pyxel.text(self.camera.x+1, self.camera.y+13, "Ammo:"+str(self.player.gun["mag_ammo"])+"/"+str(self.player.gun["max_ammo"])+" ("+str(self.player.gun["reserve_ammo"])+")",7)
        pyxel.text(self.camera.x+96, self.camera.y+8, "Fuel:"+str(self.player.fuel),7)
        if self.player.gun["mag_ammo"] < self.player.gun["max_ammo"] and self.player.gun["reserve_ammo"]>0:
            pyxel.text(self.camera.x+1, self.camera.y+19, "[R] to reload", 7)

    def draw_description(self):
        if self.info.description != ["N/A"]:
            pyxel.text(self.camera.x+1, self.camera.y+107, self.info.description[0], 7)
            pyxel.text(self.camera.x+1, self.camera.y+113, self.info.description[1], 7)
            pyxel.text(self.camera.x+1, self.camera.y+119, self.info.description[2], 7)

    def draw_ship_outside(self):
        waves = (math.cos(pyxel.frame_count/50)+1)/2
        pyxel.dither(waves/2+0.3125)
        draw_screen(16,16,0,-32)
        for i in range(len(self.anim.slide)):
            pyxel.dither(waves/2+0.3125)
            pyxel.blt(
                self.anim.slide_pos + i*8,
                105,
                0,
                self.anim.slide[i][0]*8,
                self.anim.slide[i][1]*8,
                8,
                8
                )
            pyxel.dither(1)
            pyxel.blt(
                self.anim.slide_pos + i*8,
                112,
                0,
                WorldItem.WALL[0],
                WorldItem.WALL[1],
                8,
                8
                )
            pyxel.blt(
                self.anim.slide_pos + i*8,
                120,
                0,
                WorldItem.WALL[0],
                WorldItem.WALL[1],
                8,
                8
                )
        pyxel.dither(1)
    
    def draw_ship(self):
        pyxel.blt(40,55,1,32,0,5*TILE_SIZE,3*TILE_SIZE,colkey=11,scale=2)
        pyxel.blt(
            40,95,1,
            self.anim.image1[0],
            self.anim.image1[1],
            40,
            8,
            scale=2,
            colkey=11
        )

    def enemies_spawn_in_rooms(self):
        margin_spawn = 3
        for room in self.world.roombuild.rooms:
            ideal = (room['name']+1)//2
            if room['name'] <=6:
                nb_enemies = ideal
            else:
                nb_enemies = random.randint(ideal-margin_spawn,ideal+margin_spawn)
            
            for i in range(nb_enemies):
                occupied = True
                for attempt in range(3):
                    if occupied:
                        X_pos = room['X'] + random.randint(0,room['W']-1)
                        Y_pos = room['Y'] + random.randint(0,room['H']-1)
                        if not (check_entity(loadedEntities, 'x', X_pos) and check_entity(loadedEntities, 'y', Y_pos)):
                            occupied = False
                random_enemy = random.randint(0,99)
                for enemy in EnemyTemplates.ENEMY_LIST:
                    if random_enemy in enemy['spawning_chance']:
                        Enemy(self, X_pos*TILE_SIZE,Y_pos*TILE_SIZE,enemy)

    def spawn_enemies_at(self,x,y,dic,always_loaded=False):
        for enemy in EnemyTemplates.ENEMY_LIST:
            if enemy['name'] in dic.keys():
                for i in range(dic[enemy['name']]):
                    Enemy(self, x*TILE_SIZE,y*TILE_SIZE,enemy,always_loaded)

    def update_in_start(self):
        self.camera.x, self.camera.y = 0,0
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.difficulty = 0
            self.bunkers_explored = 0
            self.generateShip()
            self.bunkers_highscore_this_run = False
            self.kills_highscore_this_run = False
            self.items_highscore_this_run = False
        if pyxel.btnp(pyxel.KEY_F1):
            self.resetSaves()

    def update_death(self):
        global activeBoosts
        if pyxel.btnp(pyxel.KEY_RETURN):
            activeBoosts = []
            self.difficulty = 0
            self.bunkers_explored = 0
            self.generateShip()
            self.player.alive = True
            self.player = Player(self)

    def update_in_ship(self):
        self.camera.x,self.camera.y = 0,0
        self.anim.loop(6,10,32,24,[0,1])
        self.anim.slide_anim(10,3,WorldItem.UPWORLD_FLOOR)
        self.player.update_in_ship()
        if self.player.lever_pulled:
            self.game_state = 'bunker'
            self.generateBunker()

    def update_in_bunker(self):
        self.update_effects()
        self.effects.update()

        if self.player.alive:
            self.player.update()
            for entity in loadedEntities:
                entity.update()

            for boost in activeBoosts:
                boost.update()
 
            if on_cooldown(self.game_start,self.ship_hold_time):
                self.enemy_bar =  (self.ship_hold_time-pyxel.frame_count+self.game_start) * 32 // self.ship_hold_time
                
            if not on_cooldown(self.game_start,self.ship_hold_time) and self.group_alive:
                if self.group.room['name'] < self.player.room['name'] - 3:
                    self.group.update()
                else:
                    self.spawn_enemies_at(self.group.room['X'],self.group.room['Y'],self.group.dic_enemies,True)
                    self.group_alive = False
                    

            if self.ship_broken:
                if on_cooldown(self.ship_hold_time+self.game_start,self.explosion_time):
                    self.explosion_bar =  (self.game_start+self.ship_hold_time+self.explosion_time-pyxel.frame_count) * 32 // self.explosion_time

            if self.effects.explo_screen and not on_cooldown(self.effects.explo_frame,120):
                self.player.alive = False
                self.effects.explo_screen = False


            pyxel.camera(self.camera.x,self.camera.y)
            
            if on_tick(60):
                if pyxel.frame_count - self.game_start >= self.ship_hold_time and not self.ship_broken:
                    self.ship_broken = True
                    self.group = EnemyGroup(self, 0,{'spider':7,'hive_queen':1,'stalker':3,'bulwark':1})
                    self.group_alive = True
                    pyxel.playm(1, loop=True)

        else:
            self.game_state = "death"
            self.endOfRun()
                
        if pyxel.frame_count - self.game_start >= self.ship_hold_time:
            self.info.description = ['','Return to SHIP','Explosion incoming']

        if pyxel.frame_count - self.game_start >= self.ship_hold_time + self.explosion_time and self.player.alive:
            if not self.effects.explo_screen:
                if not self.effects.explo_screen:
                    self.effects.explo_frame = pyxel.frame_count
                self.effects.explo_screen = True
                
        self.check_escape()

    def endOfRun(self):
        if self.bunkers_explored > int(self.save[0]["bunkers_highscore"]):
            self.save[0]["bunkers_highscore"] = str(self.bunkers_explored)
            self.bunkers_highscore_this_run = True
        if self.player.enemiesKilled > int(self.save[0]["kills_highscore"]):
            self.save[0]["kills_highscore"] = str(self.player.enemiesKilled)
            self.kills_highscore_this_run = True
        if self.player.itemsPickedUp > int(self.save[0]["items_highscore"]):
            self.save[0]["items_highscore"] = str(self.player.itemsPickedUp)
            self.items_highscore_this_run = True
        export_csv("save.csv", self.save)

    def update_effects(self):
        for slash in self.world.effects:
            if pyxel.frame_count - slash['time'] > 60:
                self.world.effects.remove(slash)

    def check_escape(self):
        if in_perimeter(self.player.x,self.player.y,WIDTH//2*TILE_SIZE+14,40,10):
            if self.player.fuel >= 5+self.difficulty:
                self.info.description = ['[F] to escape','the explosion','']
                if pyxel.btnp(pyxel.KEY_F):
                    self.player.fuel += -5-self.difficulty
                    self.generateShip()
                    self.difficulty += 1
                    self.bunkers_explored += 1
            else:
                self.info.description = ['Needs '+str(5+self.difficulty)+' fuel to start','','']

    def generateShip(self):
        self.game_state = 'ship'
        self.world.__init__(pyxel.tilemaps[0],RoomBuild(0,WIDTH//2,10),'ship',self.difficulty)
        pyxel.playm(2,loop=True)
        self.player.x = 60
        self.player.y = 70
        pyxel.camera(0,0)
        self.camera.x,self.camera.y = 0,0

    def generateBunker(self):
        global pickUpsOnGround
        global loadedEntities
        global activeBoosts
        loadedEntities = []
        pickUpsOnGround = []
        activeBoosts = []

        self.camera.__init__()
        self.world.__init__(pyxel.tilemaps[0],RoomBuild(0,WIDTH//2,10),'bunker',self.difficulty)
        self.itemList.__init__()
        pyxel.playm(0, loop=True)

        self.player.reset(self.world)

        self.effects.__init__(self.player)
        self.game_start = pyxel.frame_count
        self.ship_broken =  False
        self.ship_hold_time = 120*120
        self.explosion_time = 80*120
        self.group_alive = False
        self.game_state = 'bunker'
        self.enemy_bar = 32
        self.explosion_bar = 32
        self.rooms = self.world.roombuild.rooms

        pyxel.mouse(True)
        self.enemies_spawn_in_rooms()

    def resetSaves(self):
        data = [{'bunkers_highscore': '0', 'kills_highscore': '0', 'items_highscore': '0'}]
        export_csv("save.csv", data)
        self.save = import_csv("save.csv")

class Animation: #makes moving things from the pyxres 
    def __init__(self):
        self.image1 = (0,0)
        self.slide  = [random.choice(WorldItem.UPWORLD_FLOOR) for i in range(CAM_WIDTH//TILE_SIZE+1)]
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

class WorldItem: # all blocks needed to make the world
    WALL = (0,0)
    GROUND = (0,1)
    CONNECT = (1,1)
    INVISIBLE = (6,0)

    BLOCKS = [WALL,GROUND]
    WALLS = [WALL,INVISIBLE]
    UPWORLD_FLOOR = [(3,0),(2,1),(3,1)]

class World: #puts together everything to make the world
    def __init__(self,tilemap,roombuild,game_state,difficulty):
        self.tilemap = tilemap
        self.roombuild = roombuild
        self.world_map = [[(0,1) for j in range(WIDTH)] for i in range(HEIGHT)]
        self.nb_rooms = 20
        self.difficulty = difficulty
        self.effects = []
            
        if game_state == 'bunker':
            self.world_map = [[(0,0) for j in range(WIDTH)] for i in range(HEIGHT)]
            self.player_init_posX = WIDTH//2 + 1.5
            self.player_init_posY = 45/TILE_SIZE
            self.roombuild.random_rooms_place(self.world_map,self.nb_rooms+difficulty//2)
            self.world_map = self.roombuild.world_map
            rect_place(self.world_map,0,0,WIDTH,9,(2,0))
            for i in range(WIDTH):
                self.world_map[9][i] = WorldItem.UPWORLD_FLOOR[random.randint(0,len(WorldItem.UPWORLD_FLOOR)-1)]
            rect_place(self.world_map,0,0,1,10,WorldItem.WALL)
            rect_place(self.world_map,WIDTH-1,0,1,10,WorldItem.WALL)
            self.roombuild.spaceship_walls_place()
            self.furniture = Furniture(self.roombuild.rooms)

            for room in self.roombuild.rooms:
                if 'chest' in room.keys():
                    x = room['chest'][0]
                    y = room['chest'][1]
                    self.world_map[y][x] = (4,0)
                    
                if 'recycler' in room.keys():
                    x = room['recycler'][0]
                    y = room['recycler'][1]
                    self.world_map[y][x] = (8,0)


        elif game_state == 'ship':
            self.world_map = [[(0,1) for j in range(WIDTH)] for i in range(HEIGHT)]
            self.player_init_posX = 60/TILE_SIZE
            self.player_init_posY = 56/TILE_SIZE
            rect_place(self.world_map,4,6,7,1,WorldItem.INVISIBLE)
            rect_place(self.world_map,3,6,1,6,WorldItem.INVISIBLE)
            rect_place(self.world_map,11,6,1,6,WorldItem.INVISIBLE)
            rect_place(self.world_map,4,11,7,1,WorldItem.INVISIBLE)

class RoomBuild: #creates random rooms different every time
    def __init__(self, name, startX, startY):
        self.rooms = [{'name':name,'X':startX,'Y':startY,'W':4,'H':4,'connect':(startX,startY),'direction':'down'}]
        self.world_map = []
        self.name = name
        self.x = startX
        self.y = startY
        self.w = 4
        self.h = 4
        self.connect = [0,0]
        self.newX = startX
        self.newY = startY
        self.newW = 4
        self.newH = 4
        self.newConnect = [0,0]
        self.max_size = 5
        self.collide_tolerated = 3
    
    def random_rooms_place(self, world_map, nb_rooms):
        rect_place(world_map,self.x,self.y,self.w,self.h,WorldItem.GROUND)
        self.last_placement = 'N/A'
        for i in range(nb_rooms):

            self.newW = random.randint(2,self.max_size)*2
            self.newH = random.randint(2,self.max_size)*2

            if self.last_placement == 'down':
                self.room_pos = random.randint(0,2)
                if self.room_pos == 0 and self.x>self.max_size*2+1:
                    self.room_place_left()
                else:
                    self.room_place_right()

                if self.room_pos == 1 and self.x<WIDTH-self.max_size*2+1:
                    self.room_place_right()
                else:
                    self.room_place_left()

                if self.room_pos == 2:
                    self.room_place_down()

            else:
                self.room_place_down()
            
            self.fix_collide_rooms()
            
            rect_place(world_map,self.newConnect[0],self.newConnect[1], 2, 2, WorldItem.CONNECT)
            rect_place(world_map, self.newX, self.newY, self.newW, self.newH, WorldItem.GROUND)
            self.rooms.append({'name':i+1,'X':self.newX,'Y':self.newY,'W':self.newW,'H':self.newH,'connect':(self.newConnect[0],self.newConnect[1]),'direction':self.last_placement})
            
            self.x, self.y, self.w, self.h, self.connect = self.newX, self.newY, self.newW, self.newH, self.newConnect
        
        self.world_map = world_map
    
    def room_place_left(self):
        self.place_newConnect(self.x - 2, self.y + random.randint(0,self.h-2))
        self.newX = self.newConnect[0] - self.newW
        self.newY = self.newConnect[1] - random.randint(0,self.newH-2)
        self.last_placement = 'left'
    def room_place_right(self):
        self.place_newConnect(self.x + self.w, self.y + random.randint(0,self.h-2))
        self.newX = self.newConnect[0] +2
        self.newY = self.newConnect[1] - random.randint(0,self.newH-2)
        self.last_placement = 'right'
    def room_place_down(self):
        self.place_newConnect(self.x + random.randint(1,self.w-2), self.y + self.h)
        self.newX = self.newConnect[0] - random.randint(0,self.newW-2)
        self.newY = self.newConnect[1] +2
        self.last_placement = 'down'
    
    def room_place_direction(self,direction):
        if direction == 'down':
            self.room_place_down()
        elif direction == 'left':
            self.room_place_left()
        elif direction == 'right':
            self.room_place_right()

    def place_newConnect(self,x,y):
        self.newConnect[0] = x
        self.newConnect[1] = y

    def fix_collide_rooms(self): #plupart des collisions arrivent a cause de newY trop haut 'dont work'
        collided=False

        if self.newY <= 10:
            self.room_place_down()
        
        for room in self.rooms:
            if collision(self.newX-1,self.newY-1,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])):
                direction = self.rooms[-2]['direction']
                self.room_place_direction(direction)
                if collision(self.newX-1,self.newY-1,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])):
                    direction = self.rooms[-1]['direction']
                    self.room_place_direction(direction)
                if collision(self.newX-1,self.newY-1,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])):
                    collided=True
                else:
                    collided=False
        
        if collided:
            self.room_place_down()

    def spaceship_walls_place(self):
        rect_place(self.world_map,WIDTH//2+5,4,1,5,WorldItem.INVISIBLE)
        rect_place(self.world_map,WIDTH//2-2,4,1,5,WorldItem.INVISIBLE)
        rect_place(self.world_map,WIDTH//2-1,4,6,1,WorldItem.INVISIBLE)
        rect_place(self.world_map,WIDTH//2+3,9,2,1,WorldItem.WALL)
        rect_place(self.world_map,WIDTH//2-1,9,2,1,WorldItem.WALL)

class Furniture: #objects interactables to get items and fuel
    def __init__(self,rooms):
        self.rooms = rooms
        chests = []
        for i in range(len(self.rooms)//2): #puts 10 chests in all the rooms, stored in the list as the number of the room its going to be in
            room_chest = random.randint(1,len(self.rooms)-1)
            if room_chest in chests:
                for attempt in range(5): #attemps 5 times to put the chest in a different room
                    if room_chest in chests:
                        if room_chest<len(self.rooms)-1: #1 room further if there is a room after
                            room_chest += 1
                        else:
                            room_chest = random.randint(1,len(self.rooms)//2+3)#else randomly in the first half of the rooms 
            chests.append(room_chest)
        
        for index in chests:
            room = self.rooms[index]
            X_pos = random.randint(room['X'],room['X']+room['W']-1)
            Y_pos = random.randint(room['Y'],room['Y']+room['H']-1)
            self.rooms[index]['chest'] = (X_pos,Y_pos)
            self.rooms[index]['chest_opening'] = 0
                
        
        recyclers = []
        for i in range(len(self.rooms)//2+3):
            room_recycler = random.randint(5,len(self.rooms)-1)
            if room_recycler in recyclers:
                for attempt in range(5):
                    if room_recycler in recyclers:
                        if room_recycler<len(self.rooms)-1:
                            room_recycler += 1
                        else:
                            room_recycler = random.randint(1,len(self.rooms)//2+5)
            recyclers.append(room_recycler)
        
        for index in recyclers:
            room = self.rooms[index]
            X_pos = random.randint(room['X'],room['X']+room['W']-1)
            Y_pos = random.randint(room['Y'],room['Y']+room['H']-1)
            if 'chest' in self.rooms[index].keys():
                for attempt in range(5):
                    if (X_pos,Y_pos) == self.rooms[index]['chest']:
                        X_pos = random.randint(room['X'],room['X']+room['W']-1)
                        Y_pos = random.randint(room['Y'],room['Y']+room['H']-1)
            self.rooms[index]['recycler'] = (X_pos,Y_pos)

class Physics: #This is used to have a common move function
    def __init__(self, owner, world):
        self.world = world
        self.owner = owner
        self.collision_happened = False

    def move(self, vector, coef): #We give a movement vector and get the new coordinates of the entity
        X = int(self.owner.x//TILE_SIZE)
        Y = int(self.owner.y//TILE_SIZE)

        #We handle horizontal and vertical movement separatly to make problem solving easier

        #Calculate the new position and prevent entities from going faster than 1T/f in order to prevent clipping
        if abs(vector[0]*coef) < TILE_SIZE:
            new_x = self.owner.x + vector[0]*coef
        else:
            new_x = self.owner.x + (pyxel.sgn(vector[0]) * (TILE_SIZE - 0.01))
        new_X = X+pyxel.sgn(vector[0])

        if new_x+TILE_SIZE > new_X*TILE_SIZE:
            new_x = new_X*TILE_SIZE
            
        if vector[0]!=0:
            next_X_1 = self.world.world_map[Y][new_X]
            if self.owner.y != Y*TILE_SIZE:
                next_X_2 = self.world.world_map[Y+1][new_X]
            else:
                next_X_2 = WorldItem.GROUND
            #If there's enough space for the entity to move, it moves unimpeded
            if (next_X_1 not in WorldItem.WALLS or not collision(new_x, self.owner.y, new_X*TILE_SIZE, Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])) and (next_X_2 not in WorldItem.WALLS or not collision(new_x, self.owner.y, new_X*TILE_SIZE, (Y+1)*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])):
                self.owner.x = new_x
            #Else If the movement puts the entity in the wall, we snap it back to the border to prevent clipping.
            elif (next_X_1 in WorldItem.WALLS or next_X_2 in WorldItem.WALLS) and new_x+self.owner.width>X*TILE_SIZE and (X+1)*TILE_SIZE>new_x:
                self.collision_happened = True
                self.owner.x = (new_X-pyxel.sgn(vector[0]))*TILE_SIZE
        
        X = int(self.owner.x//TILE_SIZE)

        #We calculate vertical movement in the same way we do horizontal movement

        if abs(vector[1]*coef) < TILE_SIZE:
            new_y = self.owner.y + vector[1]*coef
        else:
            new_y = self.owner.y + (pyxel.sgn(vector[1]) * (TILE_SIZE - 0.01))
        new_Y = Y+pyxel.sgn(vector[1])
        if new_y+TILE_SIZE > new_Y*TILE_SIZE:
            new_y = new_Y*TILE_SIZE

        
        if vector[1]!=0:
            next_Y_1 = self.world.world_map[new_Y][X]
            if self.owner.x != X*TILE_SIZE:
                next_Y_2 = self.world.world_map[new_Y][X+1]
            else:
                next_Y_2 = WorldItem.GROUND
            
            if (next_Y_1 not in WorldItem.WALLS or not collision(self.owner.x, new_y, X*TILE_SIZE, new_Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])) and (next_Y_2 not in WorldItem.WALLS or not collision(self.owner.x, new_y, (X+1)*TILE_SIZE, new_Y*TILE_SIZE, [self.owner.width, self.owner.height], [TILE_SIZE, TILE_SIZE])):
                self.owner.y = new_y
            elif (next_Y_1 in WorldItem.WALLS or next_Y_2 in WorldItem.WALLS) and new_y+self.owner.height>Y*TILE_SIZE and (Y+1)*TILE_SIZE>new_y:
                self.collision_happened = True
                self.owner.y = (new_Y-pyxel.sgn(vector[1]))*TILE_SIZE

class Player: #Everything relating to the player and its control
    def __init__(self, app):
        self.app = app
        self.world = app.world
        self.camera = app.camera
        self.info = app.info
        self.itemList = app.itemList

        self.alive = True
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.physics = Physics(self, self.world)

        self.image = (1,3)
        self.facing = [1,0]
        self.last_facing = [1,0]

        self.speed = 0.25
        self.knockbackCoef = 1
        self.momentum = 0
        self.speedFallOff = 4

        self.isDashing = False
        self.dashCooldown = 40
        self.dashLength = 20
        self.dashFrame = 0
        self.dashStrength = self.speed*3
        self.dashDamage = 0
        self.dashDamageKnockbackCoef = 0.5
        
        self.stuck = False
        self.open_time = 240

        self.gun = dic_copy(Guns.PISTOL)

        self.attackFrame = 0
        self.damage = 10
        self.slash_cooldown = 0.5*120
        self.slashFrame = 0
        self.pierceDamage = 1

        self.ownedItems = []
        self.justKilled = False

        self.luck = 0

        self.shotsFired = 0
        self.enemiesKilled = 0
        self.itemsPickedUp = 0

        self.fuel = 0
        self.reset(self.world)

    def reset(self,world):
        self.world = world
        self.x = world.player_init_posX*TILE_SIZE
        self.y = world.player_init_posY*TILE_SIZE
        self.rooms = self.world.roombuild.rooms
        self.room = self.rooms[0]

        self.lever_pulled = False
        self.no_text = False

        self.health = 80
        self.max_health = 80
        self.hitFrame = 0
        self.hitLength = 120
        self.isHit = False
        self.pickup_text = ["N/A"]
        
    def update(self): #All the things we run every frame to make the player work
        if pyxel.btnp(pyxel.KEY_A):
            self.health = 0
        self.no_text = True

        self.room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)

        self.loadedEntitiesInRange = []

        for entity in loadedEntities: #Only load the entities in the camera
            if in_perimeter(self.camera.x+CAM_WIDTH//2,self.camera.y+CAM_HEIGHT//2,entity.x,entity.y,CAM_WIDTH*3//4):
                self.loadedEntitiesInRange.append(entity)

        self.posXmouse = self.camera.x+pyxel.mouse_x
        self.poxYmouse = self.camera.y+pyxel.mouse_y
        if not self.stuck:
            if not self.isDashing:
                self.movement()
                self.fireWeapon()
                self.slash()
                self.reloadWeapon()
                self.dash()
            else:
                self.dashMovement()
        
        self.hitDetection()
        self.attackFrame += 1
        self.dashFrame += 1
        self.hitFrame += 1
        self.slashFrame +=1
        self.preventOOB()
        self.furniture_gestion()
        self.description_text()
        self.change_PickupText()
        self.check_death()

        if self.health > self.max_health:
            self.health = self.max_health
        if self.gun["mag_ammo"] > self.gun["max_ammo"]:
            self.gun["mag_ammo"] = self.gun["max_ammo"]
        
    def update_in_ship(self): #All the things we run every frame while the player is in the ship
        
        self.posXmouse = self.camera.x+pyxel.mouse_x
        self.poxYmouse = self.camera.y+pyxel.mouse_y
        if not self.isDashing and not self.stuck:
            self.movement()
            self.dash()
        else:
            self.dashMovement()
            
        self.dashFrame += 1
        self.change_PickupText()
        self.preventOOB()
        if in_perimeter(self.x,self.y,56,58,10):
            self.lever_gestion()
            self.change_PickupText()
        else:
            self.pickup_text = ['N/A']

    def lever_gestion(self):
        self.lever_pulled = False
        self.pickup_text = ['[F] to stop at a bunker', '', '']
        self.no_text = False
        if pyxel.btnp(pyxel.KEY_F):
            self.lever_pulled = True

    def movement(self): #Handle ZQSD inputs and translate them into movement
        if pyxel.btn(pyxel.KEY_Q):
            self.physics.move([-1,0], self.momentum)
            self.facing[0] = -1
            self.image = (1,2)
        if pyxel.btn(pyxel.KEY_D):
            self.physics.move([1,0], self.momentum)
            self.facing[0] = 1
            self.image = (0,2)
        if pyxel.btn(pyxel.KEY_Z):
            self.physics.move([0,-1], self.momentum)
            self.facing[1] = -1
            self.image = (0,3)
        if pyxel.btn(pyxel.KEY_S):
            self.physics.move([0,1], self.momentum)
            self.facing[1] = 1
            self.image = (1,3)
        if not (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D)):
            self.facing[0] = 0
        if not (pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S)):
            self.facing[1] = 0
            
        if (pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_D)):
            self.image = (2,2)
        if (pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_Q)):
            self.image = (3,2)
        if (pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_D)):
            self.image = (2,3)
        if (pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_Q)):
            self.image = (3,3)
            
        if self.facing == [0,0]:
            self.facing[0] = self.last_facing[0]
            self.facing[1] = self.last_facing[1]
        else:
            self.last_facing[0] = self.facing[0]
            self.last_facing[1] = self.facing[1]

        if (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S))and self.momentum <= self.speed and not self.stuck:
            self.momentum = self.speed
        else:
            self.momentum /= self.speedFallOff

    def fireWeapon(self): #Fire the player's gun when they left-click
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.attackFrame>=self.gun["cooldown"] and self.gun["mag_ammo"]>0:
            pyxel.play(2,60)
            self.attackFrame = 0
            self.gun["mag_ammo"] -= 1
            self.shotsFired += 1
            for i in range(self.gun["bullet_count"]):
                horizontal = self.posXmouse - (self.x+self.width/2)
                vertical = self.poxYmouse - (self.y+self.height/2)
                norm = math.sqrt(horizontal**2+vertical**2)
                if norm != 0:
                    cos = horizontal/norm
                    sin = vertical/norm
                    angle = math.acos(cos)*pyxel.sgn(sin)
                    lowest_angle = angle - self.gun["spread"]*(math.pi/180)
                    highest_angle = angle + self.gun["spread"]*(math.pi/180)
                    angle = random.uniform(lowest_angle, highest_angle)
                    cos = math.cos(angle)
                    sin = math.sin(angle)
                else:
                    cos = 0
                    sin = 0
                Bullet(self.app, self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.gun, "player", self.shotsFired)

    def reloadWeapon(self): #Makes the player reload its weapon when it reaches 0 or presses R
        if pyxel.btnp(pyxel.KEY_R) and self.gun["mag_ammo"]<self.gun["max_ammo"] and self.gun["mag_ammo"]!=0:
            self.gun["mag_ammo"] = 0
            self.attackFrame = 0
            
        if self.gun["mag_ammo"]==0 and self.attackFrame>=self.gun["reload"] and self.gun["reserve_ammo"]>0:
            if self.gun["reserve_ammo"]>=self.gun["max_ammo"]:
                self.gun["mag_ammo"]=self.gun["max_ammo"]
                self.gun["reserve_ammo"] -= self.gun["max_ammo"]
            else:
                self.gun["mag_ammo"] = self.gun["reserve_ammo"]
                self.gun["reserve_ammo"] = 0
            self.triggerOnReloadItems()
            
    def slash(self):
        if (pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btn(pyxel.KEY_C)) and self.slashFrame>=self.slash_cooldown:
            self.slashFrame = 0
            pyxel.play(2,random.randint(47,49))
            horizontal = self.posXmouse - (self.x+self.width/2)
            vertical = self.poxYmouse - (self.y+self.height/2)
            norm = math.sqrt(horizontal**2+vertical**2)
            if norm != 0:
                cos = horizontal/norm
                sin = vertical/norm
            else:
                cos = 0
                sin = 0
            self.world.effects.append({'x':self.x+cos*TILE_SIZE,'y':self.y+sin*TILE_SIZE,'image':[6,6],'scale':1.1,'time':pyxel.frame_count})
            for entity in self.loadedEntitiesInRange:
                if collision(self.x+cos*TILE_SIZE,self.y+sin*TILE_SIZE,entity.x,entity.y,(TILE_SIZE*1.1,TILE_SIZE*1.1),(TILE_SIZE,TILE_SIZE)) and entity.type == 'enemy':
                    entity.health -= Melees.SHOVE["damage"]
                    entity.hitStun = True
                    if "movement" in entity.abilities.keys():
                        entity.apply_knockback([cos,sin], Melees.SHOVE["damage"], Melees.SHOVE["knockback_coef"])

    def dash(self): #Start the dash when the player presses space
        if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_SHIFT)) and self.dashFrame >= self.dashCooldown:
            self.isDashing = True
            self.dashFrame = 0
            self.momentum = self.dashStrength
            self.image = [6,2]

    def dashMovement(self): #Does the movement while the player is dashing
        self.physics.move(self.facing, self.momentum)
        if self.dashDamage > 0:
            for entity in loadedEntities:
                if entity.type == "enemy" and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]) and not entity.hitByDash:
                    entity.health -= self.dashDamage
                    entity.hitStun = True
                    entity.hitByDash = True
                    if "movement" in entity.abilities.keys():
                        entity.apply_knockback(self.facing, self.dashDamage, self.dashDamageKnockbackCoef)
        if self.dashFrame >= self.dashLength:
            self.isDashing = False
            self.dashFrame = 0
            self.triggerOnDashItems()
            for entity in loadedEntities:
                if entity.type == "enemy" and entity.hitByDash:
                    entity.hitByDash = False
        if pyxel.frame_count % self.dashLength >= self.dashLength//2-2:
            self.image = [6,2]
        else:
            self.image = [7,2]

    def hitDetection(self): #Checks if the player got hit this frame
        if self.isHit and self.hitFrame >= self.hitLength:
                self.isHit = False
                self.hitFrame = 0

    def applyKnockback(self, vector, damage, coef):
        base_knockback = 10*len(str(damage))
        coef_knockback = coef * self.knockbackCoef * base_knockback
        self.physics.move(vector, coef_knockback)

    def preventOOB(self): #Prevents the player going out of bounds
        if self.x<0:
            self.x = 0
        if self.y<0:
            self.y = 0
        if self.x > WIDTH*TILE_SIZE:
            self.x = (WIDTH-1)*TILE_SIZE
        if self.y > HEIGHT*TILE_SIZE:
            self.y = (HEIGHT-1)*TILE_SIZE

    def furniture_gestion(self):
        if 'chest' in self.room.keys():
            if in_perimeter(self.x,self.y,self.room['chest'][0]*TILE_SIZE,self.room['chest'][1]*TILE_SIZE,TILE_SIZE*1.5):
                if self.no_text:
                    self.pickup_text = ['Hold [F] to open', 'Chest', 'Get item or weapon']
                    self.no_text = False

                if pyxel.btn(pyxel.KEY_F):
                    self.stuck = True
                    self.momentum /= self.speedFallOff
                    self.room['chest_opening'] += 1

                    for i in range(3):
                        if self.room['chest_opening'] >= self.open_time//3 * i:
                            self.world.world_map[self.room['chest'][1]][self.room['chest'][0]] = (4+i%2,i//2) # very complex - [0,1,2] into -> [0,1,0] et [0,0,1] for image


                    if self.room['chest_opening'] >= self.open_time:
                        self.spawn_item(self.room['chest'][0],self.room['chest'][1])
                        self.world.world_map[self.room['chest'][1]][self.room['chest'][0]] = WorldItem.GROUND
                        self.room.pop('chest')
                        self.room.pop('chest_opening')
                        self.stuck = False
                else:
                    self.stuck = False
                    self.room['chest_opening'] = 0
                    self.world.world_map[self.room['chest'][1]][self.room['chest'][0]] = (4,0)

        if 'recycler' in self.room.keys():
            if in_perimeter(self.x,self.y,self.room['recycler'][0]*TILE_SIZE,self.room['recycler'][1]*TILE_SIZE,TILE_SIZE*1.5):
                if self.no_text:
                    self.pickup_text = ['[F] to use', 'Recycler', 'Transform random item into fuel']
                    self.no_text = False
                if pyxel.btn(pyxel.KEY_F):
                    if len(self.ownedItems) > 0:
                        self.world.world_map[self.room['recycler'][1]][self.room['recycler'][0]] = WorldItem.GROUND
                        randomItem = random.randint(0,len(self.ownedItems)-1)
                        removedItem = self.ownedItems[randomItem]
                        self.ownedItems.pop(randomItem)

                        if removedItem in self.itemList.common_list:
                            PickUp(self.room['recycler'][0]*TILE_SIZE,self.room['recycler'][1]*TILE_SIZE, "item", self.itemList.FUEL, self)
                        elif removedItem in self.itemList.uncommon_list:
                            for i in range(2):
                                PickUp(self.room['recycler'][0]*TILE_SIZE+random.randint(-2,2),self.room['recycler'][1]*TILE_SIZE+random.randint(-2,2), "item", self.itemList.FUEL, self)
                        elif removedItem in self.itemList.legendary_list:
                            for i in range(3):
                                PickUp(self.room['recycler'][0]*TILE_SIZE+random.randint(-2,2),self.room['recycler'][1]*TILE_SIZE+random.randint(-2,2), "item", self.itemList.FUEL, self)
                            
                        self.room.pop('recycler')
                    else:
                        self.pickup_text = ['[F] to use', 'Recycler', '--NEEDS ITEM--']
                        
    def spawn_item(self,x,y):

        pickup = random.randint(1,2)
        if pickup == 1:
            item_random = random.randint(0, len(self.itemList.common_list)-1)
            item = self.itemList.common_list[item_random]
            PickUp(x*TILE_SIZE, y*TILE_SIZE, "item", item, self)

        elif pickup == 2:
            gun_random = random.randint(26,100)
            for gun in Guns.Gun_list:
                if gun_random in gun["rate"]:
                    PickUp(x*TILE_SIZE, y*TILE_SIZE, "weapon", gun, self)

    def description_text(self): #Checks for all pickups and gets the correct text if the player is standing on them
        for i in range(len(pickUpsOnGround)-1, -1, -1): #from most recent to oldest
            pickup = pickUpsOnGround[i]
            if collision(self.x, self.y, pickup.x, pickup.y, [self.width, self.height], [pickup.width, pickup.height]):
                self.pickup_text = ["[E] to pickup", pickup.object["name"], pickup.object["description"]]
                self.no_text = False

    def change_PickupText(self):
        if not self.no_text:
            self.info.description = self.pickup_text
        else:
            self.info.description = ["N/A"]

    def check_death(self): #Does what the name implies
        if self.health<=0:
            self.alive = False

    def getItem(self, item): #Adds an item to the player inventory, and triggers the effect of passive items
        if item['name']!='Fuel':
            self.ownedItems.append(item)
            self.itemsPickedUp += 1
        if item["trigger"] == "passive" and (item["effect"] == "stat"):
            for change in item["function"]:
                self.increaseStat(change[0], change[1], change[2], change[3])

    def changeWeapon(self, gun): #Allows the player to change guns, randomize its values slightly, and then reapplies item effects for it to work 
        self.gun = dic_copy(gun)
        for key in self.gun.keys():
            if key not in ["name", "description", "image", "bullet_image", "rate", "bullet_count"]:
                lowest_value = self.gun[key]*0.9
                highest_value = self.gun[key]*1.1
                self.gun[key] = random.uniform(lowest_value, highest_value)
        for item in self.ownedItems:
            if item["trigger"] == "passive" and item["effect"]=="stat":
                for change in item["function"]:
                    if change[3]:
                        self.increaseStat(change[0], change[1], change[2], change[3])
        for boost in activeBoosts:
            if boost.gun:
                self.increaseStat(boost.stat, boost.operation, boost.value, boost.gun)
        self.gun["piercing"] = math.ceil(self.gun["piercing"])
        self.gun["max_ammo"] = math.ceil(self.gun["max_ammo"])
        self.gun["mag_ammo"] = self.gun["max_ammo"]
        self.gun["reserve_ammo"] = math.ceil(self.gun["reserve_ammo"])

    def increaseStat(self, stat, operation, value, gun): #Increases a stat by the stated operation and value
        if not gun:
            if operation == "addition":
                setattr(self, stat, getattr(self, stat)+value)
            elif operation == "multiplication":
                setattr(self, stat, getattr(self, stat)*value)
        else:
            if operation == "addition":
                self.gun[stat] += value
            elif operation == "multiplication":
                self.gun[stat] *= value

        self.health = math.ceil(self.health)
        self.max_health = math.ceil(self.max_health)
        self.gun["bullet_count"] = math.ceil(self.gun["bullet_count"])
        self.gun["max_ammo"] = math.ceil(self.gun["max_ammo"])
        self.gun["mag_ammo"] = math.ceil(self.gun["mag_ammo"])
        self.gun["reserve_ammo"] = math.ceil(self.gun["reserve_ammo"])
        if self.speed  > 1.9*TILE_SIZE:
                self.speed = 1.9*TILE_SIZE
        
    def triggerOnKillItems(self): #Self-explanatory
        for item in self.ownedItems:
            if item["trigger"] == "onKill":
                if item["effect"] == "stat":
                    for change in item["function"]:
                        self.increaseStat(change[0], change[1], change[2], change[3])
                elif item["effect"] == "boost":
                    for change in item["function"]:
                        Boost(change[0], change[1], change[2], change[3], change[4], self, item)

    def triggerOnReloadItems(self): #Self-explanatory
        for item in self.ownedItems:
            if item["trigger"] == "onReload":
                if item["effect"] == "stat":
                    for change in item["function"]:
                        self.increaseStat(change[0], change[1], change[2], change[3])
                elif item["effect"] == "boost":
                    for change in item["function"]:
                        Boost(change[0], change[1], change[2], change[3], change[4], self, item)
        
    def triggerOnDashItems(self): #Self-explanatory
        for item in self.ownedItems:
            if item["trigger"] == "onDash":
                if item["effect"] == "stat":
                    for change in item["function"]:
                        self.increaseStat(change[0], change[1], change[2], change[3])
                elif item["effect"] == "boost":
                    for change in item["function"]:
                        boost_already_active = False
                        for boost in activeBoosts: #Si l'item est déja actif, on remet son timer à 0, sinon, on créé un boost
                            if boost.creator == item:
                                boost_already_active = True
                                boost.frame = 0
                        if not boost_already_active:
                            Boost(change[0], change[1], change[2], change[3], change[4], self, item)

class Melees: #Basic class for all the melee weapons, will get expanded once we implement the player's melee weapons
    SPIDER_MELEE = {"damage":5, "range":1*TILE_SIZE, "cooldown":1*FPS, "knockback_coef":1}
    BULWARK_MELEE = {"damage":15, "range":1*TILE_SIZE, "cooldown":1*FPS, "knockback_coef":1}
    HIVE_QUEEN_MELEE = {"damage":5, "range":1*TILE_SIZE, "cooldown":1*FPS, "knockback_coef":1}
    HATCHLING_MELEE = {"damage":2, "range":1*TILE_SIZE, "cooldown":0.75*FPS, "knockback_coef":1}

    SHOVE = {"damage":5, "range":1*TILE_SIZE, "cooldown":1*FPS, "knockback_coef":1.5}

class Guns: #Contains all the different guns the player can get
    NONE = {"name":"None","description":"No weapon",
            "image":[0,0],
            "bullet_image":[0,0],
            "rate":[],
            "spread":0, "bullet_count":0,
            "bullet_speed":1, "range":1,
            "damage":0,  "piercing":0, "explode_radius":0, "knockback_coef":0,
            "max_ammo":0, "mag_ammo":0, "reserve_ammo":0, "reload":1*FPS, 
            "cooldown":1*FPS}
    
    PISTOL = {"name":"Pistol", "description":"Basic weapon",
              "image":[1*TILE_SIZE,7*TILE_SIZE],
              "bullet_image":[0,6*TILE_SIZE],
              "rate":[x for x in range(1,26)],
              "spread":15, "bullet_count":1,
              "bullet_speed":0.75, "range":6*TILE_SIZE,
              "damage":9,  "piercing":0, "explode_radius":0, "knockback_coef":5,
              "max_ammo":16, "mag_ammo":16, "reserve_ammo":60, "reload":0.8*FPS,
              "cooldown":1/3*FPS}
    
    SHOTGUN = {"name":"Shotgun", "description":"Multiple pellets, medium damage",
               "image":[3*TILE_SIZE,7*TILE_SIZE],
               "bullet_image":[0,6*TILE_SIZE],
               "rate":[x for x in range(26,51)],
               "spread":25, "bullet_count":6,
               "bullet_speed":0.6, "range":4*TILE_SIZE,
               "damage":12,  "piercing":0, "explode_radius":0, "knockback_coef":1,
               "max_ammo":5, "mag_ammo":5, "reserve_ammo":20, "reload":3*FPS, 
               "cooldown":0.75*FPS}
    
    SMG = {"name":"SMG", "description":"Highest fire rate, low damage",
           "image":[0*TILE_SIZE,7*TILE_SIZE],
           "bullet_image":[0,6*TILE_SIZE],
           "rate":[x for x in range(51,76)],
           "spread":20, "bullet_count":1,
           "bullet_speed":1, "range":4*TILE_SIZE,
           "damage":8,  "piercing":0, "explode_radius":0, "knockback_coef":1,
           "max_ammo":40, "mag_ammo":40, "reserve_ammo":140, "reload":2.5*FPS, 
           "cooldown":0.12*FPS}
    
    RIFLE = {"name":"Rifle", "description":"High fire rate, medium damage",
             "image":[2*TILE_SIZE,7*TILE_SIZE],
             "bullet_image":[0,6*TILE_SIZE],
             "rate":[x for x in range(76,86)],
             "spread":12, "bullet_count":1,
             "bullet_speed":0.9, "range":7*TILE_SIZE,
             "damage":12,  "piercing":1, "explode_radius":0, "knockback_coef":1,
             "max_ammo":24, "mag_ammo":24, "reserve_ammo":70, "reload":3*FPS, 
             "cooldown":0.25*FPS}
    
    SNIPER = {"name":"Sniper", "description":"Single fire, high damage",
              "image":[4*TILE_SIZE,7*TILE_SIZE],
              "bullet_image":[0,6*TILE_SIZE],
              "rate":[x for x in range(86,96)],
              "spread":0, "bullet_count":1,
              "bullet_speed":2, "range":20*TILE_SIZE,
              "damage":20,  "piercing":4, "explode_radius":0, "knockback_coef":1,
              "max_ammo":4, "mag_ammo":4, "reserve_ammo":25, "reload":4*FPS, 
              "cooldown":1*FPS}
    
    GRENADE_LAUNCHER = {"name":"Grenade Launcher", "description":"Single fire, explosive shots",
                        "image":[5*TILE_SIZE,7*TILE_SIZE],
                        "bullet_image":[0,6*TILE_SIZE],
                        "rate":[x for x in range(96,101)],
                        "spread":5, "bullet_count":1,
                        "bullet_speed":1.5, "range":20*TILE_SIZE,
                        "damage":20, "piercing":0, "explode_radius":1.5*TILE_SIZE, "knockback_coef":2,
                        "max_ammo":1, "reserve_ammo":20, "mag_ammo":1, "reload":1.5*FPS, 
                        "cooldown":1*FPS}
    
    Gun_list = [PISTOL, RIFLE, SMG, SNIPER, SHOTGUN, GRENADE_LAUNCHER]

    TURRET_GUN = {"name":"Turret Gun","description":"You're not supposed to see this",
            "image":[0,0],
            "bullet_image":[1*TILE_SIZE,6*TILE_SIZE],
            "rate":[],
            "spread":0, "bullet_count":1,
            "bullet_speed":0.3, "range":7*TILE_SIZE,
            "damage":5,  "piercing":0, "explode_radius":0, "knockback_coef":1,
            "max_ammo":0, "mag_ammo":0, "reserve_ammo":0, "reload":1*FPS, 
            "cooldown":0.5*FPS}

class EnemyTemplates: #all enemies and their stats to get easily
    SPIDER = {'name':'spider',
              "image":(0*TILE_SIZE,12*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE,
              'spawning_chance':[x for x in range(0,45)],
              "health":40,
              "abilities":{
                  "movement":{"speed":0.36, "knockback_coef":1, "weight":1},
                  "melee_attack":{"weapon":Melees.SPIDER_MELEE, "freeze":40},
                  "lunge":{"range":6*TILE_SIZE, "freeze":40, "length":20, "speed":1,"cooldown":random.randint(2,6)*120//2, "damage":0, "knockback_coef":0}}}
    
    BULWARK = {'name':'bulwark',
               "image":(0*TILE_SIZE,18*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE,
               'spawning_chance':[x for x in range(65,75)],
               "health":100,
               "abilities":{
                   "movement":{"speed":0.18, "knockback_coef":0, "weight":1},
                   "melee_attack":{"weapon":Melees.BULWARK_MELEE, "freeze":40},
                   "lunge":{"range":6*TILE_SIZE, "freeze":40, "length":15, "speed":1,"cooldown":random.randint(2,6)*120//2, "damage":0, "knockback_coef":0}}}
    
    STALKER = {'name':'stalker',
               "image":(0*TILE_SIZE,14*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE,
               'spawning_chance':[x for x in range(45,65)],
               "health":40,
               "abilities":{
                   "movement":{"speed":0.1, "knockback_coef":1, "weight":1},
                   "lunge":{"range":12*TILE_SIZE, "freeze":60, "length":20, "speed":1.5,"cooldown":random.randint(2,6)*120//2, "damage":10, "knockback_coef":1}}}
    
    TUMOR = {'name':'tumor',
             "image":(0*TILE_SIZE,24*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE,
             'spawning_chance':[x for x in range(75,82)],
             "health":20,
             "abilities":{
                 "movement":{"speed":0.36, "knockback_coef":1, "weight":1},
                 "lunge":{"range":6*TILE_SIZE, "freeze":40, "length":20, "speed":1,"cooldown":random.randint(2,4)*120//2, "damage":0, "knockback_coef":0},
                 "kamikaze":{"damage":5, "radius":2*TILE_SIZE, "knockback_coef":2}}}
    
    TURRET = {'name':'turret',
              "image":(0*TILE_SIZE,22*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE,
              'spawning_chance':[x for x in range(82,90)],
              "health":40,
              "abilities":{
                  "ranged_attack":{"weapon":Guns.TURRET_GUN, "freeze":0}}}
    
    INFECTED_SCRAPPER = {'name':'infected_scrapper',
                         "image":(0*TILE_SIZE,26*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, 
                         'spawning_chance':[x for x in range(91,92)],
                         "health":50,
                         "abilities":{
                             "movement":{"speed":0.45, "knockback_coef":1, "weight":1}, 
                             "ranged_attack":{"weapon":"random", "freeze":40}, 
                             "lunge":{"range":12*TILE_SIZE, "freeze":40, "length":20, "speed":1,"cooldown":random.randint(2,6)*120//2, "damage":0, "knockback_coef":0}}}
    
    HATCHLING = {'name':'hatchling',
                 "image":(0*TILE_SIZE,20*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, 
                 'spawning_chance':[], 
                 "health":10, 
                 "abilities":{
                     "movement":{"speed":0.4, "knockback_coef":1, "weight":1}, 
                     "melee_attack":{"weapon":Melees.HATCHLING_MELEE, "freeze":40}, 
                     "lunge":{"range":6*TILE_SIZE, "freeze":30, "length":15, "speed":1.5,"cooldown":random.randint(2,6)*120//2, "damage":0, "knockback_coef":0}}}
    
    HIVE_QUEEN = {'name':'hive_queen',
                  "image":(0*TILE_SIZE,16*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, 
                  'spawning_chance':[x for x in range(92,99)],
                  "health":50,
                  "abilities":{
                      "movement":{"speed":0.15, "knockback_coef":1, "weight":1}, 
                      "melee_attack":{"weapon":Melees.HIVE_QUEEN_MELEE, "freeze":40}, 
                      "lunge":{"range":2*TILE_SIZE, "freeze":40, "length":20, "speed":0.5,"cooldown":random.randint(2,6)*120//2, "damage":0, "knockback_coef":0}, 
                      "spawner":{"passive_amount":2, "death_amount":3, "cooldown":5*FPS, "entity":"HATCHLING"}}}
    
    
    ENEMY_LIST = [SPIDER,BULWARK,STALKER,TUMOR,TURRET,INFECTED_SCRAPPER,HIVE_QUEEN,HATCHLING]

class Enemy: #all the gestion of the atitude of the enemies
    def __init__(self, app, x, y, template, always_loaded=False, spawned=False): #Creates a new enemy, with all its stats
        self.app = app
        self.player = app.player
        self.world = app.world
        self.itemList = app.itemList
        self.difficulty = app.difficulty

        self.x = x
        self.y = y
        self.physics = Physics(self, self.world)
        self.rooms = self.world.roombuild.rooms
        self.room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)
        self.scale = 1
        self.spawned = spawned

        self.health = math.ceil(template["health"] * (1.25**self.difficulty))
        self.cos = 0
        self.sin = 0

        self.loaded = False
        self.always_loaded = always_loaded

        self.base_image = template["image"]
        self.image = [template["image"][0], template["image"][1]]
        self.facing = [0,0]
        self.img_change = [0,0]
        self.width = template["width"]
        self.height = template["height"]

        self.pierced = []

        self.hitStun = False
        self.hitFrame = 0
        self.knockback = 0
        self.hitByDash = False

        self.lastHitBy = "N/A"

        self.type = "enemy"
        self.name = template["name"]
        self.pathing()

        self.abilities = dic_copy(template["abilities"])

        if "ranged_attack" in self.abilities.keys():
            if self.abilities["ranged_attack"]["weapon"] == "random":
                gun_random = random.randint(1,100)
                for gun in Guns.Gun_list:
                    if gun_random in gun["rate"]:
                        self.abilities["ranged_attack"]["weapon"] = gun
            self.abilities["ranged_attack"]["weapon"]["damage"] = math.ceil(self.abilities["ranged_attack"]["weapon"]["damage"] * (1.25**self.difficulty))
            self.isAttackingRanged = False
            self.rangedAttackFrame = 0
            self.rangedAttackVector = []
            self.shotsFired = 0

        if "melee_attack" in self.abilities.keys():
            self.abilities["melee_attack"]["weapon"]["damage"] = math.ceil(self.abilities["melee_attack"]["weapon"]["damage"] * (1.25**self.difficulty))
            self.isAttackingMelee = False
            self.meleeAttackFrame = 0
            self.meleeAttackVector = []

        if "lunge" in self.abilities.keys():
            self.lungeFrame = 0
            self.lungeState = "notLunging"
            self.lungeVector = []

        if "kamikaze" in self.abilities.keys():
            self.abilities["kamikaze"]["damage"] = math.ceil(self.abilities["kamikaze"]["damage"] * (1.25**self.difficulty))

        if "spawner" in self.abilities.keys():
            self.spawnFrame = 0

        self.actionPriority = 0

        loadedEntities.append(self) #As long as this enemy exists in this list, its alive

    def update(self): #All the things we need to do every frame to make the enemy work
        
        if self in self.player.loadedEntitiesInRange:
            self.loaded = True
        else:
            self.loaded = False

        self.room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)
        
        self.img_change = [0,0]

        if self.loaded or self.always_loaded:
            self.establishPriority()
            if "movement" in self.abilities.keys():
                self.enemies_pusharound()
            if "melee_attack" in self.abilities.keys():
                self.melee_attack()
                self.meleeAttackFrame += 1
            if "ranged_attack" in self.abilities.keys():
                self.ranged_attack()
                self.rangedAttackFrame += 1
            if "lunge" in self.abilities.keys():
                self.lunge()
                self.lungeFrame += 1
            if "spawner" in self.abilities.keys():
                self.spawner()
                self.spawnFrame += 1
            if "kamikaze" in self.abilities.keys():
                self.kamikaze()
            self.getFacing()
            self.death()
            
            if self.hitStun:
                self.hitStunFunction()
            else:
                self.pathing()
                if "movement" in self.abilities.keys():
                    self.moveInPathing()

            self.image[0], self.image[1] = self.base_image[0] + self.facing[0] + self.img_change[0], self.base_image[1] + self.facing[1] + self.img_change[1]
    
    def establishPriority(self):
        # The Action with a priority of 0 (walking), is the default action, which happens when no other action is going on. All actions with a priority > 0 will only happen when their condition is met, and when the action the entity is doing has a strictly lower priority
        if "melee_attack" in self.abilities.keys() and self.isAttackingMelee:
            self.actionPriority = 1
        elif "ranged_attack" in self.abilities.keys() and self.isAttackingRanged:
            self.actionPriority = 1
        elif "lunge" in self.abilities.keys() and self.lungeState != "notLunging":
            self.actionPriority = 1
        else:
            self.actionPriority = 0

    def hitStunFunction(self):
        self.img_change[0] = 16
        if self.hitFrame >= 24:
            self.hitStun = False
            self.hitFrame = 0
        self.hitFrame += 1

    def moveInPathing(self):
        if self.actionPriority == 0:
            if self.norm < 100 and self.norm > 5:
                self.physics.move([self.cos, self.sin], self.abilities["movement"]["speed"])
    
    def enemies_pusharound(self): #Prevent enemies from overlapping by making them push each other
        for entity in self.player.loadedEntitiesInRange:
            cos = random.randint(-200,200)/100
            sin = math.sqrt((2-cos)**2) * (random.randint(0,1)*2-1)
            if entity.type == "enemy" and collision(self.x, self.y, entity.x ,entity.y, [self.width, self.height], [entity.width, entity.height]) and self != entity and "movement" in entity.abilities.keys():
                self.physics.move([cos, sin], entity.abilities["movement"]["weight"])
                entity.physics.move([-cos, -sin], self.abilities["movement"]["weight"])

    def apply_knockback(self, vector, damage, coef):
        base_knockback = 10*len(str(damage))
        coef_knockback = coef * self.abilities["movement"]["knockback_coef"] * base_knockback
        self.physics.move(vector, coef_knockback)

    def melee_attack(self):
        if (self.actionPriority == 0 or self.isAttackingMelee) and self.room["name"] == self.player.room["name"]:
            if distance(self.player.x, self.player.y, self.x, self.y) <= self.abilities["melee_attack"]["weapon"]["range"] and self.meleeAttackFrame >= self.abilities["melee_attack"]["weapon"]["cooldown"] and not self.isAttackingMelee:
                self.meleeAttackFrame = 0
                self.isAttackingMelee = True
                self.meleeAttackVector = [self.cos, self.sin]
            if self.isAttackingMelee and self.meleeAttackFrame >= self.abilities["melee_attack"]["freeze"]:
                self.meleeAttackFrame = 0
                self.isAttackingMelee = False
                self.slash()
        if self.room["name"] != self.player.room["name"]:
            self.isAttackingMelee = False

    def ranged_attack(self):
        if (self.actionPriority == 0 or self.isAttackingRanged) and self.room["name"] == self.player.room["name"]:
            if distance(self.player.x, self.player.y, self.x, self.y) <= self.abilities["ranged_attack"]["weapon"]["range"] and self.rangedAttackFrame >= self.abilities["ranged_attack"]["weapon"]["cooldown"] and not self.isAttackingRanged:
                self.rangedAttackFrame = 0
                self.isAttackingRanged = True
                self.rangedAttackVector = [self.cos, self.sin]
            if self.isAttackingRanged and self.rangedAttackFrame >= self.abilities["ranged_attack"]["freeze"]:
                self.rangedAttackFrame = 0
                self.isAttackingRanged = False
                self.shotsFired += 1
                for i in range(self.abilities["ranged_attack"]["weapon"]["bullet_count"]):
                    if self.norm != 0:
                        angle = math.acos(self.cos)*pyxel.sgn(self.sin)
                        lowest_angle = angle - self.abilities["ranged_attack"]["weapon"]["spread"]*(math.pi/180)
                        highest_angle = angle - self.abilities["ranged_attack"]["weapon"]["spread"]*(math.pi/180)
                        angle = random.uniform(lowest_angle, highest_angle)
                        sin = math.sin(angle)
                        cos = math.cos(angle)
                    else:
                        cos = 0
                        sin = 0
                    Bullet(self.app, self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.abilities["ranged_attack"]["weapon"], "enemy", self.shotsFired)
        
        if self.room['name'] != self.player.room['name']:
            self.isAttackingRanged = False

    def slash(self):
        self.world.effects.append({'x':self.x+self.meleeAttackVector[0]*TILE_SIZE,'y':self.y+self.meleeAttackVector[1]*TILE_SIZE,'image':[7,6],'scale':1,'time':pyxel.frame_count})
        pyxel.play(3,54)
        if collision(self.x+self.meleeAttackVector[0]*TILE_SIZE,self.y+self.meleeAttackVector[1]*TILE_SIZE,self.player.x,self.player.y,(TILE_SIZE,TILE_SIZE),(TILE_SIZE,TILE_SIZE)): #pas assez de sin et cos
            self.player.health -= self.abilities["melee_attack"]["weapon"]["damage"]
            self.player.isHit = True
            self.player.hitFrame = 0
            self.player.applyKnockback(self.meleeAttackVector, self.abilities["melee_attack"]["weapon"]["damage"], self.abilities["melee_attack"]["weapon"]["knockback_coef"])

    def lunge(self): #Allows the enemy to lunge at the player
        if (self.actionPriority == 0 or self.lungeState != "notLunging"):
            if self.norm <= self.abilities["lunge"]["range"] and self.lungeFrame >= self.abilities["lunge"]["cooldown"] and self.lungeState == "notLunging":
                self.lungeFrame = 0
                self.lungeState = "freezing"
                self.lungeVector = [self.cos, self.sin]
                if self.name == 'stalker':
                    pyxel.play(3,50)
            if self.lungeState == "freezing" and self.lungeFrame >= self.abilities["lunge"]["freeze"]:
                self.lungeFrame = 0
                self.lungeState = "lunging"
                self.hit_player = False
                pyxel.play(3,random.randint(51,53))
            if self.lungeState == "lunging":
                self.physics.move(self.lungeVector, self.abilities["lunge"]["speed"])
                if self.abilities["lunge"]["damage"] > 0: #Makes the enemy damage the player when colliding
                    if collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]) and not self.hit_player:
                        self.player.health -= self.abilities["lunge"]["damage"]
                        self.player.isHit = True
                        self.player.hitFrame = 0
                        self.hit_player = True
                        self.player.applyKnockback(self.lungeVector, self.abilities["lunge"]["damage"], self.abilities["lunge"]["knockback_coef"])
                if self.lungeFrame >= self.abilities["lunge"]["length"]:
                    self.lungeState = "notLunging"

    def spawner(self): #Allows enemies to spawn hatchlings
        if self.spawnFrame >= self.abilities["spawner"]["cooldown"]:
            for i in range(self.abilities["spawner"]["passive_amount"]):
                Enemy(self.app, self.x, self.y, getattr(EnemyTemplates, self.abilities["spawner"]["entity"]), spawned=True)
            self.spawnFrame = 0

    def kamikaze(self): #Allows enemy to blow itself up
        if collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]):
            self.health = 0

    def getFacing(self):
        if abs(self.horizontal)>abs(self.vertical):
            self.facing[1] = 0
            if self.horizontal>0:
                self.facing[0] = 0
            else:
                self.facing[0] = 8
        else:
            self.facing[1] = 8
            if self.vertical>0:
                self.facing[0] = 0
            else:
                self.facing[0] = 8

        if "lunge" in self.abilities.keys() and self.lungeState == "freezing":
                self.img_change[0] = 32

    def randomItem(self): #Returns a random item, depending on its rarity
        item_rarity = random.randint(1,20)
        if item_rarity == 20:
            item_random = random.randint(0, len(self.itemList.legendary_list)-1)
            item = self.itemList.legendary_list[item_random]
        elif item_rarity>15 and item_rarity<20:
            item_random = random.randint(0, len(self.itemList.uncommon_list)-1)
            item = self.itemList.uncommon_list[item_random]
        else:
            item_random = random.randint(0, len(self.itemList.common_list)-1)
            item = self.itemList.common_list[item_random]
        return item     

    def death(self): #Runs alls the things that happen when the enemy dies
        if self.health <= 0:

            if "spawner" in self.abilities.keys():
                for i in range(self.abilities["spawner"]["death_amount"]):
                    Enemy(self.app, self.x, self.y, getattr(EnemyTemplates, self.abilities["spawner"]["entity"]), spawned=True)

            if "kamikaze" in self.abilities.keys():
                Effect(4,[2*TILE_SIZE, 6*TILE_SIZE], {0:9, 1:9, 2:9, 3:9}, self.x, self.y, TILE_SIZE, TILE_SIZE)
                pyxel.play(3,56)
                if distance(self.x+self.width/2, self.y+self.height/2, self.player.x+self.width/2, self.player.y+self.height/2) <= self.abilities["kamikaze"]["radius"]:
                    self.player.health -= self.abilities["kamikaze"]["damage"]
                    self.player.isHit = True
                    self.player.hitFrame = 0
                    self.player.applyKnockback([self.cos, self.sin], self.abilities["kamikaze"]["damage"], self.abilities["kamikaze"]["knockback_coef"])
                for entity in loadedEntities:
                    if entity.type == "enemy" and distance(self.x+self.width/2, self.y+self.height/2, entity.x+entity.width/2, entity.y+entity.height/2)<=2*TILE_SIZE:
                        entity.health -= self.abilities["kamikaze"]["damage"]
                        entity.hitStun = True
                        if "movement" in entity.abilities.keys():
                            horizontal = entity.x - self.x
                            vertical = entity.y - self.y
                            norm = math.sqrt(horizontal**2+vertical**2)
                            if norm != 0:
                                cos = horizontal/norm
                                sin = vertical/norm
                            else:
                                cos = 0
                                sin = 0
                            entity.apply_knockback([cos, sin], self.abilities["kamikaze"]["damage"], self.abilities["kamikaze"]["knockback_coef"])

            if not self.spawned:
                item_chance = 10 + self.player.luck
                gun_chance = 12

                pickup = random.randint(1,100)
                if pickup <= item_chance:
                    PickUp(self.x, self.y, "item", self.randomItem(), self.player)

                if pickup > 100-gun_chance:
                    gun_random = random.randint(1,100)
                    for gun in Guns.Gun_list:
                        if gun_random in gun["rate"]:
                            PickUp(self.x, self.y, "weapon", gun, self.player)

                if pickup > 100-gun_chance-10-self.player.luck and  pickup <= 100-gun_chance:
                    PickUp(self.x, self.y, "item", self.itemList.FUEL, self.player)

            self.player.triggerOnKillItems()
            self.player.enemiesKilled += 1
            loadedEntities.remove(self)
    
    def pathing(self):
        if self.room['name'] == self.player.room['name']:
            self.horizontal = self.player.x - self.x
            self.vertical = self.player.y - self.y
        else:
            if self.room['name']>self.player.room['name']:
                x_con = self.room['connect'][0]
                y_con = self.room['connect'][1]
                if self.room['direction'] == 'left':
                    x_entry = x_con-1
                    y_entry = y_con+0.5
                    x_exit = x_con+3
                    y_exit = y_con+0.5
                elif self.room['direction'] == 'right':
                    x_entry = x_con+3
                    y_entry = y_con+0.5
                    x_exit = x_con-1
                    y_exit = y_con+0.5
                elif self.room['direction'] == 'down':
                    x_entry = x_con+0.5
                    y_entry = y_con+3
                    x_exit = x_con+0.5
                    y_exit = y_con-1

            else:
                room = self.rooms[self.room['name']+1]
                x_con = room['connect'][0]
                y_con = room['connect'][1]
                if room['direction'] == 'left':
                    x_entry = x_con+3
                    y_entry = y_con+0.5
                    x_exit = x_con-1
                    y_exit = y_con+0.5
                elif room['direction'] == 'right':
                    x_entry = x_con-1
                    y_entry = y_con+0.5
                    x_exit = x_con+3
                    y_exit = y_con+0.5
                elif room['direction'] == 'down':
                    x_entry = x_con+0.5
                    y_entry = y_con-1
                    x_exit = x_con+0.5
                    y_exit = y_con+3

                    

            
            if distance(self.x, self.y, x_exit*TILE_SIZE,y_exit*TILE_SIZE)<TILE_SIZE*5:
                self.horizontal = x_exit*TILE_SIZE - self.x
                self.vertical = y_exit*TILE_SIZE - self.y
            else:
                self.horizontal = x_entry*TILE_SIZE - self.x
                self.vertical = y_entry*TILE_SIZE - self.y
                    
        self.norm = math.sqrt(self.horizontal**2+self.vertical**2)
        if self.norm != 0:
            self.cos = self.horizontal/self.norm
            self.sin = self.vertical/self.norm
        else:
            self.cos = 0
            self.sin = 0

class EnemyGroup: #simulates a group of enemies to not load them directly (those who come from above)
    def __init__(self,app, room, dic_enemies={'spider':0}):
        self.app = app
        self.rooms = app.rooms
        self.room = self.rooms[room]

        self.dic_enemies = dic_enemies
        self.loaded = False
    def update(self):
        if on_tick(120*2):
            if self.room['name']+1 <= len(self.rooms):
                self.room = self.rooms[self.room['name']+1]

class Bullet: #Creates a bullet that can collide and deal damage
    def __init__(self, app, x, y, width, height, vector, gun, owner, shot):
        self.app = app
        self.world = app.world
        self.player = app.player

        self.physics = Physics(self, self.world)


        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale = 1
        self.vector = vector

        self.gun = gun

        self.image = gun["bullet_image"]

        self.damage = gun["damage"]
        self.range = gun["range"]
        self.speed = gun["bullet_speed"]
        self.explode_radius = gun["explode_radius"]
        self.piercing = gun["piercing"]
        self.knockback_coef = gun["knockback_coef"]

        self.owner = owner
        self.shot = shot
        self.type = "bullet"
        
        
        loadedEntities.append(self) #As long as the bullet is a part of this list, it exists

    def update(self): #All the things we need to run every frame
        self.physics.move(self.vector, self.speed)
        self.check_hit()
        self.bullet_destroyed()
    
    def check_hit(self): #Checks if its hit an enemy (if created by the player) or the player (if created by an enemy) and deals damage
        for entity in loadedEntities:
            if self.owner == "player" and entity.type == "enemy" and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]) and self not in entity.pierced and self.piercing>=0 and (not entity.hitStun or entity.lastHitBy == self.shot):
                entity.health -= self.damage
                entity.hitStun = True
                entity.lastHitBy = self.shot
                if "movement" in entity.abilities.keys():
                    if entity.hitFrame<=10:
                        if "lunge" in entity.abilities.keys():
                            if entity.lungeState == "notLunging":
                                entity.apply_knockback(self.vector, self.damage, self.knockback_coef)
                        else:
                            entity.physics.move(self.vector, self.damage, self.knockback_coef)
                if self.piercing != 0:
                    entity.pierced.append(self)
                    self.damage *= self.player.pierceDamage
                self.piercing -= 1
        if self.owner=="enemy" and collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]) and self.piercing>=0:
            self.player.health -= self.damage
            self.piercing -= 1
            self.player.isHit = True
            self.player.hitFrame = 0
        self.range -= math.sqrt((self.vector[0]*self.speed)**2+(self.vector[1]*self.speed)**2)
    
    def bullet_destroyed(self): #Checks if the bullet should destroy itself
        if self.physics.collision_happened or self.range <= 0 or self.piercing<0:
            if self.explode_radius > 0:
                Effect(5,[1*TILE_SIZE, 6*TILE_SIZE], {0:6, 1:6, 2:6, 3:6, 4:6}, self.x, self.y, TILE_SIZE, TILE_SIZE)
                for entity in loadedEntities:
                    if entity.type == "enemy":
                        horizontal = entity.x+entity.width/2 - self.x+self.width/2
                        vertical = entity.y+entity.height/2 - self.y+self.height/2
                        norm = math.sqrt(horizontal**2 + vertical**2)
                        if norm <= self.explode_radius:
                            entity.health -= self.damage
                            entity.hitStun = True
                            entity.knockback = 2
            loadedEntities.remove(self)

class PickUp: #Creates an object on the ground the player can pickup
    def __init__(self, x, y, type, object, player):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = object["image"]
        self.type = type
        self.object = object
        self.player = player
        self.scale = 1
        loadedEntities.append(self)
        pickUpsOnGround.append(self)

    def update(self): #Checks if the player picked up the object
        if collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]):
            if pyxel.btnp(pyxel.KEY_E):
                if self.type == "weapon":
                    self.player.changeWeapon(self.object)
                if self.type == "item":
                    self.player.getItem(self.object)
                    if self.object['name'] == 'Fuel':
                        pyxel.play(2,46)
                loadedEntities.remove(self)
                pickUpsOnGround.remove(self)

class ItemList: #Lists every item and its properties
    def __init__(self):
        self.SPEED_PASSIVE = {"name":"Jet speedup", "description":"Movement speed increase", "image":[1*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["speed", "addition", 0.05, False]]}
        self.HEALTH_PASSIVE = {"name":"Armor Plating", "description":"Health increase", "image":[0*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["max_health", "addition", 5, False], ["health", "addition", 5, False]]}
        self.RANGE_PASSIVE = {"name":"Aerodynamism", "description":"Range increase", "image":[2*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["range", "multiplication", 1.2, True]]}
        self.PIERCING_PASSIVE = {"name":"Sharpened Rounds", "description":"Pierce increase", "image":[3*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["piercing", "addition", 1, True]]}
        self.SPREAD_PASSIVE = {"name":"Iron Sight", "description":"Precision increase", "image":[4*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["spread", "multiplication", 0.9, True]]}
        self.HEAL_KILL = {"name":"Filth Blood", "description":"On kill : Heal", "image":[0*TILE_SIZE,9*TILE_SIZE], "trigger":"onKill", "effect":"stat", "function":[["health", "addition", 2, False]]}
        self.AMMO_KILL = {"name":"Blood Bullets", "description":"On kill : Gain ammo", "image":[2*TILE_SIZE,9*TILE_SIZE], "trigger":"onKill", "effect":"stat", "function":[["mag_ammo", "addition", 1, True]]}
        self.SPEED_KILL = {"name":"Hot Blood", "description":"On kill : Speed boost", "image":[4*TILE_SIZE,9*TILE_SIZE], "trigger":"onKill", "effect":"boost", "function":[["speed", "addition", 0.05, 1*120, False]]}
        self.DAMAGE_DASH = {"name":"Terminal Velocity", "description":"On dash : Damage boost", "image":[3*TILE_SIZE,9*TILE_SIZE], "trigger":"onDash", "effect":"boost", "function":[["damage", "addition", 3, 1.5*120, False], ["damage", "addition", 3, 1.5*120, True]]}
        self.SPEED_DASH = {"name":"Reactor Boost", "description":"On dash : speed boost", "image":[1*TILE_SIZE,8*TILE_SIZE], "trigger":"onDash", "effect":"boost", "function":[["speed", "addition", 0.1, 1.5*120, False], False]}
        self.common_list = [self.SPEED_PASSIVE, self.HEALTH_PASSIVE, self.RANGE_PASSIVE, self.PIERCING_PASSIVE, self.SPREAD_PASSIVE, self.HEAL_KILL, self.AMMO_KILL, self.SPEED_KILL, self.DAMAGE_DASH, self.SPEED_DASH]
        
        self.DASH_DAMAGE_PASSIVE = {"name":"Crowd Burner", "description":"Dash deals damage", "image":[6*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["dashDamage", "addition", 10, False]]}
        self.HEAL_RELOAD = {"name":"Core stabilization", "description":"On reload : Heal", "image":[7*TILE_SIZE,8*TILE_SIZE], "trigger":"onReload", "effect":"stat", "function":[["health", "addition", 5, False]]}
        self.DAMAGE_PASSIVE = {"name":"Burning Bullets", "description":"Damage increase", "image":[7*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["damage", "addition", 5, True], ["damage", "addition", 5, False]]}
        self.MAX_AMMO_PASSIVE = {"name":"Arm attachment", "description":"Max ammo increase", "image":[8*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["max_ammo", "multiplication", 1.1, True]]}
        self.FIRERATE_KILL = {"name":"Overheat", "description":"On kill : Firerate boost", "image":[8*TILE_SIZE,9*TILE_SIZE], "trigger":"onKill", "effect":"boost", "function":[["cooldown", "multiplication", 0.8, 2*FPS, True]]}
        self.uncommon_list = [self.DASH_DAMAGE_PASSIVE, self.HEAL_RELOAD, self.DAMAGE_PASSIVE, self.MAX_AMMO_PASSIVE, self.FIRERATE_KILL]

        self.BULLET_COUNT_PASSIVE = {"name":"Extra Gun", "description":"Double bullets", "image":[6*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["bullet_count", "multiplication", 2, True]]}
        self.LUCK_PASSIVE = {"name":"Compatibility plug / Clover Charm", "description":"Increased chance of getting items", "image":[9*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["luck", "addition", 1, False]]}
        self.PIERCING_DAMAGE_PASSIVE = {"name":"Blood Acceleration", "description":"Damage increase with piercing", "image":[9*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["pierceDamage", "multiplication", 1.5, False]]}
        self.legendary_list = [self.BULLET_COUNT_PASSIVE, self.LUCK_PASSIVE, self.PIERCING_DAMAGE_PASSIVE]

        self.FUEL = {"name":"Fuel", "description":"Keep the ship moving", "image":[5*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat", "function":[["fuel", "addition", 1, False]]}

class Effect: #Used to generate collision-less effects like explosions
    def __init__(self, length, image, durations, x, y, width, height):
        self.length = length
        self.image = image
        self.durations = durations
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = "effect"
        self.scale = 1.5

        self.state = 0
        self.frame = 0
        
        loadedEntities.append(self)
    
    def update(self): #Used for animating the effect
        if self.frame == self.durations[self.state]:
            self.image[0] += TILE_SIZE
            self.state += 1
            self.frame = 0
        if self.state == self.length :
            loadedEntities.remove(self)
        self.frame += 1

class ScreenEffect: #effects that cover the whole screen
    def __init__(self, player):
        self.player = player
        self.redscreen = False
        self.red_dither = 0

        self.explo_screen = False
        self.explo_dither = 0
        self.explo_frame = -140

    def update(self):
        if self.player.isHit:
            self.redscreen = True
            if self.player.hitLength > self.player.hitFrame:
                self.red_dither = (self.player.hitLength - self.player.hitFrame)/self.player.hitLength - 0.5
                if self.red_dither<0:
                    self.red_dither = 0
            else:
                self.red_dither = 0
                self.redscreen = False
        if self.explo_screen:
            self.explo_dither = (pyxel.frame_count - self.explo_frame)/180

class Boost: #Gives a temporary stat boost to the player
    def __init__(self, stat, operation, value, duration, gun, player, creator):
        self.stat = stat
        self.operation = operation
        self.value = value
        self.duration = duration
        self.gun = gun
        self.frame = 0
        self.player = player
        self.player.increaseStat(self.stat, self.operation, self.value, self.gun)
        activeBoosts.append(self) #The boost is active as long as its a part of this list
        self.creator = creator

    def update(self): #Once the boost is over, we reverse its effect
        if self.frame >= self.duration:
            if self.operation == "addition":
                self.player.increaseStat(self.stat, self.operation, -self.value, self.gun)
            elif self.operation == "multiplication":
                self.player.increaseStat(self.stat, self.operation, 1/self.value, self.gun)
            activeBoosts.remove(self)
        self.frame += 1

class Camera: #makes the camera move wth the player
    def __init__(self):
        self.x = (WIDTH//2-6)*TILE_SIZE
        self.y = 0
        self.margin = 3/8
    
    def update(self,player):
        if player.x  < self.x + CAM_WIDTH * self.margin and self.x >0:
            self.x = player.x - CAM_WIDTH * self.margin
        if player.x + TILE_SIZE  > self.x + CAM_WIDTH * (1-self.margin) and self.x + CAM_WIDTH < WIDTH *TILE_SIZE:
            self.x = player.x + TILE_SIZE - CAM_WIDTH * (1-self.margin)
        if player.y  < self.y + CAM_HEIGHT * self.margin and self.y >0:
            self.y = player.y - CAM_HEIGHT * self.margin
        if player.y + TILE_SIZE  > self.y + CAM_HEIGHT * (1-self.margin) and self.y + CAM_HEIGHT < HEIGHT * TILE_SIZE:
            self.y = player.y + TILE_SIZE - CAM_HEIGHT * (1-self.margin)

        if self.x<0:
            self.x = 0
        if self.x + CAM_WIDTH > WIDTH*TILE_SIZE:
            self.x = WIDTH*TILE_SIZE - CAM_WIDTH
        if self.y<0:
            self.y = 0
        if self.y - CAM_HEIGHT > HEIGHT*TILE_SIZE:
            self.y = HEIGHT*TILE_SIZE-CAM_HEIGHT
        
        self.x, self.y = round(self.x),round(self.y)

class Info: #accessible by all, acts as a global kind of
    def __init__(self):
        self.description = ['N/A']

def draw_screen(u, v,camx,camy): #draws on the whole screen a pattern of 16 by 16 on the pyxres
    for y in range(CAM_HEIGHT//2):
        for x in range(CAM_WIDTH//2):
            pyxel.blt(
                camx+x*16,
                camy+y*16,
                1,
                u,
                v,
                16,
                16
            )

def check_entity(loadedEntities, key, value): #unused
    for entity in loadedEntities:
        if getattr(entity,key) == value:
            return True
    return False
    
def on_tick(tickrate=60,delay=0): #allows the computer to make operations only on certain times to not do averything 120 times a second
    return (pyxel.frame_count % tickrate)-delay == 0

def on_cooldown(frame,cooldown): #checks if a timer is up or not
    return (pyxel.frame_count - frame) < cooldown

def distance(x1,y1,x2,y2): #looks at distance with pythagorean theorem
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def tuple_list_sort(list): #unused
    for i in range(len(list)-1):
        min=list[i][0]
        index=i
        for j in range(len(list)-1-i):
            if list[i+j][0]<min:
                min=list[i+j][0]
                index=i+j
        list[i], list[index] = list[index], list[i]
    return list
        

def dic_copy(dico): #copy doesnt exist elsewhere i am in denial
    dicoC = {}
    for key in dico.keys():
        dicoC[key]=dico[key]
    return dicoC


def list_copy(listP): #same
    listC = []
    for i in range(len(listP)):
        listC.append(listP[i])
        return listC

def rooms_collide(world, x, y, w, h): #checks if 2 rooms collide
    for in_y in range(h+2):
        for in_x in range(w+2):
            if world[y+in_y-1][x+in_x-1] == WorldItem.GROUND:
                return True
    return False

def rect_place(world_map, x, y, w, h, block): #places a rectangle of blocks in the world map
    for in_y in range(h):
        for in_x in range(w):
            world_map[y+in_y][x+in_x] = block

def world_item_draw(pyxel,x,y,block): #draw a singular block
    pyxel.blt(
        x*TILE_SIZE,
        y*TILE_SIZE,
        0,
        block[0]*TILE_SIZE,
        block[1]*TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE
    )

def list_dic_find(list,value,key):
    for dic in list:
        if dic[key] == value:
            return dic
    return None

def find_room(x,y,rooms): #can find in wich room the coordinates are
    rooms_distance = []
    for room in rooms:
        if (x >= room['X'] and x < room['X']+room['W'] and y >= room['Y'] and y < room['Y']+room['H']) or (x >= room['connect'][0] and x < room['connect'][0]+2 and y >= room['connect'][1] and y < room['connect'][1]+2):
            return room
        rooms_distance.append((distance(x,y,room['X'],room['Y']),room))
    rooms_distance = tuple_list_sort(rooms_distance)
    return rooms_distance[0][1]

pickUpsOnGround = []
activeBoosts = []

def in_camera(x,y, camx, camy): #checks if coordinates are inside the camera view
    return in_perimeter((camx + CAM_WIDTH//2)//TILE_SIZE,(camy + CAM_HEIGHT//2)//TILE_SIZE, x, y, CAM_WIDTH//(TILE_SIZE*2) + 1)

def collision(x1, y1, x2, y2, size1, size2): #Checks if object1 and object2 are colliding with each other
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1

def import_csv(file) :
    tab = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            tab.append(line)
    return tab

def export_csv(file, data):
    with open(file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())

App()