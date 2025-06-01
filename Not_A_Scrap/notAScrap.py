import pyxel, os, random, math

WIDTH = 200
HEIGHT = 200
TILE_SIZE = 8

CAM_WIDTH = 16*8
CAM_HEIGHT = 16*8

FPS = 120

loadedEntities = []

class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(CAM_WIDTH,CAM_HEIGHT,title='Not a Scrap', fps=FPS)
        pyxel.load('../notAScrap.pyxres')
        pyxel.playm(0, loop=True)

        self.camera = Camera()
        self.world = World(pyxel.tilemaps[0],RoomBuild(0,WIDTH//2,10),'ship')
        self.itemList = ItemList()
        self.info = Info()
        self.player = Player(self.world, self.camera,self.itemList,self.info)
        self.effects = ScreenEffect(self.player)
        self.anim = Animation()

        self.ship_broken =  False
        self.ship_hold_time = 120*120
        self.explosion_time = 40*120
        self.group_alive = False
        self.game_start = 0
        self.game_state = 'ship'
        self.enemy_bar = 32
        self.rooms = self.world.roombuild.rooms

        
        pyxel.mouse(True)

        pyxel.run(self.update,self.draw)
    

    def update(self):
        if self.game_state == 'bunker':
            self.update_in_bunker()
        if self.game_state == 'ship':
            self.update_in_ship()

    
    def draw(self):
        if self.game_state == 'bunker':
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
            self.draw_help()
            self.draw_timer_bar()

        if self.game_state == 'ship':
            self.draw_ship_outside()
            self.draw_ship()
            self.draw_player()
            self.draw_help()

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
                        colkey=11)
    
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
            pyxel.dither(self.effects.dither)
            draw_screen(
                0,
                16,
                self.camera.x,
                self.camera.y,)
        pyxel.dither(1)

    def draw_timer_bar(self):
        pyxel.blt(self.camera.x + 96,self.camera.y,1,0,32,32,4)
        pyxel.blt(self.camera.x + 96,self.camera.y,1,0,36,32,4)
        if self.enemy_bar>0:
            pyxel.blt(self.camera.x + 96,self.camera.y,1,0,40,self.enemy_bar+1,4)

    def draw_stats(self):
        pyxel.text(self.camera.x+1, self.camera.y+1, "Health:"+str(self.player.health)+"/"+str(self.player.max_health),8)
        pyxel.text(self.camera.x+1, self.camera.y+7, "Weapon:"+str(self.player.gun["name"]),7)
        pyxel.text(self.camera.x+1, self.camera.y+13, "Ammo:"+str(self.player.gun["ammo"])+"/"+str(self.player.gun["max_ammo"]),7)
        pyxel.text(self.camera.x+96, self.camera.y+8, "Fuel:"+str(self.player.fuel),7)
        if self.player.gun["ammo"] < self.player.gun["max_ammo"]:
            pyxel.text(self.camera.x+1, self.camera.y+19, "[R] to reload", 7)

    def draw_help(self):
        if self.info.description != ["N/A"]:
            pyxel.text(self.camera.x+1, self.camera.y+107, self.info.description[0], 7)
            pyxel.text(self.camera.x+1, self.camera.y+113, self.info.description[1], 7)
            pyxel.text(self.camera.x+1, self.camera.y+119, self.info.description[2], 7)

    def draw_ship_outside(self):
        pyxel.cls(0)
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
                        Enemy(X_pos*TILE_SIZE,Y_pos*TILE_SIZE,enemy,self.player,self.world,self.itemList)

    def spawn_enemies_at(self,x,y,dic,always_loaded=False):
        print(x,y,'spawn')
        for enemy in EnemyTemplates.ENEMY_LIST:
            if enemy['name'] in dic.keys():
                for i in range(dic[enemy['name']]):
                    Enemy(x*TILE_SIZE,y*TILE_SIZE,enemy,self.player,self.world,self.itemList,always_loaded)

    def update_in_ship(self):
        self.camera.x,self.camera.y = 0,0
        self.anim.loop(6,10,32,24,[0,1])
        self.anim.slide_anim(10,3,WorldItem.UPWORLD_FLOOR)
        self.player.update_in_ship()
        if self.player.lever_pulled:
            self.game_state = 'bunker'
            self.restartGame()

    def update_in_bunker(self):
        self.update_effects()
        self.effects.update()

        if self.player.alive:
            self.player.update()
            for entity in loadedEntities:
                entity.update()

            for boost in activeBoosts:
                boost.update()
 
            if not on_cooldown(self.game_start,self.ship_hold_time) and self.group_alive:
                if self.group.room['name'] < self.player.room['name'] - 3:
                    self.group.update()
                else:
                    self.spawn_enemies_at(self.group.room['X'],self.group.room['Y'],self.group.dic_enemies,True)
                    self.group_alive = False
            if on_cooldown(self.game_start,self.ship_hold_time):
                self.enemy_bar =  (self.ship_hold_time-pyxel.frame_count+self.game_start) * 32 // self.ship_hold_time
            elif on_cooldown(self.ship_hold_time,self.explosion_time):
                self.explosion_bar =  (self.ship_hold_time+self.explosion_time-pyxel.frame_count+self.game_start) * 32 // self.ship_hold_time+self.explosion_time


            self.camera.update(self.player)
            pyxel.camera(self.camera.x,self.camera.y)
        
        if on_tick(60):
            if not self.player.alive:
                self.restartGame()
            else:
                if pyxel.frame_count - self.game_start >= self.ship_hold_time and not self.ship_broken:
                    self.ship_broken = True
                    self.group = EnemyGroup(self.rooms,self.rooms[0],{'spider':7,'hive_queen':1,'stalker':3,'bulwark':1})
                    self.group_alive = True
        self.check_win()

    def update_effects(self):
        for slash in self.world.effects:
            if pyxel.frame_count - slash['time'] > 60:
                self.world.effects.remove(slash)

    def check_win(self):
        if in_perimeter(self.player.x,self.player.y,814,40,10):
            if self.player.fuel >= 5:
                self.info.description = ['[F] to escape','the explosion','']
                if pyxel.btnp(pyxel.KEY_F):
                    self.player.fuel += -5
                    self.game_state = 'ship'
                    self.world.__init__(pyxel.tilemaps[0],RoomBuild(0,WIDTH//2,10),'ship')
                    self.player.x = 60
                    self.player.y = 70
                    pyxel.camera(0,0)
                    self.camera.x,self.camera.y = 0,0
            else:
                self.info.description = ['Needs 5 fuel to start','','']

    def restartGame(self):
        global pickUpsOnGround
        global loadedEntities
        global activeBoosts
        loadedEntities = []
        pickUpsOnGround = []
        activeBoosts = []

        self.camera.__init__()
        self.world.__init__(pyxel.tilemaps[0],RoomBuild(0,WIDTH//2,10),'bunker')
        self.itemList.__init__()
        if self.player.alive:
            self.player.reset(self.world)
        else:
            self.player.__init__(self.world, self.camera,self.itemList,self.info)
        self.effects.__init__(self.player)
        self.game_start = pyxel.frame_count
        self.ship_broken =  False
        self.ship_hold_time = 120*120
        self.explosion_time = 40*120
        self.group_alive = False
        self.game_state = 'bunker'
        self.rooms = self.world.roombuild.rooms
        pyxel.stop()

        pyxel.mouse(True)
        self.enemies_spawn_in_rooms()      


class Animation:
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

class WorldItem:
    WALL = (0,0)
    GROUND = (0,1)
    CONNECT = (1,1)
    INVISIBLE = (6,0)

    BLOCKS = [WALL,GROUND]
    WALLS = [WALL,INVISIBLE]
    UPWORLD_FLOOR = [(3,0),(2,1),(3,1)]

class World:
    def __init__(self,tilemap,roombuild,game_state):
        self.tilemap = tilemap
        self.roombuild = roombuild
        self.world_map = [[(0,1) for j in range(WIDTH)] for i in range(HEIGHT)]
        self.nb_rooms = 20
        self.effects = []
            
        if game_state == 'bunker':
            self.world_map = [[(0,0) for j in range(WIDTH)] for i in range(HEIGHT)]
            self.player_init_posX = 812/TILE_SIZE
            self.player_init_posY = 45/TILE_SIZE
            self.roombuild.random_rooms_place(self.world_map,20)
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


        elif game_state == 'ship':
            self.world_map = [[(0,1) for j in range(WIDTH)] for i in range(HEIGHT)]
            self.player_init_posX = 60/TILE_SIZE
            self.player_init_posY = 56/TILE_SIZE
            rect_place(self.world_map,4,6,7,1,WorldItem.INVISIBLE)
            rect_place(self.world_map,3,6,1,6,WorldItem.INVISIBLE)
            rect_place(self.world_map,11,6,1,6,WorldItem.INVISIBLE)
            rect_place(self.world_map,4,11,7,1,WorldItem.INVISIBLE)

class RoomBuild:
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
                    self.fix_collide_rooms()
                else:
                    self.room_place_right()

                if self.room_pos == 1 and self.x<WIDTH-self.max_size*2+1:
                    self.room_place_right()
                    self.fix_collide_rooms()
                else:
                    self.room_place_left()

                if self.room_pos == 2:
                    self.room_place_down()

            else:
                self.room_place_down()
            
            rect_place(world_map,self.newConnect[0],self.newConnect[1], 2, 2, WorldItem.CONNECT)
            rect_place(world_map, self.newX, self.newY, self.newW, self.newH, WorldItem.GROUND)
            self.rooms.append({'name':i+1,'X':self.newX,'Y':self.newY,'W':self.newW,'H':self.newH,'connect':(self.newConnect[0],self.newConnect[1]),'direction':self.last_placement})

            self.x, self.y, self.w, self.h, self.connect = self.newX, self.newY, self.newW, self.newH, self.newConnect
        
        self.world_map = world_map
    
    def room_place_left(self):
        self.newConnect[0] = self.x - 2
        self.newConnect[1] = self.y + random.randint(0,self.h-2)
        self.newX = self.newConnect[0] - self.newW
        self.newY = self.newConnect[1] - random.randint(0,self.newH-2)
        self.last_placement = 'left'
    def room_place_right(self):
        self.newConnect[0] = self.x + self.w
        self.newConnect[1] = self.y + random.randint(0,self.h-2)
        self.newX = self.newConnect[0] +2
        self.newY = self.newConnect[1] - random.randint(0,self.newH-2)
        self.last_placement = 'right'
    def room_place_down(self):
        self.newConnect[0] = self.x + random.randint(1,self.w-2)
        self.newConnect[1] = self.y + self.h
        self.newX = self.newConnect[0] - random.randint(0,self.newW-2)
        self.newY = self.newConnect[1] +2
        self.last_placement = 'down'
        
    def fix_collide_rooms(self): #plupart des collisions arrivent a cause de newY trop haut 'dont work'
        collided=False
        for room in self.rooms:
            if not collided:
                if collision(self.newX-1,self.newY-1,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])):
                    collided=True
                    self.room_place_down()

        for room in self.rooms:
            if not collided:
                if collision(self.newX-1,self.newY-1,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])):
                    self.room_place_left()
                    print('tried place left',flush=True)

        for room in self.rooms:
            if not collided:
                if collision(self.newX-1,self.newY-1,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])):
                    self.room_place_right()
                    print('tried place right',flush=True)
        for room in self.rooms:
            if collision(self.newX-1,self.newY-1,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])):
                self.room_place_down()
                print('collision',flush=True)

    def spaceship_walls_place(self):
        rect_place(self.world_map,105,4,1,5,WorldItem.INVISIBLE)
        rect_place(self.world_map,98,4,1,5,WorldItem.INVISIBLE)
        rect_place(self.world_map,99,4,6,1,WorldItem.INVISIBLE)
        rect_place(self.world_map,103,9,2,1,WorldItem.WALL)
        rect_place(self.world_map,99,9,2,1,WorldItem.WALL)

class Furniture:
    def __init__(self,rooms):
        self.rooms = rooms
        chests = []
        for i in range(10):
            room_chest = random.randint(1,len(self.rooms)-1)
            if room_chest in chests:
                for j in range(5):
                    if room_chest in chests:
                        if room_chest<len(self.rooms)-1:
                            room_chest += 1
                        else:
                            room_chest = random.randint(1,len(self.rooms)//2+3)
            chests.append(room_chest)
        
        for index in chests:
            room = self.rooms[index]
            X_pos = random.randint(room['X'],room['X']+room['W']-1)
            Y_pos = random.randint(room['Y'],room['Y']+room['H']-1)
            self.rooms[index]['chest'] = (X_pos,Y_pos)
            self.rooms[index]['chest_opening'] = 0
                

        for room in rooms:
            nb_chest = random.randint(0,2)//2
            X_chest = random.randint(room['X'],room['X']+room['W']-1)
            Y_chest = random.randint(room['Y'],room['Y']+room['H']-1)

class Physics: #This is used to have a common move function
    def __init__(self, world):
        self.world = world
        self.momentum = 0
        self.collision_happened = False

    def move(self, x, y, width, height, vector): #We give a movement vector, and information relating to the thing moving, and we get the new coordinates
        X = int(x//TILE_SIZE)
        Y = int(y//TILE_SIZE)

        #We handle horizontal and vertical movement separatly to make problem solving easier

        new_x = x + vector[0]*self.momentum

        new_X = X+pyxel.sgn(vector[0])
        if vector[0]!=0:
            next_X_1 = self.world.world_map[Y][new_X]
            if y != Y*TILE_SIZE:
                next_X_2 = self.world.world_map[Y+1][new_X]
            else:
                next_X_2 = WorldItem.GROUND
            #If there's enough space for the entity to move, it moves unimpeded
            if (next_X_1 not in WorldItem.WALLS or not collision(new_x, y, new_X*TILE_SIZE, Y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])) and (next_X_2 not in WorldItem.WALLS or not collision(new_x, y, new_X*TILE_SIZE, (Y+1)*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])):
                x = new_x
            #Else If the movement puts the entity in the wall, we snap it back to the border to prevent clipping.
            elif (next_X_1 in WorldItem.WALLS or next_X_2 in WorldItem.WALLS) and new_x+width>X*TILE_SIZE and (X+1)*TILE_SIZE>new_x:
                self.collision_happened = True
                x = (new_X-pyxel.sgn(vector[0]))*TILE_SIZE
        
        X = int(x//TILE_SIZE)

        #We calculate vertical movement in the same way we do horizontal movement

        new_y = y + vector[1]*self.momentum
        new_Y = Y+pyxel.sgn(vector[1])
        if vector[1]!=0:
            next_Y_1 = self.world.world_map[new_Y][X]
            if x != X*TILE_SIZE:
                next_Y_2 = self.world.world_map[new_Y][X+1]
            else:
                next_Y_2 = WorldItem.GROUND
            
            if (next_Y_1 not in WorldItem.WALLS or not collision(x, new_y, X*TILE_SIZE, new_Y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])) and (next_Y_2 not in WorldItem.WALLS or not collision(x, new_y, (X+1)*TILE_SIZE, new_Y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])):
                y = new_y
            elif (next_Y_1 in WorldItem.WALLS or next_Y_2 in WorldItem.WALLS) and new_y+height>Y*TILE_SIZE and (Y+1)*TILE_SIZE>new_y:
                self.collision_happened = True
                y = (new_Y-pyxel.sgn(vector[1]))*TILE_SIZE

        return x,y

class Player: #Everything relating to the player and its control
    def __init__(self, world, camera,itemList,info):
        self.alive = True
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.physics = Physics(world)
        self.camera = camera
        self.info = info

        self.image = (1,3)
        self.facing = [1,0]
        self.last_facing = [1,0]

        self.speed = 0.25
        self.speedFallOff = 4
        self.isDashing = False
        self.dashCooldown = 40
        self.dashLength = 20
        self.dashFrame = 0
        self.dashStrength = self.speed*2.5
        self.dashDamage = 0
        
        self.stuck = False
        self.open_time = 240
        self.itemList = itemList

        self.gun = dic_copy(Guns.PISTOL)
        self.attackFrame = 0
        self.damage = 10
        self.slash_cooldown = 0.5*120
        self.slashFrame = 0
        self.pierceDamage = 1

        self.ownedItems = []
        self.justKilled = False

        self.fuel = 0
        self.reset(world)

    def reset(self,world):
        self.world = world
        self.x = world.player_init_posX*TILE_SIZE
        self.y = world.player_init_posY*TILE_SIZE
        self.rooms = self.world.roombuild.rooms
        self.room = self.rooms[0]

        self.lever_pulled = False
        self.no_text = False
        self.luck = 0

        self.health = 50
        self.max_health = 50
        self.hitFrame = 0
        self.hitLength = 120
        self.isHit = False
        self.pickup_text = ["N/A"]
        
    def update(self): #All the things we run every frame to make the player work
        self.no_text = True

        if pyxel.btnp(pyxel.KEY_A):
            print(self.room['name'],self.room['X'], self.room['Y'], self.speed,self.x,self.y)

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
        self.chest_gestion()
        self.description_text()
        self.change_PickupText()
        self.check_death()

        if self.health > self.max_health:
            self.health = self.max_health
        if self.gun["ammo"] > self.gun["max_ammo"]:
            self.gun["ammo"] = self.gun["max_ammo"]
        
    def update_in_ship(self): #All the things we run every frame while the player is in the ship
        if pyxel.btnp(pyxel.KEY_A):
            print(self.x//TILE_SIZE,self.y//TILE_SIZE)
        
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
            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [-1,0])
            self.facing[0] = -1
            self.image = (1,2)
        if pyxel.btn(pyxel.KEY_D):
            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [1,0])
            self.facing[0] = 1
            self.image = (0,2)
        if pyxel.btn(pyxel.KEY_Z):
            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [0,-1])
            self.facing[1] = -1
            self.image = (0,3)
        if pyxel.btn(pyxel.KEY_S):
            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [0,1])
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

        if (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S))and self.physics.momentum <= self.speed and not self.stuck:
            self.physics.momentum = self.speed
        else:
            self.physics.momentum /= self.speedFallOff

    def fireWeapon(self): #Fire the player's gun when they right-click
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.attackFrame>=self.gun["cooldown"] and self.gun["ammo"]>0:
            pyxel.play(2,60)
            pyxel.play(3,61)
            self.attackFrame = 0
            self.gun["ammo"] -= 1
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
                Bullet(self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.gun["damage"], self.gun["bullet_speed"], self.gun["range"], self.gun["piercing"], self.world, self, (0,6*TILE_SIZE), "player", self.gun["explode_radius"])

    def chest_gestion(self):
        if 'chest' in self.room.keys():
            if in_perimeter(self.x,self.y,self.room['chest'][0]*TILE_SIZE,self.room['chest'][1]*TILE_SIZE,TILE_SIZE*1.5):
                if self.no_text:
                    self.pickup_text = ['Hold [F] to open', 'Chest', 'Get item or weapon']
                    self.no_text = False

                if pyxel.btn(pyxel.KEY_F):
                    print(self.room['chest_opening'])
                    self.stuck = True
                    self.physics.momentum /= self.speedFallOff
                    self.room['chest_opening'] += 1

                    if self.room['chest_opening'] >= self.open_time:
                        self.spawn_item(self.room['chest'][0],self.room['chest'][1])
                        self.world.world_map[self.room['chest'][1]][self.room['chest'][0]] = WorldItem.GROUND
                        self.room.pop('chest')
                        self.room.pop('chest_opening')
                        self.stuck = False
                else:
                    self.stuck = False
                    self.room['chest_opening'] = 0

    def spawn_item(self,x,y):

        pickup = random.randint(1,3)
        if pickup == 1:
            item_random = random.randint(0, len(self.itemList.common_list)-1)
            item = self.itemList.common_list[item_random]
            PickUp(x*TILE_SIZE, y*TILE_SIZE, "item", item, self)

        elif pickup >= 2:
            gun_random = random.randint(26,100)
            for gun in Guns.Gun_list:
                if gun_random in gun["rate"]:
                    PickUp(x*TILE_SIZE, y*TILE_SIZE, "weapon", gun, self)

    def reloadWeapon(self): #Makes the player reload its weapon when it reaches 0 or presses R
        if pyxel.btnp(pyxel.KEY_R) and self.gun["ammo"]<self.gun["max_ammo"] and self.gun["ammo"]!=0:
            self.gun["ammo"] = 0
            self.attackFrame = 0
            
        if self.gun["ammo"]==0 and self.attackFrame>=self.gun["reload"]:
            self.gun["ammo"]=self.gun["max_ammo"]
            self.triggerOnReloadItems()
            
    def slash(self):
        if (pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btn(pyxel.KEY_C)) and self.slashFrame>=self.slash_cooldown:
            self.slashFrame = 0
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
                    entity.health -= self.damage
                    entity.hitStun = True
                    entity.knockback = 2

    def dash(self): #Start the dash when the player presses space
        if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_SHIFT)) and self.dashFrame >= self.dashCooldown:
            self.isDashing = True
            self.dashFrame = 0
            self.physics.momentum = self.speed*2.5
            self.image = [6,2]

    def dashMovement(self): #Does the movement while the player is dashing
        self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.facing)
        if self.dashDamage > 0:
            for entity in loadedEntities:
                if entity.type == "enemy" and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]) and not entity.hitByDash:
                    entity.health -= self.dashDamage
                    entity.hitStun = True
                    entity.hitByDash = True
                    entity.knockback = 0.5
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

    def preventOOB(self): #Prevents the player going out of bounds
        if self.x<0:
            self.x = 0
        if self.y<0:
            self.y = 0
        if self.x > WIDTH*TILE_SIZE:
            self.x = (WIDTH-1)*TILE_SIZE
        if self.y > HEIGHT*TILE_SIZE:
            self.y = (HEIGHT-1)*TILE_SIZE

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
        self.ownedItems.append(item)
        if item["trigger"] == "passive" and (item["effect"] == "stat_p" or item["effect"] == "stat_g"):
            for change in item["function"]:
                self.increaseStat(change[0], change[1], change[2])

    def changeWeapon(self, gun): #Allows the player to change guns, randomize its values slightly, and then reapplies item effects for it to work 
        self.gun = dic_copy(gun)
        for key in self.gun.keys():
            if key not in ["name", "description", "image", "rate", "bullet_count"]:
                lowest_value = self.gun[key]*0.9
                highest_value = self.gun[key]*1.1
                self.gun[key] = random.uniform(lowest_value, highest_value)
        for item in self.ownedItems:
            if item["trigger"] == "passive" and item["effect"]=="stat_g":
                for change in item["function"]:
                    self.increaseStat(change[0], change[1], change[2])
        for boost in activeBoosts:
            if boost.target == "boost_g":
                self.increaseStat(boost.stat, boost.operation, boost.value)
        self.gun["piercing"] = math.ceil(self.gun["piercing"])
        self.gun["max_ammo"] = math.ceil(self.gun["max_ammo"])
        self.gun["ammo"] = self.gun["max_ammo"]

    def increaseStat(self, stat, operation, value): #I despise this function, but it just does what the name implies
        if stat == "health":
            if operation == "addition":
                self.health += value
            elif operation == "multiplication":
                self.health *= value
        elif stat == "max_health":
            if operation == "addition":
                self.max_health += value
            elif operation == "multiplication":
                self.max_health *= value
        elif stat == "speed":
            if operation == "addition":
                self.speed += value
            elif operation == "multiplication":
                self.speed *= value
            if self.speed  > 1.9*TILE_SIZE:
                self.speed = 1.9*TILE_SIZE
        elif stat == "dash_cooldown":
            if operation == "addition":
                self.dashCooldown += value
            elif operation == "multiplication":
                self.dashCooldown *= value
        elif stat == "damage":
            if operation == "addition":
                self.gun["damage"] += value
            elif operation == "multiplication":
                self.gun["damage"] *= value
        elif stat == "range":
            if operation == "addition":
                self.gun["range"] += value
            elif operation == "multiplication":
                self.gun["range"] *= value
        elif stat == "spread":
            if operation == "addition":
                self.gun["spread"] += value
            elif operation == "multiplication":
                self.gun["spread"] *= value
        elif stat == "piercing":
            if operation == "addition":
                self.gun["piercing"] += value
            elif operation == "multiplication":
                self.gun["piercing"] *= value
        elif stat == "bullet_speed":
            if operation == "addition":
                self.gun["bullet_speed"] += value
            elif operation == "multiplication":
                self.gun["bullet_speed"] *= value
        elif stat == "max_ammo":
            if operation == "addition":
                self.gun["max_ammo"] += value
            elif operation == "multiplication":
                self.gun["max_ammo"] *= value
            self.gun["max_ammo"] = math.ceil(self.gun["max_ammo"])
        elif stat == "ammo":
            if operation == "addition":
                self.gun["ammo"] += value
            elif operation == "multiplication":
                self.gun["ammo"] *= value
            self.gun["ammo"] = math.ceil(self.gun["ammo"])
        elif stat == "reload":
            if operation == "addition":
                self.gun["reload"] += value
            elif operation == "multiplication":
                self.gun["reload"] *= value
        elif stat == "gun_cooldown":
            if operation == "addition":
                self.gun["cooldown"] += value
            elif operation == "multiplication":
                self.gun["cooldown"] *= value
        elif stat == "bullet_count":
            if operation == "addition":
                self.gun["bullet_count"] += value
            elif operation == "multiplication":
                self.gun["bullet_count"] *= value
            self.gun["bullet_count"] = math.ceil(self.gun["bullet_count"])
        elif stat == "dash_damage":
            if operation == "addition":
                self.dashDamage += value
            elif operation == "multiplication":
                self.dashDamage *= value
        elif stat == "luck":
            if operation == "addition":
                self.luck += value
            elif operation == "multiplication":
                self.luck *= value
        elif stat == "pierce_damage":
            if operation == "addition":
                self.pierceDamage += value
            elif operation == "multiplication":
                self.pierceDamage *= value
        
    def triggerOnKillItems(self): #Self-explanatory
        for item in self.ownedItems:
            if item["trigger"] == "onKill":
                if item["effect"] == "stat_p" or item["effect"] == "stat_g":
                    for change in item["function"]:
                        self.increaseStat(change[0], change[1], change[2])
                elif item["effect"] == "boost_p" or item["effect"] == "boost_p":
                    for change in item["function"]:
                        Boost(change[0], change[1], change[2], change[3], item["effect"], self, item)

    def triggerOnReloadItems(self): #Self-explanatory
        for item in self.ownedItems:
            if item["trigger"] == "onReload":
                if item["effect"] == "stat_p" or item["effect"] == "stat_g":
                    for change in item["function"]:
                        self.increaseStat(change[0], change[1], change[2])
                elif item["effect"] == "boost_p" or item["effect"] == "boost_p":
                    for change in item["function"]:
                        Boost(change[0], change[1], change[2], change[3], item["effect"], self, item)
        
    def triggerOnDashItems(self): #Self-explanatory
        for item in self.ownedItems:
            if item["trigger"] == "onDash":
                if item["effect"] == "stat_p" or item["effect"] == "stat_g":
                    for change in item["function"]:
                        self.increaseStat(change[0], change[1], change[2])
                elif item["effect"] == "boost_p" or item["effect"] == "boost_p":
                    for change in item["function"]:
                        boost_already_active = False
                        for boost in activeBoosts: #Si l'item est déja actif, on remet son timer à 0, sinon, on créé un boost
                            if boost.creator == item:
                                boost_already_active = True
                                boost.frame = 0
                        if not boost_already_active:
                            Boost(change[0], change[1], change[2], change[3], item["effect"], self, item)

class EnemyTemplates:
    SPIDER = {'name':'spider',"health":50, "speed":0.36, "damage":5, "range":1*TILE_SIZE, "attack_freeze":40, "attack_cooldown":120, "attack_speed":1.5, "lunge_range":6*TILE_SIZE, "lunge_freeze":40, "lunge_length":20, "lunge_speed":1,"lunge_cooldown":random.randint(2,6)*120//2, "image":(0*TILE_SIZE,12*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, "takes_knockback":True, "can_lunge":True, "attack":"slash", "spawner":False, "has_items":False, 'spawning_chance':[x for x in range(0,45)]}
    BULWARK = {'name':'bulwark',"health":150, "speed":0.18, "damage":15, "range":1*TILE_SIZE, "attack_freeze":40, "attack_cooldown":120, "attack_speed":1.5, "lunge_range":6*TILE_SIZE, "lunge_freeze":40, "lunge_length":15, "lunge_speed":1,"lunge_cooldown":random.randint(2,6)*120//2, "image":(0*TILE_SIZE,18*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, "takes_knockback":False, "can_lunge":True, "attack":"slash", "spawner":False, "has_items":False, 'spawning_chance':[x for x in range(65,75)]}
    STALKER = {'name':'stalker',"health":50, "speed":0.1, "damage":5, "range":1*TILE_SIZE, "attack_freeze":40, "attack_cooldown":120, "attack_speed":1.5, "lunge_range":12*TILE_SIZE, "lunge_freeze":60, "lunge_length":20, "lunge_speed":3,"lunge_cooldown":random.randint(2,6)*120//2, "image":(0*TILE_SIZE,14*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, "takes_knockback":True, "can_lunge":True, "attack":"lunge", "spawner":False, "has_items":False, 'spawning_chance':[x for x in range(45,65)]}
    TUMOR = {'name':'tumor',"health":50, "speed":0.36, "damage":5, "range":1*TILE_SIZE, "attack_freeze":40, "attack_cooldown":120, "attack_speed":1.5, "lunge_range":6*TILE_SIZE, "lunge_freeze":40, "lunge_length":20, "lunge_speed":1,"lunge_cooldown":random.randint(2,6)*120//2, "image":(0*TILE_SIZE,24*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, "takes_knockback":True, "can_lunge":True, "attack":"collision", "spawner":False, "has_items":False, 'spawning_chance':[x for x in range(75,82)]}
    TURRET = {'name':'turret',"health":50, "speed":0, "damage":5, "range":7*TILE_SIZE, "attack_freeze":0, "attack_cooldown":0.5*FPS, "attack_speed":0.5, "lunge_range":0*TILE_SIZE, "lunge_freeze":40, "lunge_length":20, "lunge_speed":1,"lunge_cooldown":random.randint(2,6)*120//2, "image":(0*TILE_SIZE,22*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, "takes_knockback":True, "can_lunge":False, "attack":"bullet", "spawner":False, "has_items":False, 'spawning_chance':[x for x in range(82,90)]}
    INFECTED_SCRAPPER = {'name':'infected_scrapper',"health":50, "speed":0.36, "damage":5, "range":1*TILE_SIZE, "attack_freeze":40, "attack_cooldown":120, "attack_speed":1.5, "lunge_range":6*TILE_SIZE, "lunge_freeze":40, "lunge_length":20, "lunge_speed":1,"lunge_cooldown":random.randint(2,6)*120//2, "image":(0*TILE_SIZE,26*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, "takes_knockback":True, 'can_lunge':True,"attack":"bullet", "spawner":False, "has_items":True, 'spawning_chance':[x for x in range(91,92)]}
    HIVE_QUEEN = {'name':'hive_queen',"health":70, "speed":0.15, "damage":5, "range":1*TILE_SIZE, "attack_freeze":40, "attack_cooldown":120, "attack_speed":1.5, "lunge_range":2*TILE_SIZE, "lunge_freeze":40, "lunge_length":20, "lunge_speed":0.5,"lunge_cooldown":random.randint(2,6)*120//2, "image":(0*TILE_SIZE,16*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, "takes_knockback":True, "can_lunge":True, "attack":"slash", "spawner":True, "has_items":False, 'spawning_chance':[x for x in range(92,99)]}
    HATCHLING = {'name':'hatchling',"health":20, "speed":0.4, "damage":2, "range":1*TILE_SIZE, "attack_freeze":40, "attack_cooldown":90, "attack_speed":1.5, "lunge_range":6*TILE_SIZE, "lunge_freeze":30, "lunge_length":15, "lunge_speed":1.5,"lunge_cooldown":random.randint(2,6)*120//2, "image":(0*TILE_SIZE,20*TILE_SIZE), "width":TILE_SIZE, "height":TILE_SIZE, "takes_knockback":True, "can_lunge":True, "attack":"slash", "spawner":False, "has_items":False, 'spawning_chance':[]}
    
    ENEMY_LIST = [SPIDER,BULWARK,STALKER,TUMOR,TURRET,INFECTED_SCRAPPER,HIVE_QUEEN,HATCHLING]

class Enemy:
    def __init__(self, x, y, template, player, world,itemList,always_loaded=False): #Creates a new enemy, with all its stats
        self.x = x
        self.y = y
        self.player = player
        self.world = world
        self.physics = Physics(world)
        self.rooms = self.world.roombuild.rooms
        self.room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)

        self.health = template["health"]
        self.speed = template["speed"]
        self.physics.momentum = self.speed
        self.cos = 0
        self.sin = 0

        self.isAttacking = False
        self.damage = template["damage"]
        self.range = template["range"]
        self.attack_freeze = template["attack_freeze"]
        self.attack_cooldown = template["attack_cooldown"]
        self.attack_speed = template["attack_speed"]
        self.attackFrame = 0

        self.isLunging = 0
        self.lunge_range = template["lunge_range"]
        self.lunge_speed = template["lunge_speed"]
        self.lunge_freeze = template["lunge_freeze"]
        self.lunge_length = template["lunge_length"]
        self.lunge_cooldown = template["lunge_cooldown"]
        self.lungeFrame = 0

        self.loaded = False
        self.always_loaded = always_loaded
        self.itemList = itemList

        self.base_image = template["image"]
        self.image = [template["image"][0], template["image"][1]]
        self.facing = [0,0]
        self.img_change = [0,0]
        self.width = template["width"]
        self.height = template["height"]

        self.pierced = []

        self.hitStun = False
        self.hitFrame = 0
        self.takesKnockback = template["takes_knockback"]
        self.knockback = 0
        self.hitByDash = False

        self.canLunge = template["can_lunge"]
        self.attack_type = template["attack"]
        self.spawnFrame = 0
        self.spawner = template["spawner"]

        self.type = "enemy"
        self.has_items = template["has_items"]
        self.name = template["name"]
        self.pathing()

        if template["has_items"]:
            gun_random = random.randint(1,100)
            for gun in Guns.Gun_list:
                if gun_random in gun["rate"]:
                    self.gun = gun

        loadedEntities.append(self) #As long as this enemy exists in this list, its alive

    def update(self): #All the things we need to do every frame to make the enemy work
        
        if self in self.player.loadedEntitiesInRange:
            self.loaded = True
        else:
            self.loaded = False

        self.room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)
        
        self.img_change = [0,0]

        if self.loaded or self.always_loaded:
            self.enemies_pusharound()
            self.attack()
            self.lunge()
            self.spawn_hatchlings()
            self.kamikaze()
            self.lungeFrame += 1
            self.attackFrame += 1
            self.spawnFrame += 1
            self.getFacing()
            self.death()
            
            if self.hitStun:
                self.hitStunFunction()
            else:
                self.pathing()
                self.moveInPathing()

            self.image[0], self.image[1] = self.base_image[0] + self.facing[0] + self.img_change[0], self.base_image[1] + self.facing[1] + self.img_change[1]
    

    def hitStunFunction(self):
        self.img_change[0] = 16
        if self.hitFrame >= 24:
            self.hitStun = False
            self.hitFrame = 0
        self.hitFrame += 1

    def moveInPathing(self):
        if not self.isAttacking and self.isLunging == 0:
            if self.norm < 100 and self.norm > 5:
                self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [self.cos, self.sin])
    
    def enemies_pusharound(self): #Prevent enemies from overlapping by making them push each other
        for entity in self.player.loadedEntitiesInRange:
            cos = random.randint(-200,200)/100
            sin = math.sqrt((2-cos)**2) * (random.randint(0,1)*2-1)
            if in_perimeter(self.x,self.y,entity.x,entity.y,3) and self != entity:
                if entity.type == "enemy" and collision(self.x, self.y, entity.x ,entity.y, [self.width, self.height], [entity.width, entity.height]):
                    self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [cos, sin])
                    entity.x ,entity.y = entity.physics.move(entity.x ,entity.y, entity.width, entity.height, [-cos, -sin])

    def attack(self): #Makes the enemies slash or attack 
        if self.isLunging == 0 and self.room['name'] == self.player.room['name'] and self.attack_type in ["slash", "bullet"]:
            if self.norm <= self.range and self.attackFrame >= self.attack_cooldown and not self.isAttacking:
                self.attackFrame = 0
                self.isAttacking = True
                self.attackVector = [self.cos, self.sin]
            if self.isAttacking and self.attackFrame >= self.attack_freeze:
                self.attackFrame = 0
                self.isAttacking = False
                if self.attack_type == "slash":
                    self.slash()
                elif self.attack_type == "bullet":
                    if self.has_items:
                        for i in range(self.gun["bullet_count"]):
                            if self.norm != 0:
                                angle = math.acos(self.cos)*pyxel.sgn(self.sin)
                                lowest_angle = angle - self.gun["spread"]*(math.pi/180)
                                highest_angle = angle + self.gun["spread"]*(math.pi/180)
                                angle = random.uniform(lowest_angle, highest_angle)
                                cos = math.cos(angle)
                                sin = math.sin(angle)
                            else:
                                cos = 0
                                sin = 0
                            Bullet(self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.gun["damage"], self.gun["bullet_speed"], self.gun["range"], self.gun["piercing"], self.world, self.player, (1*TILE_SIZE,6*TILE_SIZE), "enemy", self.gun["explode_radius"])
                    else:
                        Bullet(self.x+self.width/2, self.y+self.height/2, 4, 4, [self.cos, self.sin], self.damage, self.attack_speed, self.range, 0, self.world, self.player, [1*TILE_SIZE,6*TILE_SIZE], "enemy", 0)

    def slash(self):
        self.world.effects.append({'x':self.x+self.cos*TILE_SIZE,'y':self.y+self.sin*TILE_SIZE,'image':[7,6],'scale':1,'time':pyxel.frame_count})
        if collision(self.x+self.cos*TILE_SIZE,self.y+self.sin*TILE_SIZE,self.player.x,self.player.y,(TILE_SIZE,TILE_SIZE),(TILE_SIZE,TILE_SIZE)): #pas assez de sin et cos
            self.player.health -= self.damage
            self.player.isHit = True
            self.player.hitFrame = 0

    def lunge(self): #Allows the enemy to lunge at the player
        if not self.isAttacking and self.canLunge:
            if self.norm<=self.lunge_range and self.norm>self.range and self.lungeFrame >= self.lunge_cooldown and self.isLunging==0:
                self.lungeFrame = 0
                self.isLunging = 1
                self.lungeVector = [self.cos, self.sin]
            if self.isLunging==1 and self.lungeFrame >= self.lunge_freeze:
                self.lungeFrame = 0
                self.isLunging = 2
                self.physics.momentum = self.lunge_speed
                self.hit_player = False
            if self.isLunging==2:
                self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.lungeVector)
                if self.attack_type == "lunge": #Makes the enemy damage the player when colliding
                    if collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]) and not self.hit_player:
                        self.player.health -= self.damage
                        self.player.isHit = True
                        self.player.hitFrame = 0
                        self.hit_player = True
                if self.lungeFrame >= self.lunge_length:
                    self.isLunging=0
                    self.physics.momentum = self.speed

    def spawn_hatchlings(self): #Allows enemies to spawn hatchlings
        if self.spawner and self.spawnFrame > 3*FPS:
            for i in range(2):
                Enemy(self.x, self.y, EnemyTemplates.HATCHLING, self.player, self.world, self.itemList,True)
            self.spawnFrame = 0

    def kamikaze(self): #Allows enemy to blow itself up
        if self.attack_type == "collision" and collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]):
            self.health = 0
            self.player.health -= self.damage
            self.player.isHit = True
            self.player.hitFrame = 0
            Effect(4,[2*TILE_SIZE, 6*TILE_SIZE], {0:6, 1:6, 2:6, 3:6}, self.x, self.y, TILE_SIZE, TILE_SIZE)
            for entity in loadedEntities:
                if entity.type == "enemy" and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]):
                    entity.health -= self.damage
                    entity.hitStun = True
                    entity.knockback = 20


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

        if self.isLunging == 1:
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

            if self.spawner :
                for i in range(5):
                    Enemy(self.x, self.y, EnemyTemplates.HATCHLING, self.player, self.world, self.itemList)

            if self.attack_type == "collision":
                Effect(4,[2*TILE_SIZE, 6*TILE_SIZE], {0:6, 1:6, 2:6, 3:6}, self.x, self.y, TILE_SIZE, TILE_SIZE)
                for entity in loadedEntities:
                    if entity.type == "enemy" and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]):
                        entity.health -= self.damage
                        entity.hitStun = True
                        entity.knockback = 20

            if self.name != "hatchling":
                item_chance = 10 + self.player.luck
                gun_chance = 12

                pickup = random.randint(1,100)
                if pickup <= item_chance:
                    PickUp(self.x, self.y, "item", self.randomItem(), self.player)

                elif pickup > 100-gun_chance:
                    gun_random = random.randint(1,100)
                    for gun in Guns.Gun_list:
                        if gun_random in gun["rate"]:
                            PickUp(self.x, self.y, "weapon", gun, self.player)

                elif pickup > 100-gun_chance-5:
                    PickUp(self.x, self.y, "item", self.itemList.FUEL, self.player)

            self.player.triggerOnKillItems()
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

class EnemyGroup:
    def __init__(self,rooms,room,dic_enemies={'spider':0}):
        self.rooms = rooms
        self.room = room
        self.dic_enemies = dic_enemies
        self.loaded = False
    def update(self):
        if on_tick(120*2):
            if self.room['name']+1 <= len(self.rooms):
                print(self.room['X'],self.room['Y'],flush=True)
                self.room = self.rooms[self.room['name']+1]

class Guns: #Contains all the different guns the player can get
    NONE = {"damage":0, "bullet_speed":1, "range":1, "piercing":0, "max_ammo":0, "ammo":0, "reload":120, "cooldown":120, "spread":0, "bullet_count":0, "name":"None", "image":[0,0], "rate":[], "description":"No weapon", "explode_radius":0}
    PISTOL = {"damage":9, "bullet_speed":0.75, "range":6*TILE_SIZE, "piercing":0, "max_ammo":16, "ammo":16, "reload":0.8*120, "cooldown":1/3*120, "spread":15, "bullet_count":1, "name":"Pistol", "image":[1*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(1,26)], "description":"Basic weapon", "explode_radius":0}
    SHOTGUN = {"damage":9, "bullet_speed":0.6, "range":4*TILE_SIZE, "piercing":0, "max_ammo":5, "ammo":5, "reload":3*120, "cooldown":0.75*120, "spread":25, "bullet_count":6, "name":"Shotgun", "image":[3*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(26,51)], "description":"Multiple pellets, medium damage", "explode_radius":0}
    SMG = {"damage":8, "bullet_speed":1, "range":4*TILE_SIZE, "piercing":0, "max_ammo":40, "ammo":40, "reload":2.5*120, "cooldown":0.12*120, "spread":20, "bullet_count":1, "name":"SMG", "image":[0*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(51,76)], "description":"Highest fire rate, low damage", "explode_radius":0}
    RIFLE = {"damage":12, "bullet_speed":0.9, "range":7*TILE_SIZE, "piercing":1, "max_ammo":24, "ammo":24, "reload":3*120, "cooldown":0.25*120, "spread":12, "bullet_count":1, "name":"Rifle", "image":[2*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(76,86)], "description":"High fire rate, medium damage", "explode_radius":0}
    SNIPER = {"damage":20, "bullet_speed":2, "range":20*TILE_SIZE, "piercing":4, "max_ammo":4, "ammo":4, "reload":4*120, "cooldown":1*120, "spread":0, "bullet_count":1, "name":"Sniper", "image":[4*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(86,96)], "description":"Single fire, high damage", "explode_radius":0}
    GRENADE_LAUNCHER = {"damage":20, "bullet_speed":1.5, "range":20*TILE_SIZE, "piercing":0, "max_ammo":1, "ammo":1, "reload":1.5*120, "cooldown":1*120, "spread":5, "bullet_count":1, "name":"Grenade Launcher", "image":[5*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(96,101)], "description":"Single fire, explosive shots", "explode_radius":1.5*TILE_SIZE}
    Gun_list = [PISTOL, RIFLE, SMG, SNIPER, SHOTGUN, GRENADE_LAUNCHER]

class Bullet: #Creates a bullet that can collide and deal damage
    def __init__(self, x, y, width, height, vector, damage, speed, range, piercing, world, player, image, owner, explode_radius):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vector = vector
        self.damage = damage
        self.range = range
        self.world = world
        self.player = player
        self.image = image
        self.physics = Physics(world)
        self.physics.momentum = speed
        self.owner = owner
        self.explode_radius = explode_radius
        self.piercing = piercing
        self.type = "bullet"
        loadedEntities.append(self) #As long as the bullet is a part of this list, it exists

    def update(self): #All the things we need to run every frame
        self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.vector)
        self.check_hit()
        self.bullet_destroyed()
    
    def check_hit(self): #Checks if its hit an enemy (if created by the player) or the player (if created by an enemy) and deals damage
        for entity in loadedEntities:
            if self.owner == "player" and entity.type == "enemy" and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]) and self not in entity.pierced and self.piercing>=0 and not entity.hitStun:
                entity.health -= self.damage
                entity.hitStun = True
                entity.knockback = 10
                if entity.hitFrame<=10 and entity.takesKnockback and (entity.isLunging != 2 and entity.isLunging != 1):
                    entity.x, entity.y = entity.physics.move(entity.x, entity.y, entity.width, entity.height, [-entity.cos*entity.knockback, -entity.sin*entity.knockback])
                if self.piercing != 0:
                    entity.pierced.append(self)
                    self.damage *= self.player.pierceDamage
                self.piercing -= 1
        if self.owner=="enemy" and collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]) and self.piercing>=0:
            self.player.health -= self.damage
            self.piercing -= 1
            self.player.isHit = True
            self.player.hitFrame = 0
        self.range -= math.sqrt((self.vector[0]*self.physics.momentum)**2+(self.vector[1]*self.physics.momentum)**2)
    
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
                    self.player.fuel += 1
                loadedEntities.remove(self)
                pickUpsOnGround.remove(self)

class ItemList: #Lists every item and its properties
    def __init__(self):
        self.SPEED_PASSIVE = {"name":"Jet speedup", "description":"Movement speed increase", "image":[1*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat_p", "function":[["speed", "addition", 0.05]]}
        self.HEALTH_PASSIVE = {"name":"Armor Plating", "description":"Health increase", "image":[0*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat_p", "function":[["max_health", "addition", 5], ["health", "addition", 5]]}
        self.RANGE_PASSIVE = {"name":"Aerodynamism", "description":"Range increase", "image":[2*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat_g", "function":[["range", "multiplication", 1.2]]}
        self.PIERCING_PASSIVE = {"name":"Sharpened Rounds", "description":"Pierce increase", "image":[3*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat_g", "function":[["piercing", "addition", 1]]}
        self.SPREAD_PASSIVE = {"name":"Focused Fire", "description":"Spread decrease", "image":[4*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat_g", "function":[["spread", "multiplication", 0.9]]}
        self.HEAL_KILL = {"name":"Filth Blood", "description":"On kill : Heal", "image":[0*TILE_SIZE,9*TILE_SIZE], "trigger":"onKill", "effect":"stat_p", "function":[["health", "addition", 2]]}
        self.AMMO_KILL = {"name":"Blood Bullets", "description":"On kill : Gain ammo", "image":[2*TILE_SIZE,9*TILE_SIZE], "trigger":"onKill", "effect":"stat_g", "function":[["ammo", "addition", 1]]}
        self.SPEED_KILL = {"name":"Hot Blood", "description":"On kill : Speed boost", "image":[4*TILE_SIZE,9*TILE_SIZE], "trigger":"onKill", "effect":"boost_p", "function":[["speed", "addition", 0.05, 1*120]]}
        self.DAMAGE_DASH = {"name":"Terminal Velocity", "description":"On dash : Damage boost", "image":[3*TILE_SIZE,9*TILE_SIZE], "trigger":"onDash", "effect":"boost_g", "function":[["damage", "addition", 3, 1.5*120]]}
        self.SPEED_DASH = {"name":"Reactor Boost", "description":"On dash : speed boost", "image":[1*TILE_SIZE,8*TILE_SIZE], "trigger":"onDash", "effect":"boost_p", "function":[["speed", "addition", 0.1, 1.5*120]]}
        self.common_list = [self.SPEED_PASSIVE, self.HEALTH_PASSIVE, self.RANGE_PASSIVE, self.PIERCING_PASSIVE, self.SPREAD_PASSIVE, self.HEAL_KILL, self.AMMO_KILL, self.SPEED_KILL, self.DAMAGE_DASH, self.SPEED_DASH]
        
        self.DASH_DAMAGE_PASSIVE = {"name":"Crowd Burner", "description":"Dash deals damage", "image":[6*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat_p", "function":[["dash_damage", "addition", 10]]}
        self.HEAL_RELOAD = {"name":"Core stabilization", "description":"On reload : Heal", "image":[7*TILE_SIZE,8*TILE_SIZE], "trigger":"onReload", "effect":"stat_p", "function":[["health", "addition", 2]]}
        self.DAMAGE_PASSIVE = {"name":"Burning Bullets", "description":"Damage increase", "image":[7*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat_g", "function":[["damage", "addition", 5]]}
        self.MAX_AMMO_PASSIVE = {"name":"Arm attachment", "description":"Max ammo increase", "image":[8*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat_g", "function":[["max_ammo", "multiplication", 1.1]]}
        self.FIRERATE_KILL = {"name":"Overheat", "description":"On kill : Firerate boost", "image":[8*TILE_SIZE,9*TILE_SIZE], "trigger":"onKill", "effect":"boost_g", "function":[["gun_cooldown", "multiplication", 0.8]]}
        self.uncommon_list = [self.DASH_DAMAGE_PASSIVE, self.HEAL_RELOAD, self.DAMAGE_PASSIVE, self.MAX_AMMO_PASSIVE, self.FIRERATE_KILL]

        self.BULLET_COUNT_PASSIVE = {"name":"Extra Gun", "description":"Double bullets", "image":[6*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat_g", "function":[["bullet_count", "multiplication", 2]]}
        self.LUCK_PASSIVE = {"name":"Compatibility plug / Clover Charm", "description":"Increased chance of getting items", "image":[9*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "effect":"stat_p", "function":[["luck", "addition", 1]]}
        self.PIERCING_DAMAGE_PASSIVE = {"name":"Blood Acceleration", "description":"Damage increase with piercing", "image":[9*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat_p", "function":[["pierce_damage", "multiplication", 1.5]]}
        self.legendary_list = [self.BULLET_COUNT_PASSIVE, self.LUCK_PASSIVE, self.PIERCING_DAMAGE_PASSIVE]

        self.FUEL = {"name":"Fuel", "description":"Keep the ship moving", "image":[5*TILE_SIZE,9*TILE_SIZE], "trigger":"passive", "effect":"stat_g", "function":[["N/A", "N/A", 0]]}

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

class ScreenEffect:
    def __init__(self,player):
        self.player = player
        self.redscreen = False
        self.redscreen_alpha = 0
        self.dither = 0
    def update(self):
        if self.player.isHit:
            self.redscreen = True
            if self.player.hitLength > self.player.hitFrame:
                self.dither = (self.player.hitLength - self.player.hitFrame)/self.player.hitLength - 0.5
                if self.dither<0:
                    self.dither = 0
            else:
                self.dither=0
                self.redscreen = False

class Boost: #Gives a temporary stat boost to the player
    def __init__(self, stat, operation, value, duration, target, player, creator):
        self.stat = stat
        self.operation = operation
        self.value = value
        self.duration = duration
        self.frame = 0
        self.player = player
        self.target = target
        self.player.increaseStat(self.stat, self.operation, self.value)
        activeBoosts.append(self) #The boost is active as long as its a part of this list
        self.creator = creator

    def update(self): #Once the boost is over, we reverse its effect
        if self.frame >= self.duration:
            if self.operation == "addition":
                self.player.increaseStat(self.stat, self.operation, -self.value)
            elif self.operation == "multiplication":
                self.player.increaseStat(self.stat, self.operation, 1/self.value)
            activeBoosts.remove(self)
        self.frame += 1

class Camera:
    def __init__(self):
        self.x = (WIDTH//2-6)*TILE_SIZE
        self.y = 0
        self.margin = 1/4
    
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

class Info:
    def __init__(self):
        self.description = ['N/A']

def draw_screen(u, v,camx,camy):
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

def check_entity(loadedEntities, key, value):
    for entity in loadedEntities:
        if getattr(entity,key) == value:
            return True
    return False
    
def on_tick(tickrate=60,delay=0):
    return (pyxel.frame_count % tickrate)-delay == 0

def on_cooldown(frame,cooldown):
    return (pyxel.frame_count - frame) < cooldown

def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def in_perimeter(x1,y1,x2,y2,distance):
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

def tuple_list_sort(list): #NOT CHECKED
    for i in range(len(list)-1):
        min=list[i][0]
        index=i
        for j in range(len(list)-1-i):
            if list[i+j][0]<min:
                min=list[i+j][0]
                index=i+j
        list[i], list[index] = list[index], list[i]
    return list
        

def dic_copy(dico):
    dicoC = {}
    for key in dico.keys():
        dicoC[key]=dico[key]
    return dicoC


def list_copy(listP):
    listC = []
    for i in range(len(listP)):
        listC.append(listP[i])
        return listC

def rooms_collide(world, x, y, w, h): #verified+
    for in_y in range(h+2):
        for in_x in range(w+2):
            if world[y+in_y-1][x+in_x-1] == WorldItem.GROUND:
                return True
    return False

def rect_place(world_map, x, y, w, h, block): #verified+
    for in_y in range(h):
        for in_x in range(w):
            world_map[y+in_y][x+in_x] = block

def world_item_draw(pyxel,x,y,block):
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

def find_room(x,y,rooms):
    rooms_distance = []
    for room in rooms:
        if (x >= room['X'] and x < room['X']+room['W'] and y >= room['Y'] and y < room['Y']+room['H']) or (x >= room['connect'][0] and x < room['connect'][0]+2 and y >= room['connect'][1] and y < room['connect'][1]+2):
            return room
        rooms_distance.append((distance(x,y,room['X'],room['Y']),room))
    rooms_distance = tuple_list_sort(rooms_distance)
    return rooms_distance[0][1]

pickUpsOnGround = []
activeBoosts = []

def in_camera(x,y, camx, camy):
    return in_perimeter((camx + CAM_WIDTH//2)//TILE_SIZE,(camy + CAM_HEIGHT//2)//TILE_SIZE, x, y, CAM_WIDTH//(TILE_SIZE*2) + 1)

def collision(x1, y1, x2, y2, size1, size2): #Checks if object1 and object2 are colliding with each other
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1



App()