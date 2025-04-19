import pyxel
from player import*
from world import*
from physics import*
from camera import*

class App:
    def __init__(self):
        pyxel.init(CAMERA_WIDTH, CAMERA_HEIGHT, title="Horizontal 2D")
        pyxel.load("../horizontal2D.pyxres")

        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world)
        self.camera = Camera(self.player)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.camera.update()

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

            

    def draw(self):
        pyxel.cls(0)

        for y in range(HEIGHT):
            for x in range(WIDTH):
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

