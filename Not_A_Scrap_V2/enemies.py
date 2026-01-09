TILE_SIZE = 16
FPS = 120

class EnemyTemplate:

    DUMMY = {"name":"Dummy",
             "image":(32,48),"width":TILE_SIZE,"height":TILE_SIZE,
             "health":100, "maxHealth":100,
             "scaling":1.5,
             "abilities":{
                 "Walk":{"priority":0, "maxSpeed":1, "speedChangeRate":10, "knockbackCoef":1},
                 "Death":{"spawnItem":10, "spawnFuel":10, "spawnWeapon":10},
                 "Hitstun":{"duration":0.75*FPS, "freezeFrame":0, "invincibility":0}
             }}