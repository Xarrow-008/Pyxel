import pyxel, os, random, math

WIDTH = 200
HEIGHT = 200
TILE_SIZE = 8

CAM_WIDTH = 16*8
CAM_HEIGHT = 16*8

loadedEntities = []

class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(CAM_WIDTH,CAM_HEIGHT,title='Not a Scrap', fps=120)
        pyxel.load('../notAScrap.pyxres')
        self.camera = Camera()
        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world, self.camera)

        pyxel.mouse(True)

        
        for i in range(1,len(self.world.rooms)):
            Enemy(self.world.rooms[i]['X']*TILE_SIZE,self.world.rooms[i]['Y']*TILE_SIZE,EnemyTemplates.BASE,self.player,self.world)
        
        pyxel.run(self.update,self.draw)
    

    def update(self):
        self.player.update()
        for entity in loadedEntities:
            entity.update()

        self.camera.update(self.player)
        pyxel.camera(self.camera.x,self.camera.y)
    
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

        pyxel.text(self.camera.x+1, self.camera.y+1, "Health:"+str(self.player.health)+"/"+str(self.player.max_health),8)
        pyxel.text(self.camera.x+1, self.camera.y+7, "Weapon:"+str(self.player.gun["name"]),7)
        pyxel.text(self.camera.x+1, self.camera.y+13, "Ammo:"+str(self.player.gun["ammo"])+"/"+str(self.player.gun["max_ammo"]),7)


class WorldItem:
    WALL = (0,0)
    GROUND = (0,1)
    CONNECT = (1,1)

    BLOCKS = [WALL,GROUND]

class World:
    def __init__(self,tilemap):
        self.tilemap = tilemap
        self.world_map = []
        self.player_init_posX = WIDTH//2+2
        self.player_init_posY = 0
        self.nb_rooms = 20
        for y in range(HEIGHT):
            self.world_map.append([])
            for x in range(WIDTH):
                for block in WorldItem.BLOCKS:
                    if block == self.tilemap.pget(x,y):
                        self.world_map[y].append(self.tilemap.pget(x,y))
        
        self.rooms = []
        self.current_room = {'path':[0],'name':0,'X':WIDTH//2,'Y':0,'width':4,'height':4,'connect':[WIDTH//2+1,3]}
        self.new_room = {'path':[0],'name':0,'X':0,'Y':0,'width':4,'height':4,'connect':[WIDTH//2+1,3]}
        self.rooms.append(dic_copy(self.current_room))
        last_down = False
        rect_append(self.world_map, self.current_room['X'], self.current_room['Y'], self.current_room['width'], self.current_room['height'], WorldItem.GROUND)
        for j in range(self.nb_rooms):
            self.new_room['path'] = listcopy(self.current_room['path'])
            self.new_room['path'].append(self.current_room['path'][-1]+1)
            self.new_room['name'] = self.new_room['path'][-1]
            self.new_room['width'] = random.randint(2,5)*2
            self.new_room['height'] = random.randint(2,5)*2
            if last_down:
                sq_pos = random.randint(0,2)
                if sq_pos == 0 and self.current_room['X']>8:
                    self.new_room['connect'][0] = self.current_room['X'] - 2
                    self.new_room['connect'][1] = self.current_room['Y'] + random.randint(1,self.current_room['height']-2)
                    self.new_room['X'] = self.new_room['connect'][0] - self.new_room['width']
                    self.new_room['Y'] = self.new_room['connect'][1] - random.randint(1,self.new_room['height']-2)
                    last_down = False
                elif sq_pos == 1 and self.current_room['X']<WIDTH-8:
                    self.new_room['connect'][0] = self.current_room['X'] + self.current_room['width']
                    self.new_room['connect'][1] = self.current_room['Y'] + random.randint(1,self.current_room['height']-2)
                    self.new_room['X'] = self.new_room['connect'][0] +2
                    self.new_room['Y'] = self.new_room['connect'][1] - random.randint(1,self.new_room['height']-2)
                    last_down = False
                else:
                    self.new_room['connect'][0] = self.current_room['X'] + random.randint(1,self.current_room['width']-2)
                    self.new_room['connect'][1] = self.current_room['Y'] + self.current_room['height']+1
                    self.new_room['X'] = self.new_room['connect'][0] - random.randint(0,self.new_room['width']-2)
                    self.new_room['Y'] = self.new_room['connect'][1] +1


            else:
                self.new_room['connect'][0] = self.current_room['X'] + random.randint(1,self.current_room['width']-2)
                self.new_room['connect'][1] = self.current_room['Y'] + self.current_room['height']+1
                self.new_room['X'] = self.new_room['connect'][0] - random.randint(0,self.new_room['width']-2)
                self.new_room['Y'] = self.new_room['connect'][1] +1
                last_down = True
            
            rect_append(self.world_map,self.new_room['connect'][0],self.new_room['connect'][1]-1, 2, 2, WorldItem.CONNECT)
            rect_append(self.world_map, self.new_room['X'], self.new_room['Y'], self.new_room['width'], self.new_room['height'], WorldItem.GROUND)
            self.rooms.append(dic_copy(self.new_room))
            self.current_room = dic_copy(self.new_room)

class Furniture:
    def __init(self,world):
        self.world = world

def dic_copy(dico):
    dicoC = {}
    for key in dico.keys():
        dicoC[key]=dico[key]
    return dicoC


def listcopy(listP):
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

def rect_append(world_map, x, y, w, h, block): #verified+
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

class Player:
    def __init__(self, world, camera):
        self.x = world.player_init_posX*TILE_SIZE
        self.y = world.player_init_posY
        self.image = (1,3)
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.world = world

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

        self.gun = Guns.SHOTGUN
        self.attackFrame = 0

        self.ownedItems = []
        self.justKilled = False

        self.camera = camera

    def update(self):
        self.posXmouse = self.camera.x+pyxel.mouse_x
        self.poxYmouse = self.camera.y+pyxel.mouse_y
        if not self.isDashing:
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

                    Bullet(self.x+self.width/2, self.y+self.height/2, 4, 4, [cos, sin], self.gun["damage"], self.gun["bullet_speed"], self.gun["range"], self.gun["piercing"], self.world, self, (0,6*TILE_SIZE), "player")

            if pyxel.btnp(pyxel.KEY_R) and self.gun["ammo"]<self.gun["max_ammo"] and self.gun["ammo"]!=0:
                self.gun["ammo"] = 0
                self.attackFrame = 0
            
            if self.gun["ammo"]==0 and self.attackFrame>=self.gun["reload"]:
                self.gun["ammo"]=self.gun["max_ammo"]

            if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_SHIFT)) and self.dashFrame >= self.dashCooldown:
                self.isDashing = True
                self.dashFrame = 0
                self.physics.momentum = self.speed*2.5
        else:
            self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.facing)
            if self.dashFrame >= self.dashLength:
                self.isDashing = False
                self.dashFrame = 0

        self.attackFrame += 1
        self.dashFrame += 1

        if self.x<0:
            self.x = 0
        if self.y<0:
            self.y = 0
        if self.x > WIDTH*TILE_SIZE:
            self.x = (WIDTH-1)*TILE_SIZE
        if self.y > HEIGHT*TILE_SIZE:
            self.y = (HEIGHT-1)*TILE_SIZE

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            Enemy(self.posXmouse, self.poxYmouse, EnemyTemplates.BASE, self, self.world)

        if pyxel.btnp(pyxel.KEY_P):
            self.getItem(randomItem())
            print(self.ownedItems)

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

    def getItem(self, item):
        self.ownedItems.append(item)
        if item["name"] == "speed_passive":
            self.speed += 0.15
        if item["name"] == "health_passive":
            self.max_health += 10
            self.health += 10
        if item["name"] == "range_passive":
            self.gun["range"] *= 1.2
        if item["name"] == "ammo_passive":
            self.gun["max_ammo"] += 5
            self.gun["ammo"] += 5

    def changeWeapon(self, gun):
        self.gun = gun
        for item in self.ownedItems:
            if item["name"] == "range_passive":
                self.gun["range"] *= 1.2
            if item["name"] == "ammo.passive":
                self.gun["max_ammo"] += 5
                self.gun["ammo"] += 5


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
    PISTOL = {"damage":4, "bullet_speed":0.75, "range":6*TILE_SIZE, "piercing":0, "max_ammo":16, "ammo":16, "reload":1.5*120, "cooldown":1/3*120, "spread":0.1, "bullet_count":1, "name":"Pistol", "image":[1*TILE_SIZE,6*TILE_SIZE], "rate":[x for x in range(1,31)]}
    RIFLE = {"damage":3, "bullet_speed":0.9, "range":7*TILE_SIZE, "piercing":1, "max_ammo":24, "ammo":24, "reload":3*120, "cooldown":0.25*120, "spread":0.2, "bullet_count":1, "name":"Rifle", "image":[1*TILE_SIZE,6*TILE_SIZE], "rate":[x for x in range(31,51)]}
    SMG = {"damage":2, "bullet_speed":1, "range":4*TILE_SIZE, "piercing":0, "max_ammo":40, "ammo":40, "reload":2.5*120, "cooldown":0.1*120, "spread":0.4, "bullet_count":1, "name":"SMG", "image":[1*TILE_SIZE,6*TILE_SIZE], "rate":[x for x in range(71,83)]}
    SNIPER = {"damage":20, "bullet_speed":2, "range":20*TILE_SIZE, "piercing":5, "max_ammo":4, "ammo":4, "reload":4*120, "cooldown":1*120, "spread":0, "bullet_count":1, "name":"Sniper", "image":[1*TILE_SIZE,6*TILE_SIZE], "rate":[x for x in range(83,95)]}
    SHOTGUN = {"damage":6, "bullet_speed":0.6, "range":4*TILE_SIZE, "piercing":0, "max_ammo":5, "ammo":5, "reload":3*120, "cooldown":0.75*120, "spread":0.6, "bullet_count":6, "name":"Shotgun", "image":[1*TILE_SIZE,6*TILE_SIZE], "rate":[x for x in range(51,71)]}
    GRENADE_LAUNCHER = {"damage":15, "bullet_speed":1.5, "range":20*TILE_SIZE, "piercing":0, "max_ammo":1, "ammo":1, "reload":2.5*120, "cooldown":1.5*120, "spread":0, "bullet_count":1, "name":"Grenade Launcher", "image":[1*TILE_SIZE,6*TILE_SIZE], "rate":[x for x in range(95,101)]}
    Gun_list = [PISTOL, RIFLE, SMG, SNIPER, SHOTGUN, GRENADE_LAUNCHER]


class Bullet:
    def __init__(self, x, y, width, height, vector, damage, speed, range, piercing, world, player, image, owner):
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
        self.type = "bullet"
        self.piercing = piercing
        loadedEntities.append(self)

    def update(self):
        self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, self.vector)
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

        if self.physics.collision_happened or self.range <= 0 or self.piercing<0:
            loadedEntities.remove(self)

class EnemyTemplates:
    BASE = {"health":50, "speed":0.2, "damage":5, "range":2.5*TILE_SIZE, "attack_freeze":40, "attack_cooldown":240, "attack_speed":1.5, "lunge_range":6*TILE_SIZE, "lunge_freeze":40, "lunge_length":20, "lunge_speed":0.75,"lunge_cooldown":4*120, "image":[1*TILE_SIZE,4*TILE_SIZE], "width":TILE_SIZE, "height":TILE_SIZE}

class Enemy:
    def __init__(self, x, y, template, player, world):
        self.x = x
        self.y = y
        self.player = player
        self.world = world
        self.physics = Physics(world)

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

        if self.hitStun:
            if self.hitFrame >= 24:
                self.hitStun = False
                self.hitFrame = 0
            self.hitFrame += 1
        else:

            if not self.isAttacking and self.isLunging == 0:
                horizontal = self.player.x - self.x
                vertical = self.player.y - self.y
                norm = math.sqrt(horizontal**2+vertical**2)
                if norm != 0:
                    cos = horizontal/norm
                    sin = vertical/norm
                else:
                    cos = 0
                    sin = 0
                self.x, self.y = self.physics.move(self.x, self.y, self.width, self.height, [cos, sin])

            if self.isLunging == 0:
                horizontal = self.player.x - self.x
                vertical = self.player.y - self.y
                norm = math.sqrt(horizontal**2+vertical**2)
                if norm != 0:
                    cos = horizontal/norm
                    sin = vertical/norm
                else:
                    cos = 0
                    sin = 0
                if norm <= self.range and self.attackFrame >= self.attack_cooldown and not self.isAttacking:
                    self.attackFrame = 0
                    self.isAttacking = True
                    self.attackVector = [cos, sin]
                if self.isAttacking and self.attackFrame >= self.attack_freeze:
                    self.attackFrame = 0
                    self.isAttacking = False
                    Bullet(self.x+self.width/2, self.y+self.height/2, 3,3,self.attackVector, self.damage, self.attack_speed, self.range, 0, self.world, self.player,(256*TILE_SIZE,256*TILE_SIZE), "enemy")
            
            if not self.isAttacking:
                horizontal = self.player.x - self.x
                vertical = self.player.y - self.y
                norm = math.sqrt(horizontal**2+vertical**2)
                if norm != 0:
                    cos = horizontal/norm
                    sin = vertical/norm
                else:
                    cos = 0
                    sin = 0
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

        if self.health <= 0:
            self.player.justKilled = True

            pickup = random.randint(1,100)
            if pickup > 75:
                gun_random = random.randint(1,100)
                for gun in Guns.Gun_list:
                    if gun_random in gun["rate"]:
                        PickUp(self.x, self.y, "weapon", gun, self.player)

            loadedEntities.remove(self)

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
                print(self.object)
                self.player.changeWeapon(self.object)
            if self.type == "item":
                self.player.getItem(self.object)
            loadedEntities.remove(self)

class ItemList:
    SPEED = {"name":"speed_passive", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"passive", "rarity":"common"}
    HEALTH = {"name":"health_passive", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"passive", "rarity":"common"}
    AMMO1 = {"name":"ammo_passive", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"passive", "rarity":"common"}
    HEAL = {"name":"heal_on_kill", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common"}
    AMMO2 = {"name":"ammo_on_kill", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common"}
    COOLDOWN = {"name":"cooldown_on_hit", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onHit", "rarity":"common"}
    DAMAGE = {"name":"damage_on_roll", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onRoll", "rarity":"common"}
    SPEED2 = {"name":"speed_on_roll", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onRoll", "rarity":"common"}
    RANGE = {"name":"range_passive", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"passive", "rarity":"common"}
    BULLET_SPEED = {"name":"bullet_speed_on_kill", "description":"placeholder", "image":[1*TILE_SIZE,6*TILE_SIZE], "trigger":"onKill", "rarity":"common"}
    common_list = [SPEED, HEALTH, AMMO1, HEAL, AMMO2, COOLDOWN, DAMAGE, SPEED2, RANGE, BULLET_SPEED]

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
