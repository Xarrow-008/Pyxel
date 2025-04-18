from world import TILE_SIZE

class Animation:
    def __init__(self):
        self.image = 0
        self.frame = 0
        self.tickrate = 1
        self.current_key = "N/A"

    def getImageInAnimation(self,length, w, key):
        self.resetFrames(key)
        u = self.image*w
        if self.framerate():
            self.image+=1
        if self.image==length:
            self.image = 0
        v = key*TILE_SIZE
        return [u,v]
    
    def resetFrames(self, key):
        if key != self.current_key:
            self.image = 0
        self.current_key = key

    def framerate(self):
        return self.frame % (30 * self.tickrate) == 0
