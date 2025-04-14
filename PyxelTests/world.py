TILE_SIZE = 8 #MMMMMMMMMM c utilisé partout à faire super gaffe c 8 normalement

SPRITE_BANK = 0

class WorldItem:

    LAVA = (1,0) #On ne voit pas la difference entre air et non air, jai juste mis depuis l'editeur
    GRASS = (1,1)
    TREE = (0,0)
    LEAVES = (0,1)
    PLAYER = (0,2)
    WATER = (2,0)
    PATH =  (3,0)
    BRICKS = (2,1)
    LIGHT = (3,1)
    LAMP = (0,12)


    LAVA_AIR = (1,6)
    GRASS_AIR = (1,7)
    TREE_AIR = (0,6)
    LEAVES_AIR = (0,7)
    PLAYER_AIR = (0,8)
    WATER_AIR = (2,6)
    PATH_AIR = (3,6)
    BRICKS_AIR = (2,7)
    LIGHT_AIR = (3,7)

    BLOCKS_LIST = [LAVA,GRASS,TREE,LEAVES,WATER,PATH,BRICKS,LIGHT,LAMP,
                   LAVA_AIR,GRASS_AIR,TREE_AIR,LEAVES_AIR,WATER_AIR,PATH_AIR,BRICKS_AIR,LIGHT_AIR]
    OBJECTS_LIST = []

class World:
    
    # each world is 16*16
    HEIGHT = 16
    WIDTH = 16

    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.world_map = []
        self.player_grid_x = 0
        self.player_grid_y = 0
        for y in range(self.HEIGHT):
            self.world_map.append([])
            for x in range(self.WIDTH):
                for i in range(len(WorldItem.BLOCKS_LIST)):
                    if self.tilemap.pget(x,y) == WorldItem.BLOCKS_LIST[i]: #en gros si le bloc c de l'herbe tu mets de l'herbe ect (traduire du "pyxel edit" à une liste de blocs avec coordonees bien sucrées au sucre)
                        self.world_map[y].append(WorldItem.BLOCKS_LIST[i])
                        if WorldItem.BLOCKS_LIST[i] == WorldItem.LAMP:
                            OBJECTS_LIST.append([WorldItem.LAMP, x * TILE_SIZE, y * TILE_SIZE])
                    elif self.tilemap.pget(x,y) == WorldItem.PLAYER or self.tilemap.pget(x,y) == WorldItem.PLAYER_AIR:
                        self.player_grid_x = x #si c un joueur tu bouges sa pos la bas et tu mets de l'herbe
                        self.player_grid_y = y
                        self.world_map[y].append(WorldItem.GRASS_AIR)

def world_item_draw(pyxel, x, y, world_item): #apres juste dessiner chaque bloc, appelé dans le main
    pyxel.blt(
        x * TILE_SIZE,
        y * TILE_SIZE,
        SPRITE_BANK,
        world_item[0] * TILE_SIZE,
        world_item[1] * TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE
    )

def sprites_collide(x1,y1,x2,y2): #jadore c hyper simple et compréhenisble c 2 blocs superposent pas? ok bien le sang

    if x1 + TILE_SIZE <= x2 or x2 + TILE_SIZE <= x1:
        return False
    
    if y1 + TILE_SIZE <= y2 or y2 + TILE_SIZE <= y1:
        return False

    return True