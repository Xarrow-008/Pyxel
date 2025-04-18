import pyxel
from world import*
from player import Player

class App:
    def __init__(self):
        pyxel.init(128, 128, title="test")
        pyxel.load("../eliottg.pyxres")

        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world)
        self.frame = 0

        pyxel.run(self.update, self.draw)

        

    def update(self):
       
        self.frame +=1
        self.player.update()


        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
    
    def draw(self):
        pyxel.cls(0)

        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                tile = self.world.world_map[y][x]
                draw_tile(pyxel, x, y, tile)

        pyxel.blt(self.player.x,
                  self.player.y,
                  SPRITEBANK,
                  WorldItem.PLAYER[0]*TILE_SIZE,
                  WorldItem.PLAYER[1]*TILE_SIZE,
                  TILE_SIZE,
                  TILE_SIZE)

App()