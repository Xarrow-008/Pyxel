import pyxel
from player import*
from world import*
from physics import*
from camera import*
from entities import*

class App:
    def __init__(self):
        pyxel.init(CAMERA_WIDTH, CAMERA_HEIGHT, title="Horizontal 2D")
        pyxel.load("../horizontal2D.pyxres")

        self.entityHandler = EntityHandler()
        self.world = World(pyxel.tilemaps[0])
        self.player = Player(self.world, self.entityHandler)
        

        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

        if len(self.entityHandler.loadedEntities) > 0:
            for entity in self.entityHandler.loadedEntities:
                entity.update()

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.entityHandler = EntityHandler()
            self.world = World(pyxel.tilemaps[0])
            self.player = Player(self.world, self.entityHandler)

    def draw(self):
        pyxel.cls(0)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                tile = self.world.world_map[y][x]
                draw_tile(pyxel, x, y, tile)

        if len(self.entityHandler.loadedEntities) > 0:
            for entity in self.entityHandler.loadedEntities:
                entity.draw()

        self.player.draw()

App()

