import pyxel
import math

SPRITEBANK = 0
TILE_SIZE = 8
WIDTH = 256
HEIGHT = 256

CAMERA_WIDTH = 128
CAMERA_HEIGHT = 128

loadedEntities = []

class App:
    def __init__(self):
        pyxel.init(CAMERA_WIDTH, CAMERA_HEIGHT, title="Roguelike", fps=120)
        pyxel.load("../roguelike.pyxres")
        
        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world)

        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        global loadedEntities


        self.player.update()

        for entity in loadedEntities:
            entity.update()

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.world = World(pyxel.tilemaps[0])
            self.player = Player(self.world)
            loadedEntities = []

    def draw(self):
        pyxel.cls(0)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                tile = self.world.world_map[y][x]
                draw_tile(pyxel, x, y, tile)

        for entity in loadedEntities:
            pyxel.blt(
                entity.x,
                entity.y,
                SPRITEBANK,
                entity.image[0],
                entity.image[1],
                entity.width,
                entity.height,
                colkey=11
            )

        pyxel.blt(
            self.player.x,
            self.player.y,
            SPRITEBANK,
            WorldItem.PLAYER[0]*TILE_SIZE,
            WorldItem.PLAYER[1]*TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
            colkey=11
            )

class WorldItem:
    PLAYER = (0,1)
    BLOCK = (1,0)
    BACKGROUND = (0,0)

    TILES = [BLOCK, BACKGROUND]

class World:

    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.world_map = []
        self.player_init_pos_x = 0
        self.player_init_pos_y = 0
        for y in range(HEIGHT):
            self.world_map.append([])
            for x in range(WIDTH):
                for tile in WorldItem.TILES:
                    if self.tilemap.pget(x,y) == tile:
                        self.world_map[y].append(tile)
                if self.tilemap.pget(x,y) == WorldItem.PLAYER:
                    self.player_init_pos_x = x
                    self.player_init_pos_y = y
                    self.world_map[y].append(WorldItem.BACKGROUND)

    
def draw_tile(pyxel, x, y, tile):
    pyxel.blt(x*TILE_SIZE,
                y*TILE_SIZE,
                SPRITEBANK,
                tile[0]*TILE_SIZE,
                tile[1]*TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
                )
    
class Player:
    def __init__(self, world):
        self.x = 0
        self.y = 0
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.world = world
        self.physics = Physics(world)
        self.camera = Camera(self)
        self.facing = [1,0]

        self.isDashing = False
        self.dashLength = 20
        self.dashFrame = 0
        self.dashCooldown = 10
        self.dashStrength = self.physics.speed*2.5

        self.gun = Guns.RIFLE
        self.gunFrame = 0

        self.max_health = 50
        self.health = 50

    def update(self):

        if self.health <= 0:
            print("player dead")

        self.camera.update()

        self.mousePositionInWorld_x = self.camera.x + pyxel.mouse_x
        self.mousePositionInWorld_y = self.camera.y + pyxel.mouse_y

        if not self.isDashing:

            if pyxel.btn(pyxel.KEY_Z):
                self.x, self.y = self.physics.move(self.x, self.y, [0,-1], TILE_SIZE, TILE_SIZE)
                self.facing[1] = -1
            if pyxel.btn(pyxel.KEY_S):
                self.x, self.y = self.physics.move(self.x, self.y, [0,1], TILE_SIZE, TILE_SIZE)
                self.facing[1] = 1
            if pyxel.btn(pyxel.KEY_Q):
                self.x, self.y = self.physics.move(self.x, self.y, [-1,0], TILE_SIZE, TILE_SIZE)
                self.facing[0] = -1
            if pyxel.btn(pyxel.KEY_D):
                self.x, self.y = self.physics.move(self.x, self.y, [1,0], TILE_SIZE, TILE_SIZE)
                self.facing[0] = 1
            if not(pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S)):
                self.facing[1] = 0
            if not(pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D)):
                self.facing[0] = 0

            if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_D) and self.physics.momentum<=self.physics.speed:
                self.physics.momentum = self.physics.speed
            else:
                self.physics.momentum /= 2
            
            self.dashFrame += 1

            if pyxel.btnp(pyxel.KEY_SPACE) and self.dashFrame >= self.dashCooldown:
                self.isDashing = True
                self.physics.momentum = self.dashStrength
                self.dashFrame = 0

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.gun["ammo"] > 0 and self.gunFrame >= self.gun["cooldown"]:
                self.gunFrame = 0
                self.gun["ammo"] -= 1
                horizontal = self.mousePositionInWorld_x-(self.x+self.width/2)
                vertical = self.mousePositionInWorld_y-(self.y+self.height/2)
                norm = math.sqrt(horizontal**2 + vertical**2)
                cos = horizontal/norm
                sin = vertical/norm                
                Bullet(self.x+self.width/2, self.y+self.height/2, [cos, sin], self.gun["damage"], self.gun["bullet_speed"], self.gun["range"] ,self.gun["piercing"], self.world, "player", (1*TILE_SIZE, 1*TILE_SIZE), 4, 4, self)

            if pyxel.btnp(pyxel.KEY_E):
                self.gun["ammo"] = 0
                self.gunFrame = 0

            if self.gun["ammo"]==0 and self.gunFrame >= self.gun["reload_time"]:
                self.gun["ammo"] = self.gun["max_ammo"]


            self.gunFrame += 1

        else:
            self.x, self.y = self.physics.move(self.x, self.y, self.facing, TILE_SIZE, TILE_SIZE)
            self.dashFrame += 1
            if self.dashFrame == self.dashLength:
                self.isDashing = False
                self.dashFrame = 0
            

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > WIDTH*TILE_SIZE:
            self.x = (WIDTH-1)*TILE_SIZE
        if self.y > HEIGHT*TILE_SIZE:
            self.y = (HEIGHT-1)*TILE_SIZE

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            Enemy(self.mousePositionInWorld_x, self.mousePositionInWorld_y, EnemyTemplate.DUMMY, self.world, self)

class Physics:
    def __init__(self, world):
        self.momentum = 0
        self.speed = 0.4
        self.collision_happened = False
        self.world = world

    def move(self, x, y, vector, width, height):

        tile_x = int(x//TILE_SIZE)
        tile_y = int(y//TILE_SIZE)

        new_x = x + self.momentum*vector[0]
        new_y = y + self.momentum*vector[1]
        
        new_tile_x = tile_x + pyxel.sgn(vector[0])
        new_tile_y = tile_y + pyxel.sgn(vector[1])

        if pyxel.sgn(vector[0]) != 0:
            next_tile_x_1 = self.world.world_map[tile_y][new_tile_x]
            if y != tile_y*TILE_SIZE:
                next_tile_x_2 = self.world.world_map[tile_y+1][new_tile_x]
            else:
                next_tile_x_2 = WorldItem.BACKGROUND
            if (next_tile_x_1 != WorldItem.BLOCK or not collision(new_x, y, new_tile_x*TILE_SIZE, tile_y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])) and (next_tile_x_2 != WorldItem.BLOCK or not collision(new_x, y, new_tile_x*TILE_SIZE, (tile_y+1)*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])):
                x = new_x
            elif (next_tile_x_1 == WorldItem.BLOCK or next_tile_x_2 == WorldItem.BLOCK) and (new_x+width>(new_tile_x)*TILE_SIZE and (new_tile_x)*TILE_SIZE+TILE_SIZE>new_x):
                self.collision_happened = True
                if pyxel.sgn(vector[0])==1:
                    x = (new_tile_x-1)*TILE_SIZE
                else:
                    x = (new_tile_x+1)*TILE_SIZE

        tile_x = int(x//TILE_SIZE)

        if pyxel.sgn(vector[1]) != 0:
            next_tile_y_1 = self.world.world_map[new_tile_y][tile_x]
            if x != tile_x*TILE_SIZE:
                next_tile_y_2 = self.world.world_map[new_tile_y][tile_x+1]
            else:
                next_tile_y_2 = WorldItem.BACKGROUND
            if (next_tile_y_1 != WorldItem.BLOCK or not collision(x, new_y, tile_x*TILE_SIZE, new_tile_y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])) and (next_tile_y_2 != WorldItem.BLOCK or not collision(x, new_y, (tile_x+1)*TILE_SIZE, new_tile_y*TILE_SIZE, [width, height], [TILE_SIZE, TILE_SIZE])):
                y = new_y
            elif (next_tile_y_1 == WorldItem.BLOCK or next_tile_y_2 == WorldItem.BLOCK) and (new_y+height>(new_tile_y)*TILE_SIZE and (new_tile_y)*TILE_SIZE+TILE_SIZE>new_y):
                self.collision_happened = True
                if pyxel.sgn(vector[1])==1:
                    y = (new_tile_y-1)*TILE_SIZE
                else:
                    y = (new_tile_y+1)*TILE_SIZE

        return x,y
    
def collision(x1,y1,x2,y2,size1, size2):
        return x1+size1[0]>x2 and x2+size2[0]>x1 and y1+size1[1]>y2 and y2+size2[1]>y1    

    
class Camera:
    def __init__(self, player):
        self.x = 0
        self.y = 0
        self.max_x = WIDTH*TILE_SIZE-CAMERA_WIDTH
        self.max_y = HEIGHT*TILE_SIZE-CAMERA_HEIGHT
        self.player = player
        self.LENIENCE_x = 4*TILE_SIZE
        self.LENIENCE_y = 4*TILE_SIZE

    def update(self):

        self.playerDistanceFromCenter_x = self.player.x - (self.x + CAMERA_WIDTH/2)
        self.playerDistanceFromCenter_y = self.player.y - (self.y + CAMERA_WIDTH/2)

        if self.playerDistanceFromCenter_x > self.LENIENCE_x:
            self.x += self.playerDistanceFromCenter_x - self.LENIENCE_x
        elif self.playerDistanceFromCenter_x < -self.LENIENCE_x:
            self.x += self.playerDistanceFromCenter_x + self.LENIENCE_x
        if self.playerDistanceFromCenter_y > self.LENIENCE_y:
            self.y += self.playerDistanceFromCenter_y - self.LENIENCE_y
        elif self.playerDistanceFromCenter_y < -self.LENIENCE_y:
            self.y += self.playerDistanceFromCenter_y + self.LENIENCE_y

        if self.x > self.max_x:
            self.x = self.max_x
        if self.x < 0:
            self.x = 0
        if self.y > self.max_y:
            self.y = self.max_y
        if self.y < 0:
            self.y = 0
        
        pyxel.camera(self.x, self.y)

class Guns:
    PISTOL = {"cooldown":40, "max_ammo":16, "ammo":16, "reload_time":240, "damage":5, "bullet_speed":1, "range":6*TILE_SIZE, "piercing":0}
    RIFLE = {"cooldown":20, "max_ammo":30, "ammo":30, "reload_time":480, "damage":4, "bullet_speed":1.25, "range":8*TILE_SIZE, "piercing":1}


class Bullet:
    def __init__(self, x, y, vector, damage, speed, range, piercing, world, owner, image, width, height, player):
        self.x = x
        self.y = y
        self.vector = vector
        self.damage = damage
        self.range = range
        self.piercing = piercing
        self.width = width
        self.height = height
        self.physics = Physics(world)
        self.physics.momentum = speed
        self.owner = owner
        self.player = player

        self.image = image


        self.type = "bullet"
        loadedEntities.append(self)

    def update(self):
        self.x, self.y = self.physics.move(self.x, self.y, self.vector, self.width, self.height)

        self.range -= math.sqrt(self.vector[0]**2 + self.vector[1]**2)

        for entity in loadedEntities:
            if self.owner == "player" and entity.type == "enemy" and collision(self.x, self.y, entity.x, entity.y, [self.width, self.height], [entity.width, entity.height]):
                entity.health -= self.damage
                if self.piercing == 0:
                    loadedEntities.remove(self)
                else:
                    self.piercing -= 1
            if self.owner=="enemy" and collision(self.x, self.y, self.player.x, self.player.y, [self.width, self.height], [self.player.width, self.player.height]):
                self.player.health -= self.damage
                if self.piercing == 0:
                    loadedEntities.remove(self)
                else:
                    self.piercing -= 1
                

        if self.physics.collision_happened or self.range <= 0:
            loadedEntities.remove(self)

class EnemyTemplate:
    DUMMY = {"health":50, "damage":10, "range":2.5*TILE_SIZE, "attack_cooldown":40, "attack_speed":0.75, "image":[0*TILE_SIZE, 2*TILE_SIZE], "speed":0.1, "width":TILE_SIZE, "height":TILE_SIZE}

class Enemy:
    def __init__(self, x, y, template, world, player):
        self.x = x
        self.y = y
        self.health = template["health"]
        self.damage = template["damage"]
        self.range = template["range"]
        self.attack_cooldown = template["attack_cooldown"]
        self.attackFrame = 0
        self.attack_sequence = 0
        self.attack_speed = template["attack_speed"]
        self.image = template["image"]
        self.world = world
        self.physics = Physics(world)
        self.physics.momentum = template["speed"]
        self.width = template["width"]
        self.height = template["height"]
        self.player = player
        self.type = "enemy"
        loadedEntities.append(self)

    def update(self):
        if self.health <= 0:
            loadedEntities.remove(self)
        if self.attack_sequence == 0:
            horizontal = self.player.x - self.x
            vertical = self.player.y - self.y
            norm = math.sqrt(horizontal**2 + vertical**2)
            cos = horizontal/norm
            sin = vertical/norm
            self.x, self.y = self.physics.move(self.x, self.y, [cos, sin], self.width, self.height)

        horizontal = self.player.x+self.player.width/2 - (self.x+self.width/2)
        vertical = self.player.y+self.player.height/2 - (self.y+self.height/2)
        norm = math.sqrt(horizontal**2 + vertical**2)
        cos = horizontal/norm
        sin = vertical/norm
        if norm<=self.range and self.attackFrame >= self.attack_cooldown and self.attack_sequence == 0:
            self.attackFrame = 0
            self.attack_sequence = 1
        
        if self.attack_sequence==1 and self.attackFrame >= 60:
            self.attack_sequence = 0
            self.attackFrame = 0
            Bullet(self.x+self.width/2, self.y+self.height/2, [cos, sin], self.damage, self.attack_speed, self.range, 0, self.world, "enemy", (1*TILE_SIZE, 2*TILE_SIZE), 3, 3, self.player)

        self.attackFrame += 1

App()
