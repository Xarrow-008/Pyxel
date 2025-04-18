import pyxel
from player import*
from world import*
from physics import*

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Horizontal 2D")
        pyxel.load("../horizontal2D.pyxres")

        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world)
        

        pyxel.run(self.update, self.draw)

    def update(self):
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
                self.player.image[0],
                self.player.image[1],
                TILE_SIZE,
                TILE_SIZE,
                colkey = 11)

App()

