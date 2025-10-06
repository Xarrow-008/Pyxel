import pyxel, os, math, random

WID = 850 // 1
HEI = 500 // 1


class Universe:
    def __init__(self):
        pyxel.init(width=WID, height=HEI, title='balls', fps=120, display_scale=2)
        os.system('cls')

        self.ballpit = []
        self.bg_color = 1
        self.addballs(100)
        #self.ballpit.append(Vector())
        pyxel.mouse(True)

        pyxel.run(self.update,self.draw)

    def update(self):
        for ball in self.ballpit:
            ball.update()
    def draw(self):
        pyxel.cls(self.bg_color)
        
        for ball in self.ballpit:
            ball.draw()
    
    def addballs(self,nb):
        for i in range(nb):
            self.ballpit.append(Ball(random.randint(0,WID),random.randint(0,HEI),random.randint(5,10),self.ballpit))


class Ball:
    def __init__(self,x,y,size,ballpit):
        self.x = x
        self.y = y
        self.size = size
        self.ballpit = ballpit
        self.move_vector = [0,0]

    def update(self):
        self.movement_gestion()
        self.move()

        self.apply_limits()

    def movement_gestion(self):
        self.close_push(x=pyxel.mouse_x, y=pyxel.mouse_y, push_distance=100, strength=1)
        self.balls_push(push_distance=10,strength=0.1)
    
    def close_push(self,x,y,push_distance,strength):
        vect_len = distance(self.x, self.y, x, y)
        if vect_len < push_distance:
            
            distance_point = [self.x - x, self.y - y]

            if vect_len == 0:
                angle = random.randrange(0,7)
                self.move_vector[0] = math.cos(angle) * 50
                self.move_vector[1] = math.cos(angle) * 50
            else:
                Dx = distance_point[0]
                Dy = distance_point[1]
                self.move_vector[0] = Dx * 100/ vect_len**2
                self.move_vector[1] = Dy * 100/ vect_len**2

            self.move_vector[0] *= strength
            self.move_vector[1] *= strength

    def balls_push(self,push_distance,strength):
        balls_close = []
        for ball in self.ballpit:
            if in_perimeter(self.x,self.y,ball.x,ball.y,push_distance):
                if ball != self:
                    balls_close.append((ball.x,ball.y,ball.size*2))

        for ball in balls_close:
            self.close_push(x=ball[0], y=ball[1], push_distance=ball[2], strength=strength)



    def move(self):
        self.x += self.move_vector[0]
        self.y += self.move_vector[1]
        
        self.move_vector[0] *= 0.99
        self.move_vector[1] *= 0.99

    
    def apply_limits(self):
        self.limits_border_bounce()

        if abs(self.move_vector[0]) < 0.001:
            self.move_vector[0] = 0
        if abs(self.move_vector[1]) < 0.001:
            self.move_vector[1] = 0
    

    def limits_border_stop(self):
        if self.x < 0:
            self.x = 0
            self.move_vector[0] = 0
        if self.y < 0:
            self.y = 0
            self.move_vector[1] = 0

        if self.x + self.size*2 > WID:
            self.x = WID - self.size*2
        if self.y + self.size*2 > HEI:
            self.y = HEI - self.size*2
    
    def limits_border_bounce(self):
        if self.x < 0:
            self.x = 0
            self.move_vector[0] *= -2
        if self.y < 0:
            self.y = 0
            self.move_vector[1] *= -2

        if self.x + self.size*2 > WID:
            self.x = WID - self.size*2
            self.move_vector[0] *= -1
        if self.y + self.size*2 > HEI:
            self.y = HEI - self.size*2
            self.move_vector[1] *= -1



    def draw(self):
        pyxel.circ(self.x,self.y,self.size,0)


class Vector:
    def __init__(self):
        self.x = WID//2
        self.y = HEI//2
        self.move_vector = [0,0]
    def update(self):
        angle = pyxel.frame_count / 60
        self.move_vector[0] = math.cos(math.pi) * -100
        self.move_vector[1] = math.sin(math.pi) * 100


        
        
    def draw(self):
        pyxel.line(self.x,self.y,self.x+self.move_vector[0],self.y+self.move_vector[1],7)


def show(x, y, img, asset, colkey=None, rotate=None, scale=1):
    pyxel.blt(x + 10//2*(scale-1), y + 10//2*(scale-1), img, asset[0]*11, asset[1]*11, 10, 10, colkey=colkey, rotate=rotate, scale=scale)

def icon(x, y, img, asset_name, crossed_condition=False, colkey=5, scale=1):
    show(x, y, img, ASSETS[asset_name],colkey=colkey, scale=scale)
    if crossed_condition:
        show(x, y, img, ASSETS['cross'],colkey=colkey,scale=scale)

def on_tick(tickrate=60,delay=0): #allows the computer to make operations only on certain times to not do averything 120 times a second
    return (pyxel.frame_count % tickrate)-delay == 0

def distance(x1,y1,x2,y2): #looks at distance with pythagorean theorem
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def in_perimeter(x1,y1,x2,y2,distance): #makes a square and checks if coords are inside of it
    return (x1-x2<distance and x1-x2>-distance) and (y1-y2<distance and y1-y2>-distance)

Universe()