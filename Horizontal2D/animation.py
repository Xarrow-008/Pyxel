from world import TILE_SIZE

class Animation:
    def __init__(self):
        self.state = 0
        self.frame = 0
        self.tickrate = 1
        self.current_key = "N/A"

    def getImageInAnimation(self,length, w, key):
        self.resetFrames(key)
        u = self.state*w
        if self.tick():
            self.state+=1
        if self.state==length:
            self.state = 0
        v = key*TILE_SIZE
        return [u,v]
    
    def resetFrames(self, key):
        if key != self.current_key:
            self.state = 0
        self.current_key = key

    def tick(self):
        return self.frame % (30 * self.tickrate) == 0
