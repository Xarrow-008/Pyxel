from world import TILE_SIZE

class Animation:
    def __init__(self):
        self.state = 0
        self.frame = 0
        self.tickrate = 1
        self.ticksSinceLastStage = 0
        self.savedAnimations = {}
        self.animationGroups = []
        self.currentAnimationGroup = "N/A"
        

    def getImageInAnimation(self, length, w, key, durations):
        u = self.state*w
        if self.tick():
            self.ticksSinceLastStage += 1
        if durations[self.state] == self.ticksSinceLastStage:
            self.state += 1
            self.ticksSinceLastStage = 0
        if self.state==length:
            self.state = 0
        v = key*TILE_SIZE
        return [u,v]
    
    def resetStage(self, group, ):
        if group != self.currentAnimationGroup:
            self.state = 0
        self.currentAnimationGroup = group

    def tick(self):
        return self.frame % (30 * self.tickrate) == 0
    
    def saveAnimation(self, length, w, key, name, durations={}):
        for i in range(length):
            if i not in durations.keys():
                durations[i] = 1
        self.savedAnimations[name] = {}
        self.savedAnimations[name]["length"] = length
        self.savedAnimations[name]["w"] = w
        self.savedAnimations[name]["key"] = key
        self.savedAnimations[name]["durations"] = durations

    def createAnimationGroup(self, tab):
        self.animationGroups.append(tab)

    def loadAnimation(self, name):
        animation = self.savedAnimations[name]
        length = animation["length"]
        w = animation["w"]
        key = animation["key"]
        durations = animation["durations"]
        for group in range(len(self.animationGroups)):
            if name in self.animationGroups[group] :
                self.resetStage(group)
        return self.getImageInAnimation(length, w, key, durations)


