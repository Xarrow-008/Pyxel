import pyxel

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Horizontal 2D")
        pyxel.load("../horizontal2D.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)

App()

