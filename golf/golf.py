import os, random, math, pyxel

T_SIZE = 16

class Golf:
    def __init__(self):
        pyxel.init(128,128,title='golfing balls',fps=120)
        pyxel.load('../golf.pyxres')

        self.world = World(pyxel.tilemaps[0])
        self.ball = Ball(self.world)

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)
    
    def update(self):
        self.ball.update()

    def draw(self):
        pyxel.cls(0)

        draw_map(self.world.map)

        pyxel.blt(
            self.ball.x,
            self.ball.y,
            0,
            0,
            32,
            8,
            8,
            colkey=15
        )

        if self.ball.clic_hold:
            pyxel.blt(
                self.ball.bar_x,
                self.ball.bar_y,
                0,
                0,
                64,
                T_SIZE,
                4,
                colkey= 15,
            )
            pyxel.blt(
                round(self.ball.bar_x)+0.25,
                round(self.ball.bar_y)+0.25,
                0,
                0,
                68,
                self.ball.bar_fill,
                4,
                colkey= 15,
            )
            pyxel.blt(
                self.ball.x-4 + self.ball.current_cos*8,
                self.ball.y+2 + self.ball.current_sin*8,
                0,
                0,
                72,
                T_SIZE,
                1,
                colkey= 15,
                rotate= (math.acos(self.ball.current_cos) * pyxel.sgn(self.ball.vertical))*180/math.pi
            )
class Blocks:

    WALL_FULL = (0,1)
    WALL_LEFT = (1,0)
    WALL_RIGHT = (2,0)
    WALL_UP = (1,1)
    WALL_DOWN = (2,1)
    
    CORNER_LEFT = (1,2)
    CORNER_RIGHT = (2,2)
    CORNER_UP = (1,3)
    CORNER_DOWN = (2,3)

    WALLS = [WALL_FULL,WALL_LEFT,WALL_RIGHT,WALL_UP,WALL_DOWN,CORNER_LEFT,CORNER_RIGHT,CORNER_UP,CORNER_DOWN]

class World:
    def __init__(self,tilemap):
        self.tilemap = tilemap
        self.map = [[(0,0) for x in range(8)] for y in range(8)]
        self.init_course1()

    def init_course1(self):
        self.course1 = {'tilemap':(0,0),'ball_pos':(8,0),'flag_pos':(64,24)}
        for y in range(8):
            for x in range(8):
                for wall in Blocks.WALLS:
                    if self.tilemap.pget(x*2,y*2) == (wall[0]*2,wall[1]*2):
                        self.map[y][x] = wall

class Ball:
    def __init__(self,world):
        self.world = world
        self.x = self.world.course1['ball_pos'][0]
        self.y = self.world.course1['ball_pos'][1]
        self.speed = 0
        self.max_speed = 2
        self.clic_hold = False
        self.release = False
        self.start_hold = (0,0)
        self.end_hold = (0,0)
        self.moving = False

        self.horizontal = 0
        self.vertical = 0
        self.cos = 0
        self.sin = 0

        self.bar_x = 0
        self.bar_y = 0
        self.bar_fill = 0
        
    def update(self):
        draw_map(self.world.map) #puisque les collisions se font avec les couleurs, on redessine tte la map

        if self.speed <= 0.01:
            self.speed = 0
            self.moving = False

        self.clic_gestion()
    
        self.get_mouse_angle()

        if self.release:
            self.release_ball()
        
        if self.speed > 0.01:
            self.move()
            self.preventOOB()
            self.collision_walls()

    
    def move(self):
        self.x = self.x + self.cos*self.speed
        self.y = self.y + self.sin*self.speed
        self.speed += -0.005
    
    def preventOOB(self):

        if self.x<0:
            self.x = 0
            self.cos *= -1
        elif self.x > 128-8:
            self.x = 128-8
            self.cos *= -1

        if self.y<0:
            self.y = 0
            self.sin *= -1
        elif self.y > 128-8:
            self.y = 128-8
            self.sin *= -1

    def collision_walls(self):
        if pyxel.pget(self.x - 1, self.y + 4) == 1 and self.cos < 0:
            self.cos *= -1
        if pyxel.pget(self.x + 8, self.y + 4) == 1 and self.cos > 0:
            self.cos *= -1
        if pyxel.pget(self.x + 4, self.y - 1) == 1 and self.sin < 0:
            self.sin *= -1
        if pyxel.pget(self.x + 4, self.y + 8) == 1 and self.sin > 0:
            self.sin *= -1

    def clic_gestion(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not self.moving:
            if not self.clic_hold:
                self.start_hold = (pyxel.mouse_x,pyxel.mouse_y)
            
            self.clic_hold = True
            self.get_bar_pos()
        else:
            if self.clic_hold:
                self.release = True
                self.clic_hold = False
            else:
                self.release = False

    def release_ball(self):
        self.moving = True
        self.cos,self.sin = self.current_cos,self.current_sin
        if self.norm/50 > self.max_speed:
            self.speed = self.max_speed
        else:
            self.speed = self.norm/50


    def get_mouse_angle(self):
        self.horizontal = self.start_hold[0] - pyxel.mouse_x
        self.vertical = self.start_hold[1] - pyxel.mouse_y  
        self.norm = math.sqrt(self.horizontal**2+self.vertical**2)
        if self.norm != 0:
            self.current_cos = self.horizontal/self.norm
            self.current_sin = self.vertical/self.norm
        else:
            self.current_cos = 0
            self.current_sin = 0
        
        
    def get_bar_pos(self):
        if self.y < 10:
            self.bar_y = self.y + 10
        else:
            self.bar_y = self.y - 6
        
        if self.x < 4:
            self.bar_x = self.x + 2
        elif self.x > 128 - 8 - 5:
            self.bar_x = self.x - 8
        else:
            self.bar_x = self.x - 4

        if self.norm/50 > self.max_speed:
            capped_norm = self.max_speed
        else:
            capped_norm = self.norm/50
        
        self.bar_fill = capped_norm*15/self.max_speed


def draw_block(x,y,block):
    pyxel.blt(x,y,0,block[0]*T_SIZE,block[1]*T_SIZE,T_SIZE,T_SIZE)

def draw_map(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            draw_block(x*T_SIZE,y*T_SIZE,map[y][x])
        


def on_tick(tickrate=60):
    return pyxel.frame_count % tickrate == 0   

Golf()