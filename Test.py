import pyxel, os, random
"""
def draw_palette(x, y, col):
    rgb = pyxel.colors[col]
    hex = f"#{rgb:06X}"
    dec = f"{rgb >> 16},{(rgb >> 8) & 0xFF},{rgb & 0xFF}"

    pyxel.rect(x, y, 13, 13, col)
    pyxel.text(x + 16, y + 1, hex, 7)
    pyxel.text(x + 16, y + 8, dec, 7)
    pyxel.text(x + 5 - (col // 10) * 2, y + 4, f"{col}", 7 if col < 6 else 0)

    if col == 0:
        pyxel.rectb(x, y, 13, 13, 13)


pyxel.init(255, 81, title="Pyxel Color Palette")
pyxel.cls(0)
old_colors = pyxel.colors.to_list()
pyxel.colors.from_list([0x111111, 0x222222, 0x333333])
pyxel.colors[15] = 0x112233

for i in range(16):
    draw_palette(2 + (i % 4) * 64, 4 + (i // 4) * 20, i)

pyxel.show()
"""
os.system('cls')
canvas = [['.' for x in range(20)] for y in range(20)]

def draw_line(x0,y0,x1,y1):
    positions = []
    cos = x1 - x0
    sin = y1 - y0
    step_ref = max(abs(cos),abs(sin))
    if step_ref != 0:
        stepX = cos / step_ref #diviser toute la longueur par step pour creer chaque marche de l'escalier
        stepY = sin / step_ref #l'autre cote de l'escalier
        for i in range(step_ref+1): #+1 car on met un carre a 0 et a la fin
            positions.append(   (round(x0 + i * stepX), #i fois le nombre de marche auquel on se trouve
                                round(y0 + i * stepY))
                            )
    return positions
position_line = draw_line(10,10,17,1)
for pos in position_line:
    canvas[pos[1]][pos[0]] = '$'
for y in canvas:
    print(y)
print(random.randint(0,1))