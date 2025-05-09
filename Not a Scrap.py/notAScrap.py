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
        pyxel.init(CAM_WIDTH+20,CAM_HEIGHT+20,title='Not a Scrap', fps=FPS)
        pyxel.load('../notAScrap.pyxres')
        self.camera = Camera()
        self.world = World(pyxel.tilemaps[0],RoomBuild(0,WIDTH//2,0))
        self.player = Player(self.world, self.camera)
        self.itemList = ItemList(self.player)
        self.effects = ScreenEffect(self.player)

        
        pyxel.mouse(True)

        self.enemies_spawn()

        pyxel.run(self.update,self.draw)
    

    def update(self):
        if self.player.alive:
            self.player.update()
            for entity in loadedEntities:
                entity.itemList = self.itemList
                entity.update()

            self.camera.update(self.player)
            pyxel.camera(self.camera.x,self.camera.y)
        self.effects.update(self.player)
    
    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                block = self.world.world_map[y][x]
                world_item_draw(pyxel,x,y,block)

        for entity in loadedEntities:
            pyxel.blt(entity.x,
                      entity.y,
                      0,
                      entity.image[0],
                      entity.image[1],
                      entity.width,
                      entity.height,
                      colkey=11)

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
        if self.effects.redscreen:
            pyxel.dither(self.effects.dither)
            draw_screen(
                pyxel,
                0,
                16,
                self.camera.x,
                self.camera.y,)
        pyxel.dither(1)
        
        pyxel.text(self.camera.x+1, self.camera.y+1, "Health:"+str(self.player.health)+"/"+str(self.player.max_health),8)
        pyxel.text(self.camera.x+1, self.camera.y+7, "Weapon:"+str(self.player.gun["name"]),7)
        pyxel.text(self.camera.x+1, self.camera.y+13, "Ammo:"+str(self.player.gun["ammo"])+"/"+str(self.player.gun["max_ammo"]),7)
    
    def enemies_spawn(self):
        margin_spawn = 5
        for room in self.world.roombuild.rooms:
            if room['name']>=margin_spawn + 2:
                nb_enemies = random.randint(room['name']-margin_spawn,room['name'])
            else:
                nb_enemies = random.randint(0,room['name'])

            for i in range(nb_enemies):
                occupied = True
                for attempt in range(3):
                    if occupied:
                        X_pos = room['X'] + random.randint(0,room['W']-1)
                        Y_pos = room['Y'] + random.randint(0,room['H']-1)
                        if not (check_entity(loadedEntities, 'x', X_pos) and check_entity(loadedEntities, 'y', Y_pos)):
                            occupied = False
                Enemy(X_pos*TILE_SIZE,Y_pos*TILE_SIZE,EnemyTemplates.BASE,self.player,self.world)
                    


def check_entity(loadedEntities, key, value):
    for entity in loadedEntities:
        if getattr(entity,key) == value:
            return True
    return False
    
def on_tick(tickrate=0.5):
    return pyxel.frame_count % (FPS * tickrate) == 0

class WorldItem:
    WALL = (0,0)
    GROUND = (0,1)
    CONNECT = (1,1)

    BLOCKS = [WALL,GROUND]

class World:
    def __init__(self,tilemap,roombuild):
        self.tilemap = tilemap
        self.roombuild = roombuild
        self.world_map = [[(0,0) for j in range(WIDTH)] for i in range(HEIGHT)]
        self.player_init_posX = WIDTH//2+2
        self.player_init_posY = 0
        self.nb_rooms = 20
        
        self.roombuild.random_rooms_place(self.world_map,WIDTH//2,0,4,4,20)
        self.world_map = self.roombuild.world_map

class RoomBuild:
    def __init__(self, name, startX, startY):
        self.rooms = [{'name':name,'X':startX,'Y':startY,'W':4,'H':4,'connect':(startX,startY)}]
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
    def random_rooms_place(self, world_map, startX, startY, startW, startH, nb_rooms):
        rect_place(world_map,startX,startY,startW,startH,WorldItem.GROUND)
        last_placement = 'N/A'
        for i in range(nb_rooms):

            self.newW = random.randint(2,self.max_size)*2
            self.newH = random.randint(2,self.max_size)*2

            if last_placement == 'down':
                self.room_pos = random.randint(0,2)
                if self.room_pos == 0 and self.x>self.max_size*2+1:
                    self.room_place_left()
                    last_placement = 'left'

                elif self.room_pos == 1 and self.x<WIDTH-self.max_size*2+1:
                    self.room_place_right()
                    last_placement = 'right'

                else:
                    self.room_place_down()

            else:
                self.room_place_down()
                last_placement = 'down'

                if last_placement != 'down':
                    self.fix_collide_rooms() #found 1 bug "1fixed 1fixed" but 1 was left unfixed when it couldve been
            
            rect_place(world_map,self.newConnect[0],self.newConnect[1], 2, 2, WorldItem.CONNECT)
            rect_place(world_map, self.newX, self.newY, self.newW, self.newH, WorldItem.GROUND)
            self.rooms.append({'name':i+1,'X':self.newX,'Y':self.newY,'W':self.newW,'H':self.newH,'connect':(self.newConnect[0],self.newConnect[1])})
            
            self.x, self.y, self.w, self.h, self.connect = self.newX, self.newY, self.newW, self.newH, self.newConnect
        
        self.world_map = world_map
    
    def room_place_left(self):
        self.newConnect[0] = self.x - 2
        self.newConnect[1] = self.y + random.randint(0,self.h-2)
        self.newX = self.newConnect[0] - self.newW
        self.newY = self.newConnect[1] - random.randint(0,self.newH-2)
        self.last_down = False
    def room_place_right(self):
        self.newConnect[0] = self.x + self.w
        self.newConnect[1] = self.y + random.randint(0,self.h-2)
        self.newX = self.newConnect[0] +2
        self.newY = self.newConnect[1] - random.randint(0,self.newH-2)
        self.last_down = False
    def room_place_down(self):
        self.newConnect[0] = self.x + random.randint(1,self.w-2)
        self.newConnect[1] = self.y + self.h
        self.newX = self.newConnect[0] - random.randint(0,self.newW-2)
        self.newY = self.newConnect[1] +2
        
    def fix_collide_rooms(self): #plupart des collisions arrivent a cause de newY trop haut 'dont work'
        for room in self.rooms:
            collided=False
            if collision(self.newX-1,self.newY-1,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])):
                collided=True
            
            if collided:
                if self.newH>4:
                    for i in range(self.newH-4):
                        if collided:
                            if not collision(self.newX-1,self.newY-1+i,room['X'],room['Y'],(self.newW+2,self.newH+2),(room['W'],room['H'])): #ajouté +i pour descendre la room pour voir si ca collide pas
                                self.newY = self.newY+i
                                collided = False

def find_room(x,y,rooms):
    for room in rooms:
        if x >= room['X'] and x < room['X']+room['W'] and y >= room['Y'] and y < room['Y']+room['H']:
            return room
    return 'None'
        


         

class Furniture:
    def __init__(self,world):
        self.world = world

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

class ScreenEffect:
    def __init__(self,player):
        self.player = player
        self.redscreen = False
        self.redscreen_alpha = 0
        self.dither = 0
    def update(self,player):
        if player.isHit:
            self.redscreen = True
            if player.hitLength > player.hitFrame:
                self.dither = (player.hitLength - player.hitFrame)/player.hitLength - 0.5
                if self.dither<0:
                    self.dither = 0
            else:
                self.dither=0
                self.redscreen = False

def draw_screen(pyxel, u, v,camx,camy):
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


class Player:
    def __init__(self, world, camera):
        self.alive = True
        self.x = world.player_init_posX*TILE_SIZE
        self.y = world.player_init_posY
        self.image = (1,3)
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.world = world
        self.rooms = self.world.roombuild.rooms
        self.room = self.rooms[0]

        self.physics = Physics(world)
        self.speed = 0.25
        self.speedFallOff = 4
        self.facing = [1,0]
        self.last_facing = [1,0]

        self.isDashing = False
        self.dashCooldown = 40
        self.dashLength = 20
        self.dashFrame = 0
        self.dashStrength = self.speed*2.5

        self.health = 50
        self.max_health = 50
        self.last_health = self.health
        self.hitFrame = 0
        self.hitLength = 120
        self.isHit = False

        self.gun = dic_copy(Guns.SHOTGUN)
        self.attackFrame = 0

        self.ownedItems = []
        self.justKilled = False

        self.camera = camera

    def update(self):
        self.posXmouse = self.camera.x+pyxel.mouse_x
        self.poxYmouse = self.camera.y+pyxel.mouse_y
        if not self.isDashing:
            self.inputs_to_moves()

            if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S) and self.physics.momentum <= self.speed:
                self.physics.momentum = self.speed
            else:
                self.physics.momentum /= self.speedFallOff

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.attackFrame>=self.gun["cooldown"] and self.gun["ammo"]>0:
                self.shoot()

            if pyxel.btnp(pyxel.KEY_R) and self.gun["ammo"]<self.gun["max_ammo"] and self.gun["ammo"]!=0:
                self.gun["ammo"] = 0
                self.attackFrame = 0
            
            if self.gun["ammo"]==0 and self.attackFrame>=self.gun["reload"]:
                self.gun["ammo"]=self.gun["max_ammo"]

            if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_SHIFT)) and self.dashFrame >= self.dashCooldown:
                self.isDashing = True
                self.dashFrame = 0
                self.physics.momentum = self.speed*2.5
                self.image = [6,2]
        else:
            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.facing)
            if self.dashFrame >= self.dashLength:
                self.isDashing = False
                self.dashFrame = 0
        
        if self.last_health != self.health:
            self.hitFrame = 0
            self.last_health = self.health
            self.isHit = True   
        if self.hitFrame >= self.hitLength:
                self.isHit = False
                self.hitFrame = 0

        
        
        
        self.attackFrame += 1
        self.dashFrame += 1
        self.hitFrame += 1

        if self.x<0:
            self.x = 0
        if self.y<0:
            self.y = 0
        if self.x > WIDTH*TILE_SIZE:
            self.x = (WIDTH-1)*TILE_SIZE
        if self.y > HEIGHT*TILE_SIZE:
            self.y = (HEIGHT-1)*TILE_SIZE

        if self.justKilled:
            self.justKilled = False
            for item in self.ownedItems:
                if item["name"] == "heal_on_kill":
                    self.health += 5
                    if self.health > self.max_health:
                        self.health = self.max_health
                if item["name"] == "ammo_on_kill":
                    self.gun["ammo"] += 5
                    if self.gun["ammo"] > self.gun["max_ammo"]:
                        self.gun["ammo"] = self.gun["max_ammo"]
                #if item["name"] == 

        if self.health<=0:
            self.alive = False
        
        current_room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)
        if current_room != 'None':
            self.room = current_room
    
    def inputs_to_moves(self):
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

    def shoot(self):
        self.attackFrame = 0
        self.gun["ammo"] -= 1
        for i in range(self.gun["bullet_count"]):
            horizontal = self.posXmouse - (self.x+self.width/2)
            vertical = self.poxYmouse - (self.y+self.height/2)
            norm = math.sqrt(horizontal**2+vertical**2)
            if norm != 0:
                cos = horizontal/norm
                lowest_cos = cos*(1-self.gun["spread"])
                highest_cos = cos*(1+self.gun["spread"])
                cos = random.uniform(lowest_cos, highest_cos)

                sin = vertical/norm
                lowest_sin = sin*(1-self.gun["spread"])
                highest_sin = sin*(1+self.gun["spread"])
                sin = random.uniform(lowest_sin, highest_sin)
            else:
                cos = 0
                sin = 0

            if self.gun != Guns.GRENADE_LAUNCHER:
                Bullet(self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.gun["damage"], self.gun["bullet_speed"], self.gun["range"], self.gun["piercing"], self.world, self, (0,6*TILE_SIZE), "player", "bullet_normal")
            else:
                Bullet(self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.gun["damage"], self.gun["bullet_speed"], self.gun["range"], self.gun["piercing"], self.world, self, (0,6*TILE_SIZE), "player", "bullet_explode", 1.5*TILE_SIZE)


    def getItem(self, item):
        self.ownedItems.append(item)
        if item["trigger"] == "passive" and (item["effect"] == "stat_p" or item["effect"] == "stat_g"):
            print("got passive item")
            for change in item["function"]:
                if change[1] == "additive":
                    change[0] += change[2]
                if change[1] == "mutliplicative":
                    change[0] *= change[2]

    def changeWeapon(self, gun):
        self.gun = dic_copy(gun)
        for key in self.gun.keys():
            if key != "name" and key != "rate" and key != "image" and key !="bullet_count":
                lowest_value = self.gun[key]*0.9
                highest_value = self.gun[key]*1.1
                self.gun[key] = random.uniform(lowest_value, highest_value)
        self.gun["piercing"] = math.ceil(self.gun["piercing"])
        self.gun["max_ammo"] = math.ceil(self.gun["max_ammo"])
        self.gun["ammo"] = self.gun["max_ammo"]
        for item in self.ownedItems:
            if item["trigger"] == "passive" and item["effect"]=="stat_g":
                for change in item["function"]:
                    if change[1] == "additive":
                        change[0] += change[2]
                    if change[1] == "mutliplicative":
                        change[0] *= change[2]


class Physics:
    def __init__(self, world):
        self.world = world
        self.momentum = 0
        self.collision_happened = False

    def move(self, x, y, width, height, vector):
        X = int(x//TILE_SIZE)
        Y = int(y//TILE_SIZE)

        new_x = x + vector[0]*self.momentum

        new_X = X+pyxel.sgn(vector[0])
        if vector[0]!=0:
            next_X_1 = self.world.world_map[Y][new_X]
            if y != Y*TILE_SIZE:
                next_X_2 = self.world.world_map[Y+1][new_X]
            else:
                next_X_2 = WorldItem.GROUND
            if (next_X_1!=WorldItem.WALL or not collision(new_x, y, new_X*TILE_SIZE, Y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])) and (next_X_2!=WorldItem.WALL or not collision(new_x, y, new_X*TILE_SIZE, (Y+1)*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])):
                x = new_x
            elif (next_X_1==WorldItem.WALL or next_X_2==WorldItem.WALL) and new_x+width>X*TILE_SIZE and (X+1)*TILE_SIZE>new_x:
                self.collision_happened = True
                x = (new_X-pyxel.sgn(vector[0]))*TILE_SIZE
        
        X = int(x//TILE_SIZE)

        new_y = y + vector[1]*self.momentum
        new_Y = Y+pyxel.sgn(vector[1])
        if vector[1]!=0:
            next_Y_1 = self.world.world_map[new_Y][X]
            if x != X*TILE_SIZE:
                next_Y_2 = self.world.world_map[new_Y][X+1]
            else:
                next_Y_2 = WorldItem.GROUND
            if (next_Y_1!=WorldItem.WALL or not collision(x, new_y, X*TILE_SIZE, new_Y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])) and (next_Y_2!=WorldItem.WALL or not collision(x, new_y, (X+1)*TILE_SIZE, new_Y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])):
                y = new_y
            elif (next_Y_1==WorldItem.WALL or next_Y_2==WorldItem.WALL) and new_y+height>Y*TILE_SIZE and (Y+1)*TILE_SIZE>new_y:
                self.collision_happened = True
                y = (new_Y-pyxel.sgn(vector[1]))*TILE_SIZE

        return x,y

class Guns:
    PISTOL = {"damage":8, "bullet_speed":0.75, "range":6*TILE_SIZE, "piercing":0, "max_ammo":16, "ammo":16, "reload":1.5*120, "cooldown":1/3*120, "spread":0.1, "bullet_count":1, "name":"Pistol", "image":[1*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(1,31)]}
    RIFLE = {"damage":8, "bullet_speed":0.9, "range":7*TILE_SIZE, "piercing":1, "max_ammo":24, "ammo":24, "reload":3*120, "cooldown":0.25*120, "spread":0.2, "bullet_count":1, "name":"Rifle", "image":[2*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(31,51)]}
    SMG = {"damage":5, "bullet_speed":1, "range":4*TILE_SIZE, "piercing":0, "max_ammo":40, "ammo":40, "reload":2.5*120, "cooldown":0.17*120, "spread":0.55, "bullet_count":1, "name":"SMG", "image":[0*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(71,83)]}
    SNIPER = {"damage":20, "bullet_speed":2, "range":20*TILE_SIZE, "piercing":4, "max_ammo":4, "ammo":4, "reload":4*120, "cooldown":1*120, "spread":0, "bullet_count":1, "name":"Sniper", "image":[4*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(83,95)]}
    SHOTGUN = {"damage":9, "bullet_speed":0.6, "range":4*TILE_SIZE, "piercing":0, "max_ammo":5, "ammo":5, "reload":3*120, "cooldown":0.75*120, "spread":0.6, "bullet_count":6, "name":"Shotgun", "image":[3*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(51,71)]}
    GRENADE_LAUNCHER = {"damage":20, "bullet_speed":1.5, "range":20*TILE_SIZE, "piercing":0, "max_ammo":1, "ammo":1, "reload":1.5*120, "cooldown":1*120, "spread":0, "bullet_count":1, "name":"Grenade Launcher", "image":[5*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(95,101)]}
    Gun_list = [PISTOL, RIFLE, SMG, SNIPER, SHOTGUN, GRENADE_LAUNCHER]


class Bullet:
    def __init__(self, x, y, width, height, vector, damage, speed, range, piercing, world, player, image, owner, type, explode_radius=0):
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
        self.type = type
        self.explode_radius = explode_radius
        self.piercing = piercing
        loadedEntities.append(self)

    def update(self):
        self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.vector)
        self.check_hit()

        if self.physics.collision_happened or self.range <= 0 or self.piercing<0:
            if self.type == "bullet_explode":
                for entity in loadedEntities:
                    if entity.type == "enemy":
                        horizontal = entity.x+entity.width/2 - self.x+self.width/2
                        vertical = entity.y+entity.height/2 - self.y+self.height/2
                        norm = math.sqrt(horizontal**2 + vertical**2)
                        if norm <= self.explode_radius:
                            entity.health -= self.damage
                            entity.hitStun = True
            loadedEntities.remove(self)
    
    def check_hit(self):
        for entity in loadedEntities:
            if self.owner == "player" and entity.type == "enemy" and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]) and self not in entity.pierced and self.piercing>=0 and not entity.hitStun:
                entity.health -= self.damage
                entity.hitStun = True
                if self.piercing != 0:
                    entity.pierced.append(self)
                self.piercing -= 1
        if self.owner=="enemy" and collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]) and self.piercing>=0:
            self.player.health -= self.damage
            self.piercing -= 1
        self.range -= math.sqrt((self.vector[0]*self.physics.momentum)**2+(self.vector[1]*self.physics.momentum)**2)

class EnemyTemplates:
    BASE = {"health":50, "speed":0.2, "damage":5, "range":2.5*TILE_SIZE, "attack_freeze":40, "attack_cooldown":240, "attack_speed":1.5, "lunge_range":6*TILE_SIZE, "lunge_freeze":40, "lunge_length":20, "lunge_speed":0.75,"lunge_cooldown":random.randint(2,6)*120//2, "image":[1*TILE_SIZE,4*TILE_SIZE], "width":TILE_SIZE, "height":TILE_SIZE}

class Enemy:
    def __init__(self, x, y, template, player, world):
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

        self.image = template["image"]
        self.width = template["width"]
        self.height = template["height"]

        self.pierced = []

        self.hitStun = False
        self.hitFrame = 0

        self.type = "enemy"

        loadedEntities.append(self)

    def update(self):
        
        current_room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)
        if current_room != 'None':
            self.room = current_room
        
        
        horizontal = self.player.x - self.x
        vertical = self.player.y - self.y
        norm = math.sqrt(horizontal**2+vertical**2)
        if norm != 0:
            cos = horizontal/norm
            sin = vertical/norm
        else:
            cos = 0
            sin = 0

        if self.hitStun:
            if self.image[0]<16:
                self.image[0] += 32
            elif self.image[0]<32:
                self.image[0] += 16
            if self.hitFrame<=4:
                self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [-cos*2, -sin*2])
            if self.hitFrame >= 24:
                self.hitStun = False
                self.hitFrame = 0
            self.hitFrame += 1
        else:
            self.image = [0,32]

            if not self.isAttacking and self.isLunging == 0:
                if norm < 100 and norm > 5:
                    if self.room['name'] > self.player.room['name'] and current_room != 'None':
                        horizontal = self.room['connect'][0]*TILE_SIZE - self.x + TILE_SIZE-1
                        vertical = self.room['connect'][1]*TILE_SIZE - self.y + 1
                        norm = math.sqrt(horizontal**2+vertical**2)
                        if norm != 0:
                            cos = horizontal/norm
                            sin = vertical/norm
                        else:
                            cos = 0
                            sin = 0
                        #print(round(self.x//TILE_SIZE),round(self.y//TILE_SIZE),self.room['connect'],current_room)
                        if self.y//TILE_SIZE == self.room['Y'] and not (self.x//TILE_SIZE > self.room['connect'][0] and self.x//TILE_SIZE < self.room['connect'][0]+2): #bugged as shit but the idea is there
                            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [cos, 0])
                        elif self.x//TILE_SIZE == self.room['X'] and not (self.y//TILE_SIZE > self.room['connect'][1] and self.y//TILE_SIZE < self.room['connect'][1]+2):
                            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [0,sin])
                        else:
                            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [cos, sin])
                        
                    else:
                        self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [cos, sin])

            if self.isLunging == 0: #hmmmmmmm maybe rewrite clearly
                if norm <= self.range and self.attackFrame >= self.attack_cooldown and not self.isAttacking:
                    self.attackFrame = 0
                    self.isAttacking = True
                    self.attackVector = [cos, sin]
                if self.isAttacking and self.attackFrame >= self.attack_freeze:
                    self.attackFrame = 0
                    self.isAttacking = False
                    Bullet(self.x+self.width/2, self.y+self.height/2, 3,3,self.attackVector, self.damage, self.attack_speed, self.range, 0, self.world, self.player,(256*TILE_SIZE,256*TILE_SIZE), "enemy", "enemy_melee")
                
            
            if not self.isAttacking:
                if norm<=self.lunge_range and norm>self.range and self.lungeFrame >= self.lunge_cooldown and self.isLunging==0:
                    self.lungeFrame = 0
                    self.isLunging = 1
                    self.lungeVector = [cos, sin]
                if self.isLunging==1 and self.lungeFrame >= self.lunge_freeze:
                    self.lungeFrame = 0
                    self.isLunging = 2
                    self.physics.momentum = self.lunge_speed
                if self.isLunging==2:
                    self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.lungeVector)
                    if self.lungeFrame >= self.lunge_length:
                        self.isLunging=0
                        self.physics.momentum = self.speed
            self.lungeFrame += 1
            self.attackFrame += 1

            self.direction_to_image(horizontal,vertical)

        if self.health <= 0:

            pickup = random.randint(1,100)
            if pickup <= 25:
                item_rarity = random.randint(1,20)
                if item_rarity == 20:
                    print("gave legendary item")
                elif item_rarity>14 and item_rarity<15:
                    print("gave uncommon item")
                else:
                    item_random = random.randint(0, len(self.itemList.common_list)-1)
                    item = self.itemList.common_list[item_random]
                    PickUp(self.x, self.y, "item", item, self.player)

            elif pickup > 75:
                gun_random = random.randint(1,100)
                for gun in Guns.Gun_list:
                    if gun_random in gun["rate"]:
                        PickUp(self.x, self.y, "weapon", gun, self.player)

            loadedEntities.remove(self)
        

    def direction_to_image(self,horizontal,vertical):
        if abs(horizontal)>abs(vertical):
            self.image[1] = 32
            if horizontal>0:
                self.image[0] = 0
            else:
                self.image[0] = 8
        else:
            self.image[1] = 40
            if vertical>0:
                self.image[0] = 0
            else:
                self.image[0] = 8

        if self.isLunging == 1:
            if self.image[0]<16:
                self.image[0] +=16

class PickUp:
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

    def update(self):
        if collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]) and pyxel.btnp(pyxel.KEY_E):
            if self.type == "weapon":
                self.player.changeWeapon(self.object)
            if self.type == "item":
                self.player.getItem(self.object)
            loadedEntities.remove(self)

class ItemList:
    def __init__(self, player):
        self.player = player
        self.SPEED_PASSIVE = {"name":"placeholder", "description":"placeholder", "image":[1*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_p", "function":[[self.player.speed, "additive", 0.15]]}
        self.HEALTH_PASSIVE = {"name":"placeholder", "description":"placeholder", "image":[0*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_p", "function":[[self.player.max_health, "additive", 5], [self.player.health, "additive", 5]]}
        self.RANGE_PASSIVE = {"name":"placeholder", "description":"placeholder", "image":[2*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_g", "function":[[self.player.gun["range"], "multiplicative", 1.2]]}
        self.PIERCING_PASSIVE = {"name":"placeholder", "description":"placeholder", "image":[3*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_g", "function":[[self.player.gun["piercing"], "additive", 1]]}
        self.SPREAD_PASSIVE = {"name":"placeholder", "description":"placeholder", "image":[4*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_g", "function":[[self.player.gun["spread"], "multiplicative", 0.8]]}
        self.HEAL_KILL = {"name":"placeholder", "description":"placeholder", "image":[5*TILE_SIZE,8*TILE_SIZE], "trigger":"onKill", "rarity":"common"}
        self.AMMO_KILL = {"name":"placeholder", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common"}
        self.COOLDOWN_KILL = {"name":"placeholder", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common"}
        self.DAMAGE_ROLL = {"name":"placeholder", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common"}
        self.SPEED_ROLL = {"name":"placeholder", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common"}
        self.common_list = [self.SPEED_PASSIVE, self.HEALTH_PASSIVE, self.RANGE_PASSIVE, self.PIERCING_PASSIVE, self.SPREAD_PASSIVE, self.HEAL_KILL, self.AMMO_KILL, self.COOLDOWN_KILL, self.DAMAGE_ROLL, self.SPEED_ROLL]
    
        

def randomItem():
    rarity = random.randint(1,20)
    if rarity==20:
        print("gave legendary")
    elif rarity>14 and rarity<20:
        print("gave uncommon")
    else:
        item = random.randint(0,len(ItemList.common_list)-1)
        return ItemList.common_list[item]
    return ItemList.AMMO2

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
        
        self.x, self.y = round(self.x),round(self.y)


def collision(x1, y1, x2, y2, size1, size2):
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1
App()