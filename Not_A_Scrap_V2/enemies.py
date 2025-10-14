TILE_SIZE = 16
FPS = 120

class EnemyTemplate:

    DUMMY = {"name":"Dummy",
             "image":(32,48),"width":TILE_SIZE,"height":TILE_SIZE,
             "health":100, "max_health":100,
             "abilities":{
                 "walk":{"priority":0, "max_speed":1, "speedChangeRate":10, "knockback_coef":1},
                 "death":{"spawn_item":True},
                 "hitstun":{"duration":0.75*FPS, "freeze_frame":0}
             }}