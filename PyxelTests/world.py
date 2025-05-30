TILE_SIZE = 8 #MMMMMMMMMM c utilisé partout à faire super gaffe c 8 normalement

SPRITE_BANK = 0

CAMERA_HEIGHT = 128
CAMERA_WIDTH = 128

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
    GHOST = (0,14)


    LAVA_AIR = (1,6)
    GRASS_AIR = (1,7)
    TREE_AIR = (0,6)
    LEAVES_AIR = (0,7)
    PLAYER_AIR = (0,8)
    WATER_AIR = (2,6)
    PATH_AIR = (3,6)
    BRICKS_AIR = (2,7)
    LIGHT_AIR = (3,7)
    BURNING_FLOOR_AIR = (4,6)

    BLOCKS_LIST = [LAVA,GRASS,TREE,LEAVES,WATER,PATH,BRICKS,LIGHT,
                   LAVA_AIR,GRASS_AIR,TREE_AIR,LEAVES_AIR,WATER_AIR,PATH_AIR,BRICKS_AIR,LIGHT_AIR]

    OBJECTS_LIST = [LAMP,GHOST]

    OBJECT_NAMES = ['lamp','ghost']

    OBJECTS_PRESENT = []

class World:
    
    HEIGHT = 32
    WIDTH = 32
    cameraPos = [0,0]
    
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.world_map = []
        self.player_grid_x = 0
        self.player_grid_y = 0
        for y in range(self.HEIGHT):
            self.world_map.append([])
            for x in range(self.WIDTH):
                for block in WorldItem.BLOCKS_LIST:
                    if self.tilemap.pget(x,y) == block: #en gros si le bloc c de l'herbe tu mets de l'herbe ect (traduire du 'pyxel edit' à une liste de blocs avec coordonees bien sucrées au sucre)
                        self.world_map[y].append(block)
                
                for obj in WorldItem.OBJECTS_LIST:
                    if self.tilemap.pget(x,y) == obj:
                        WorldItem.OBJECTS_PRESENT.append({'x':x * TILE_SIZE,'y':y * TILE_SIZE,'name':WorldItem.OBJECT_NAMES[WorldItem.OBJECTS_LIST.index(obj)],'hit':0,'hitAnim':False,'hp':2,'dead':False,'deathAnim':0,'u':obj[0],'v':obj[1],'moment':0,'frameHit':-60})
                        self.world_map[y].append(WorldItem.GRASS_AIR)
                
                if self.tilemap.pget(x,y) == WorldItem.PLAYER or self.tilemap.pget(x,y) == WorldItem.PLAYER_AIR:
                    self.player_grid_x = x #si c un joueur tu bouges sa pos la bas et tu mets de l'herbe
                    self.player_grid_y = y
                    self.world_map[y].append(WorldItem.GRASS_AIR)


    def place_blocks(self,x,y,w,h,block):
        for i in range(w):
            for o in range(h):
                self.world_map[y+i][x+o] = block

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