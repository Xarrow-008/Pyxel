import pyxel, os, random, math

WIDTH = 200
HEIGHT = 200
TILE_SIZE = 8

CAM_WIDTH = 16*8
CAM_HEIGHT = 16*8

FPS = 120

loadedEntities = []
pickup_text = ["N/A"]

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
        self.game_start = 0

        
        pyxel.mouse(True)

        self.enemies_spawn()

        pyxel.run(self.update,self.draw)
    

    def update(self):
        if self.player.alive:
            self.player.update()
            for entity in loadedEntities:
                entity.itemList = self.itemList
                entity.update()

            for boost in activeBoosts:
                boost.update()

            self.camera.update(self.player)
            pyxel.camera(self.camera.x,self.camera.y)
        else:
            self.restartGame()
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
        if self.player.gun["ammo"] < self.player.gun["max_ammo"]:
            pyxel.text(self.camera.x+1, self.camera.y+19, "Press 'R' to reload", 7)

        if pickup_text != ["N/A"]:
            pyxel.text(self.camera.x+1, self.camera.y+127, "Press 'E' to pickup", 7)
            pyxel.text(self.camera.x+1, self.camera.y+133, pickup_text[0], 7)
            pyxel.text(self.camera.x+1, self.camera.y+139, pickup_text[1], 7)
    
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

    def restartGame(self):
        global pickUpsOnGround
        global loadedEntities
        loadedEntities = []
        pickUpsOnGround = []

        self.camera = Camera()
        self.world = World(pyxel.tilemaps[0],RoomBuild(0,WIDTH//2,0))
        self.player = Player(self.world, self.camera)
        self.itemList = ItemList(self.player)
        self.effects = ScreenEffect(self.player)
        self.game_start = pyxel.frame_count

        pyxel.mouse(True)
        self.enemies_spawn()      


def check_entity(loadedEntities, key, value):
    for entity in loadedEntities:
        if getattr(entity,key) == value:
            return True
    return False
    
def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0

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
            self.rooms.append({'name':i+1,'X':self.newX,'Y':self.newY,'W':self.newW,'H':self.newH,'connect':(self.newConnect[0],self.newConnect[1]),'direction':last_placement})

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
        if (x >= room['X'] and x < room['X']+room['W'] and y >= room['Y'] and y < room['Y']+room['H']) or (x >= room['connect'][0] and x < room['connect'][0]+2 and y >= room['connect'][1] and y < room['connect'][1]+2):
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

        self.gun = dic_copy(Guns.PISTOL)
        self.attackFrame = 0

        self.ownedItems = []
        self.justKilled = False

        self.camera = camera

    def update(self):

        current_room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)
        if current_room != 'None':
            self.room = current_room

        self.loadedEntitiesInRange = []

        for entity in loadedEntities:
            if in_perimeter(self.x,self.y,entity.x,entity.y,200):
                self.loadedEntitiesInRange.append(entity)

        self.posXmouse = self.camera.x+pyxel.mouse_x
        self.poxYmouse = self.camera.y+pyxel.mouse_y
        if not self.isDashing:
            self.movement()
            self.fireWeapon()
            self.reloadWeapon()
            self.dash()
        else:
            self.dashMovement()
        self.hitDetection()
        self.attackFrame += 1
        self.dashFrame += 1
        self.hitFrame += 1
        self.preventOOB()
        self.getPickupText()
        self.death()

        if self.health > self.max_health:
            self.health = self.max_health
        if self.gun["ammo"] > self.gun["max_ammo"]:
            self.gun["ammo"] = self.gun["max_ammo"]
        

    def movement(self):
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

        if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S) and self.physics.momentum <= self.speed:
            self.physics.momentum = self.speed
        else:
            self.physics.momentum /= self.speedFallOff

    def fireWeapon(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.attackFrame>=self.gun["cooldown"] and self.gun["ammo"]>0:
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
                if self.gun["name"] != "Grenade Launcher":
                    Bullet(self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.gun["damage"], self.gun["bullet_speed"], self.gun["range"], self.gun["piercing"], self.world, self, (0,6*TILE_SIZE), "player", 0)
                else:
                    Bullet(self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.gun["damage"], self.gun["bullet_speed"], self.gun["range"], self.gun["piercing"], self.world, self, (0,6*TILE_SIZE), "player", 1.5*TILE_SIZE)

    def reloadWeapon(self):
        if pyxel.btnp(pyxel.KEY_R) and self.gun["ammo"]<self.gun["max_ammo"] and self.gun["ammo"]!=0:
            self.gun["ammo"] = 0
            self.attackFrame = 0
            
        if self.gun["ammo"]==0 and self.attackFrame>=self.gun["reload"]:
            self.gun["ammo"]=self.gun["max_ammo"]

    def dash(self):
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_SHIFT)) and self.dashFrame >= self.dashCooldown:
            self.isDashing = True
            self.dashFrame = 0
            self.physics.momentum = self.speed*2.5
            self.image = [6,2]

    def dashMovement(self):
        self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.facing)
        if self.dashFrame >= self.dashLength:
            self.isDashing = False
            self.dashFrame = 0
            self.triggerOnDashItems()

    def hitDetection(self):
        if self.isHit and self.hitFrame >= self.hitLength:
                self.isHit = False
                self.hitFrame = 0

    def preventOOB(self):
        if self.x<0:
            self.x = 0
        if self.y<0:
            self.y = 0
        if self.x > WIDTH*TILE_SIZE:
            self.x = (WIDTH-1)*TILE_SIZE
        if self.y > HEIGHT*TILE_SIZE:
            self.y = (HEIGHT-1)*TILE_SIZE

    def getPickupText(self):
        global pickup_text
        self.collision_with_item = False
        for i in range(len(pickUpsOnGround)-1, -1, -1):
            pickup = pickUpsOnGround[i]
            if collision(self.x, self.y, pickup.x, pickup.y, [self.width, self.height], [pickup.width, pickup.height]):
                pickup_text = [pickup.object["name"], pickup.object["description"]]
                self.collision_with_item = True
            if not self.collision_with_item:
                pickup_text = ["N/A"]
        if len(pickUpsOnGround) == 0:
            pickup_text = ["N/A"]

    def death(self):
        if self.health<=0:
            self.alive = False

    def getItem(self, item):
        self.ownedItems.append(item)
        if item["trigger"] == "passive" and (item["effect"] == "stat_p" or item["effect"] == "stat_g"):
            for change in item["function"]:
                self.increaseStat(change[0], change[1], change[2])

    def changeWeapon(self, gun):
        self.gun = dic_copy(gun)
        for key in self.gun.keys():
            if key not in ["name", "description", "image", "rate", "bullet_count"]:
                lowest_value = self.gun[key]*0.9
                highest_value = self.gun[key]*1.1
                self.gun[key] = random.uniform(lowest_value, highest_value)
        self.gun["piercing"] = math.ceil(self.gun["piercing"])
        self.gun["max_ammo"] = math.ceil(self.gun["max_ammo"])
        self.gun["ammo"] = self.gun["max_ammo"]
        for item in self.ownedItems:
            if item["trigger"] == "passive" and item["effect"]=="stat_g":
                for change in item["function"]:
                    self.increaseStat(change[0], change[1], change[2])
        for boost in activeBoosts:
            if boost.target == "boost_g":
                self.increaseStat(boost.stat, boost.operation, boost.value)

    def increaseStat(self, stat, operation, value):
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
        elif stat == "ammo":
            if operation == "addition":
                self.gun["ammo"] += value
            elif operation == "multiplication":
                self.gun["ammo"] *= value
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
        
    def triggerOnKillItems(self):
        for item in self.ownedItems:
            if item["trigger"] == "onKill":
                if item["effect"] == "stat_p" or item["effect"] == "stat_g":
                    for change in item["function"]:
                        self.increaseStat(change[0], change[1], change[2])
                elif item["effect"] == "boost_p" or item["effect"] == "boost_p":
                    for change in item["function"]:
                        Boost(change[0], change[1], change[2], change[3], item["effect"], self)
        
    def triggerOnDashItems(self):
        for item in self.ownedItems:
            if item["trigger"] == "onDash":
                if item["effect"] == "stat_p" or item["effect"] == "stat_g":
                    for change in item["function"]:
                        self.increaseStat(change[0], change[1], change[2])
                elif item["effect"] == "boost_p" or item["effect"] == "boost_p":
                    for change in item["function"]:
                        Boost(change[0], change[1], change[2], change[3], item["effect"], self)

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
    PISTOL = {"damage":8, "bullet_speed":0.75, "range":6*TILE_SIZE, "piercing":0, "max_ammo":16, "ammo":16, "reload":1.5*120, "cooldown":1/3*120, "spread":0.1, "bullet_count":1, "name":"Pistol", "image":[1*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(1,31)], "description":"Basic weapon"}
    RIFLE = {"damage":10, "bullet_speed":0.9, "range":7*TILE_SIZE, "piercing":1, "max_ammo":24, "ammo":24, "reload":3*120, "cooldown":0.25*120, "spread":0.2, "bullet_count":1, "name":"Rifle", "image":[2*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(31,51)], "description":"High fire rate, medium damage"}
    SMG = {"damage":8, "bullet_speed":1, "range":4*TILE_SIZE, "piercing":0, "max_ammo":40, "ammo":40, "reload":2.5*120, "cooldown":0.17*120, "spread":0.55, "bullet_count":1, "name":"SMG", "image":[0*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(71,83)], "description":"Highest fire rate, low damage"}
    SNIPER = {"damage":20, "bullet_speed":2, "range":20*TILE_SIZE, "piercing":4, "max_ammo":4, "ammo":4, "reload":4*120, "cooldown":1*120, "spread":0, "bullet_count":1, "name":"Sniper", "image":[4*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(83,95)], "description":"Single fire, high damage"}
    SHOTGUN = {"damage":9, "bullet_speed":0.6, "range":4*TILE_SIZE, "piercing":0, "max_ammo":5, "ammo":5, "reload":3*120, "cooldown":0.75*120, "spread":0.6, "bullet_count":6, "name":"Shotgun", "image":[3*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(51,71)], "description":"Multiple pellets, medium damage"}
    GRENADE_LAUNCHER = {"damage":20, "bullet_speed":1.5, "range":20*TILE_SIZE, "piercing":0, "max_ammo":1, "ammo":1, "reload":1.5*120, "cooldown":1*120, "spread":0, "bullet_count":1, "name":"Grenade Launcher", "image":[5*TILE_SIZE,7*TILE_SIZE], "rate":[x for x in range(95,101)], "description":"Single fire, explosive shots"}
    Gun_list = [PISTOL, RIFLE, SMG, SNIPER, SHOTGUN, GRENADE_LAUNCHER]

class Bullet:
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
        loadedEntities.append(self)

    def update(self):
        self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.vector)
        self.check_hit()
        self.bullet_destroyed()
    
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
            self.player.isHit = True
            self.player.hitFrame = 0
        self.range -= math.sqrt((self.vector[0]*self.physics.momentum)**2+(self.vector[1]*self.physics.momentum)**2)
    
    def bullet_destroyed(self):
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
            loadedEntities.remove(self)

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

        self.p_objective= []
        self.loaded = False


        self.image = template["image"]
        self.width = template["width"]
        self.height = template["height"]

        self.pierced = []

        self.hitStun = False
        self.hitFrame = 0

        self.type = "enemy"

        loadedEntities.append(self)

    def update(self):
        
        if self in self.player.loadedEntitiesInRange:
            self.loaded = True
        else:
            self.loaded = False

        current_room = find_room(self.x//TILE_SIZE,self.y//TILE_SIZE,self.rooms)
        if current_room != 'None':
            self.room = current_room
        

        if self.hitStun:
            self.hitStunFunction()
        else:
            if self.loaded:
                self.image = [0,32]
                self.pathing()
                self.moveInPathing()
                self.enemies_pusharound()
                self.attack()
                self.lunge()
                self.lungeFrame += 1
                self.attackFrame += 1
                self.getImage()
                self.death()

    def hitStunFunction(self):
        if self.image[0]<16:
            self.image[0] += 32
        elif self.image[0]<32:
            self.image[0] += 16
        if self.hitFrame<=4:
            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [-self.cos*2, -self.sin*2])
        if self.hitFrame >= 24:
            self.hitStun = False
            self.hitFrame = 0
        self.hitFrame += 1

    def moveInPathing(self):
        if not self.isAttacking and self.isLunging == 0:
            if self.norm < 100 and self.norm > 5:
                self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [self.cos, self.sin])
    
    def enemies_pusharound(self):
        for entity in self.player.loadedEntitiesInRange:
            cos = random.randint(-200,200)/100
            sin = math.sqrt((2-cos)**2) * (random.randint(0,1)*2-1)
            if in_perimeter(self.x,self.y,entity.x,entity.y,3) and self != entity:
                if entity.type == "enemy" and collision(self.x, self.y, entity.x ,entity.y, [self.width, self.height], [entity.width, entity.height]):
                    self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [cos, sin])
                    entity.x ,entity.y = entity.physics.move(entity.x ,entity.y, entity.width, entity.height, [-cos, -sin])

    def attack(self):
        if self.isLunging == 0:
            if self.norm <= self.range and self.attackFrame >= self.attack_cooldown and not self.isAttacking:
                self.attackFrame = 0
                self.isAttacking = True
                self.attackVector = [self.cos, self.sin]
            if self.isAttacking and self.attackFrame >= self.attack_freeze:
                self.attackFrame = 0
                self.isAttacking = False
                Bullet(self.x+self.width/2, self.y+self.height/2, 3,3,self.attackVector, self.damage, self.attack_speed, self.range, 0, self.world, self.player,(256*TILE_SIZE,256*TILE_SIZE), "enemy", 0)
            
    def lunge(self):
        if not self.isAttacking:
            if self.norm<=self.lunge_range and self.norm>self.range and self.lungeFrame >= self.lunge_cooldown and self.isLunging==0:
                self.lungeFrame = 0
                self.isLunging = 1
                self.lungeVector = [self.cos, self.sin]
            if self.isLunging==1 and self.lungeFrame >= self.lunge_freeze:
                self.lungeFrame = 0
                self.isLunging = 2
                self.physics.momentum = self.lunge_speed
            if self.isLunging==2:
                self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.lungeVector)
                if self.lungeFrame >= self.lunge_length:
                    self.isLunging=0
                    self.physics.momentum = self.speed

    def getImage(self):
        if abs(self.horizontal)>abs(self.vertical):
            self.image[1] = 32
            if self.horizontal>0:
                self.image[0] = 0
            else:
                self.image[0] = 8
        else:
            self.image[1] = 40
            if self.vertical>0:
                self.image[0] = 0
            else:
                self.image[0] = 8

        if self.isLunging == 1:
            if self.image[0]<16:
                self.image[0] +=16

    def death(self):
        if self.health <= 0:

            item_chance = 10
            gun_chance = 10

            pickup = random.randint(1,100)
            if pickup <= item_chance:
                item_rarity = random.randint(1,20)
                if item_rarity == 20:
                    print("gave legendary item")
                elif item_rarity>15 and item_rarity<20:
                    print("gave uncommon item")
                else:
                    item_random = random.randint(0, len(self.itemList.common_list)-1)
                    item = self.itemList.common_list[item_random]
                    PickUp(self.x, self.y, "item", item, self.player)

            elif pickup > 100-gun_chance:
                gun_random = random.randint(1,100)
                for gun in Guns.Gun_list:
                    if gun_random in gun["rate"]:
                        PickUp(self.x, self.y, "weapon", gun, self.player)

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
            elif self.room['name']<self.player.room['name']:
                x_con = self.rooms[self.room['name']+1]['connect'][0]
                y_con = self.rooms[self.room['name']+1]['connect'][1]
            
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
                y_entry = y_con-3
                x_exit = x_con+0.5
                y_exit = y_con-1
            
            if distance(self.x, self.y, x_exit*TILE_SIZE,y_exit*TILE_SIZE)>TILE_SIZE*5:
                self.horizontal = x_entry*TILE_SIZE - self.x
                self.vertical = y_entry*TILE_SIZE - self.y
            else:
                self.horizontal = x_exit*TILE_SIZE - self.x
                self.vertical = y_exit*TILE_SIZE - self.y
                    
        self.norm = math.sqrt(self.horizontal**2+self.vertical**2)
        if self.norm != 0:
            self.cos = self.horizontal/self.norm
            self.sin = self.vertical/self.norm
        else:
            self.cos = 0
            self.sin = 0

            
def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def in_perimeter(x1,y1,x2,y2,distance):
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

pickUpsOnGround = []

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
        pickUpsOnGround.append(self)

    def update(self):
        if collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]):
            if pyxel.btnp(pyxel.KEY_E):
                if self.type == "weapon":
                    self.player.changeWeapon(self.object)
                if self.type == "item":
                    self.player.getItem(self.object)
                loadedEntities.remove(self)
                pickUpsOnGround.remove(self)

class ItemList:
    def __init__(self, player):
        self.player = player
        self.SPEED_PASSIVE = {"name":"Jet Fuel", "description":"Slightly increases movement speed", "image":[1*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_p", "function":[["speed", "addition", 0.05]]}
        self.HEALTH_PASSIVE = {"name":"Armor Plating", "description":"Slightly increases health", "image":[0*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_p", "function":[["max_health", "addition", 5], ["health", "addition", 5]]}
        self.RANGE_PASSIVE = {"name":"Aerodynamism", "description":"Slighlty increases your gun's range", "image":[2*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_g", "function":[["range", "multiplication", 1.2]]}
        self.PIERCING_PASSIVE = {"name":"Sharpened Rounds", "description":"Increase your gun's piercing by 1", "image":[3*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_g", "function":[["piercing", "addition", 1]]}
        self.SPREAD_PASSIVE = {"name":"Focused Fire", "description":"Slightly decreases your gun's spread", "image":[4*TILE_SIZE,8*TILE_SIZE], "trigger":"passive", "rarity":"common", "effect":"stat_g", "function":[["spread", "multiplication", 0.9]]}
        self.HEAL_KILL = {"name":"Compost", "description":"Get a small heal on kill", "image":[5*TILE_SIZE,8*TILE_SIZE], "trigger":"onKill", "rarity":"common", "effect":"stat_p", "function":[["health", "addition", 7]]}
        self.AMMO_KILL = {"name":"Reduce, Reuse, Recycle", "description":"Gain ammo back on kill", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common", "effect":"stat_g", "function":[["ammo", "addition", 3]]}
        self.SPEED_KILL = {"name":"Blood is fuel", "description":"Gain a speed boost on kill", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common", "effect":"boost_p", "function":[["speed", "addition", 0.1, 1*120]]}
        self.DAMAGE_DASH = {"name":"Terminal Velocity", "description":"Gain a damage boost after dash", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onDash", "rarity":"common", "effect":"boost_g", "function":[["damage", "addition", 3, 1.5*120]]}
        self.SPEED_DASH = {"name":"Inertia", "description":"Gain a speed boost after dash", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onDash", "rarity":"common", "effect":"boost_p", "function":[["speed", "addition", 0.2, 1.5*120]]}
        self.common_list = [self.SPEED_PASSIVE, self.HEALTH_PASSIVE, self.RANGE_PASSIVE, self.PIERCING_PASSIVE, self.SPREAD_PASSIVE, self.HEAL_KILL, self.AMMO_KILL, self.SPEED_KILL, self.DAMAGE_DASH, self.SPEED_DASH]

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

class Effect:
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
    
    def update(self):
        if self.frame == self.durations[self.state]:
            self.image[0] += TILE_SIZE
            self.state += 1
            self.frame = 0
        if self.state == self.length :
            loadedEntities.remove(self)
        self.frame += 1

activeBoosts = []

class Boost:
    def __init__(self, stat, operation, value, duration, target, player):
        self.stat = stat
        self.operation = operation
        self.value = value
        self.duration = duration
        self.frame = 0
        self.player = player
        self.target = target
        self.player.increaseStat(self.stat, self.operation, self.value)
        activeBoosts.append(self)

    def update(self):
        if self.frame >= self.duration:
            if self.operation == "addition":
                self.player.increaseStat(self.stat, self.operation, -self.value)
            elif self.operation == "multiplication":
                self.player.increaseStat(self.stat, self.operation, 1/self.value)
            activeBoosts.remove(self)
        self.frame += 1

def collision(x1, y1, x2, y2, size1, size2):
    return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1
App()