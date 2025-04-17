import pyxel

class App:
    def __init__(self):
        pyxel.init(128, 128, title="test")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
    
    def draw(self):
        pyxel.cls(0)
        pyxel.text(55,41, "Hello World !", 6)

App()