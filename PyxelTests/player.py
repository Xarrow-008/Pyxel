import os
import pyxel
from world import WorldItem, TILE_SIZE, sprites_collide

class Player:
    IMG = 0
    WIDTH = 8
    HEIGHT = 8
    DX = 1

    def __init__(self, world):
        self.x = world.player_grid_x * TILE_SIZE
        self.y = world.player_grid_y * TILE_SIZE
        self.speed = self.DX
        self.world = world

    def move_left(self): #Ma shala it works but not functionnalized hmmmmmm (g le seum)

        tile_x = int(self.x / TILE_SIZE) # = positions en termes de tiles de 16*16 (self.x est 1/16 de taille de tile)
        tile_y = int(self.y / TILE_SIZE)

        new_x = self.x - self.speed #position apres mouvement
        new_tile_x = tile_x - 1 #position 1 tile dans le sens de la direction


        next_tile_up = self.world.world_map[tile_y][new_tile_x] #nouvelle tile sur laquelle on va check la collision
        next_tile_bottom = (1,6) #explicé au prochain comm et au "and"
        if self.y / TILE_SIZE != tile_y: #fix pour le bord de la map ou tile_y + 1 sortait de la map
            next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x] #dcp ca le fait pas si on est centré tout pile vu que on doit faire collision avec 1 seul block

        if (
        (next_tile_up[1] >= 6 #si le block est de l'air
        or not sprites_collide(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE) #ou si il fait une collision avec le prochain bloc(not + dont a cause du tuto du bled)
        ) and ( #et la meme pour le 2e bloc à tester les collisions car si le joueur est pas sexactement centré il tape 2 blocks
        next_tile_bottom[1] >= 6
        or not sprites_collide(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE))):
            self.x = new_x #en gros cette position est safe, cest bon tu peux y aller + c la meme pour les autres directions

    def move_right(self):

        tile_x = int(self.x / TILE_SIZE)
        tile_y = int(self.y / TILE_SIZE)

        new_x = self.x + self.speed
        new_tile_x = tile_x + 1


        next_tile_up = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = (1,6)
        if self.y / TILE_SIZE != tile_y:
            next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]

        if (
        (next_tile_up[1] >= 6
        or not sprites_collide(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) and (
        next_tile_bottom[1] >= 6
        or not sprites_collide(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE))):
            self.x = new_x

    def move_up(self):

        tile_x = int(self.x / TILE_SIZE)
        tile_y = int(self.y / TILE_SIZE)

        new_y = self.y - self.speed
        new_tile_y = tile_y - 1


        next_tile_up = self.world.world_map[new_tile_y][tile_x]
        next_tile_bottom = (1,6)
        if self.x / TILE_SIZE != tile_x:
            next_tile_bottom = self.world.world_map[new_tile_y][tile_x + 1]

        if (
        (next_tile_up[1] >= 6
        or not sprites_collide(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) and (
        next_tile_bottom[1] >= 6
        or not sprites_collide(self.x, new_y, (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE))):
            self.y = new_y

    def move_down(self):

        tile_x = int(self.x / TILE_SIZE)
        tile_y = int(self.y / TILE_SIZE)

        new_y = self.y + self.speed
        new_tile_y = tile_y + 1


        next_tile_up = self.world.world_map[new_tile_y][tile_x]
        next_tile_bottom = (1,6)
        if self.x / TILE_SIZE != tile_x:
            next_tile_bottom = self.world.world_map[new_tile_y][tile_x + 1]

        if (
        (next_tile_up[1] >= 6
        or not sprites_collide(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) and (
        next_tile_bottom[1] >= 6
        or not sprites_collide(self.x, new_y, (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE))):
            self.y = new_y
    
    '''
    def speed_up(self,amount=0.1,limit_up=3): #ca a juste amene des bugs smeh jmen fous tfacon
        if self.speed <= limit_up:
            self.speed += amount
        if self.speed > limit_up:
            self.speed = limit_up
        print(self.speed)
    
    def speed_down(self,amount=0.1,limit_down=0.6):
        if self.speed >= limit_down:
            self.speed -= amount
        if self.speed < limit_down:
            self.speed = limit_down
        print(self.speed)
    '''

        

