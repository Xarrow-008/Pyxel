TILE_SIZE = 16
FPS = 120

class Weapon:

    NONE = {"name":"None", "description": "No weapon",
                    "hand_number":1, "type":"melee", "mode":"manual",
                    "image":(48,48), "width":TILE_SIZE, "height":TILE_SIZE,
                    "spread":0, "bullet_count":0,
                    "bullet_speed":0, "range":0,
                    "damage":0, "piercing":0, "knockback_coef":0,
                    "reload":0*FPS, "cooldown":0*FPS,
                    "mag_ammo":0, "max_ammo":0, "reserve_ammo":0}

    RUSTY_PISTOL = {"name":"Rusty Pistol", "description": "A basic weapon",
                    "hand_number":1, "type":"ranged", "mode":"automatic",
                    "image":(0,112), "width":TILE_SIZE, "height":TILE_SIZE,
                    "spread":0, "bullet_count":1,
                    "bullet_speed":0.5, "range":1,
                    "damage":10, "piercing":0, "knockback_coef":1,
                    "reload":3*FPS, "cooldown":0.1*FPS,
                    "mag_ammo":20, "max_ammo":20, "reserve_ammo":120}