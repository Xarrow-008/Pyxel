import inspect
TILE_SIZE = 16
FPS = 120

class Weapon:
    def __init__(self, name, description, handNumber, image, width, height, specialEffects):
        self.name = name
        self.shortDescription = description
        self.handNumber = handNumber
        self.image = image
        self.width = width
        self.height = height
        self.specialEffects = specialEffects

        self.scaling = 1.5

class RangedWeapon(Weapon):
    def __init__(self, baseWeaponInfo, rangedWeaponInfo):
        super().__init__(*baseWeaponInfo)
        self.mode = rangedWeaponInfo[0]

        self.bulletImage = rangedWeaponInfo[1]
        self.bulletWidth = rangedWeaponInfo[2]
        self.bulletHeight = rangedWeaponInfo[3]

        self.spread = rangedWeaponInfo[4]
        self.movingSpreadIncrease = rangedWeaponInfo[5]
        self.bulletCount = rangedWeaponInfo[6]

        self.bulletSpeed = rangedWeaponInfo[7]

        self.range = rangedWeaponInfo[8]
        self.damage = rangedWeaponInfo[9]
        self.piercing = rangedWeaponInfo[10]
        self.knockbackCoef = rangedWeaponInfo[11]
        self.fallOffCoef = rangedWeaponInfo[12]
        self.noFallOffArea = rangedWeaponInfo[13]

        self.reloadTime = rangedWeaponInfo[14]
        self.attackCooldown = rangedWeaponInfo[15]

        self.magAmmo = rangedWeaponInfo[16]
        self.maxAmmo = rangedWeaponInfo[17]
        self.reserveAmmo = rangedWeaponInfo[18]

        self.baseWeaponInfo = baseWeaponInfo
        self.rangedWeaponInfo = rangedWeaponInfo

    def copy(self):
        return RangedWeapon(self.baseWeaponInfo, [self.mode, self.bulletImage, self.bulletWidth, self.bulletHeight, self.spread, self.movingSpreadIncrease, self.bulletCount, self.bulletSpeed, self.range, self.damage, self.piercing, self.knockbackCoef, self.fallOffCoef, self.noFallOffArea, self.reloadTime, self.attackCooldown, self.magAmmo, self.maxAmmo, self.reserveAmmo, self.specialEffects])

class MeleeWeapon(Weapon):
    def __init__(self, baseWeaponInfo, meleeWeaponInfo):
        super().__init__(*baseWeaponInfo)

        self.mode = meleeWeaponInfo[0]

        self.attackImage = meleeWeaponInfo[1]
        self.attackWidth = meleeWeaponInfo[2]
        self.attackHeight = meleeWeaponInfo[3]

        self.hitBoxWidth = meleeWeaponInfo[4]
        self.range = meleeWeaponInfo[5]
        self.maxAngle = meleeWeaponInfo[6]

        self.attackSpeed = meleeWeaponInfo[7]

        self.damage = meleeWeaponInfo[8]
        self.piercing = meleeWeaponInfo[9]
        self.knockbackCoef = meleeWeaponInfo[10]

        self.attackCooldown = meleeWeaponInfo[11]

        self.durability = meleeWeaponInfo[12]
        self.baseDurability = meleeWeaponInfo[13]

        self.baseWeaponInfo = baseWeaponInfo
        #TODO, complete this when we implement melee weapons

    def copy(self):
        return MeleeWeapon(self.baseWeaponInfo, [self.mode, self.attackImage, self.attackWidth, self.attackHeight, self.hitBoxWidth, self.range, self.maxAngle, self.attackSpeed, self.damage, self.piercing, self.knockbackCoef, self.attackCooldown, self.durability, self.baseDurability])



class NO_WEAPON(MeleeWeapon):
    def __init__(self):
        name = "None"
        shortDescription = "No weapon"
        handNumber = 1
        image = (0,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "none":{"description":"No special effects"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "thrust"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE
        range = TILE_SIZE
        maxAngle = 0

        attackSpeed = 1

        damage = 5
        piercing = 1
        knockbackCoef = 3

        attackCooldown = 0.2*FPS

        durability = 0
        baseDurability = 0

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class RUSTY_KNIFE(MeleeWeapon):
    def __init__(self):
        name = "Rusty Knife"
        shortDescription = "A basic knife"
        handNumber = 1
        image = (128,224)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "none":{"description":"No special effects"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "cut"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE
        range = 1.75*TILE_SIZE
        maxAngle = 180

        attackSpeed = 10

        damage = 30
        piercing = 1
        knockbackCoef = 1

        attackCooldown = 0.2*FPS

        durability = 120
        baseDurability = 120

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class PARRYING_DAGGER(MeleeWeapon):
    def __init__(self):
        name = "Parrying Dagger"
        shortDescription = "A defensive melee weapon"
        handNumber = 1
        image = (144,224)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "deflect":{"description":"Stops melee attacks and deflects projectiles"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "cut"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE
        range = 2*TILE_SIZE
        maxAngle = 140

        attackSpeed = 20

        damage = 25
        piercing = 1
        knockbackCoef = 1

        attackCooldown = 1*FPS

        durability = 120
        baseDurability = 120

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class SYRINGE(MeleeWeapon):
    def __init__(self):
        name = "Syringe"
        shortDescription = "A poisonous melee weapon"
        handNumber = 1
        image = (160,224)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "onHitPoison":{"description":"Poisons enemies on hit.", "stacks":1}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "thrust"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = 8
        range = 2*TILE_SIZE
        maxAngle = 180

        attackSpeed = 15

        damage = 30
        piercing = 0
        knockbackCoef = 1

        attackCooldown = 0.3*FPS

        durability = 70
        baseDurability = 70

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class MACE(MeleeWeapon):
    def __init__(self):
        name = "Mace"
        shortDescription = "A slow, powerful melee weapon"
        handNumber = 1
        image = (176,224)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "extraHitstun":{"description":"Enemies are hitstun for longer", "coef":2.5}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "thrust"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE+4
        range = 1.5*TILE_SIZE
        maxAngle = 180

        attackSpeed = 1

        damage = 80
        piercing = 4
        knockbackCoef = 2

        attackCooldown = 1*FPS

        durability = 140
        baseDurability = 140

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class STAFF(MeleeWeapon):
    def __init__(self):
        name = "Staff"
        shortDescription = "A long range melee weapon"
        handNumber = 2
        image = (192,224)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "extraHitstun":{"description":"Enemies are hitstun for longer", "coef":1.5}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "thrust"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = 4
        range = 4*TILE_SIZE
        maxAngle = 180

        attackSpeed = 25

        damage = 30
        piercing = 2
        knockbackCoef = 1

        attackCooldown = 0.4*FPS

        durability = 100
        baseDurability = 100

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class GREATSWORD(MeleeWeapon):
    def __init__(self):
        name = "Greatsword"
        shortDescription = "Powerful melee weapon with circular attacks"
        handNumber = 2
        image = (208,224)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "repeatedHits":{"description":"Attacking continuously will eventually slow you and prevent you from attacking.", "duration":3*FPS, "slowDown":0.5}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "cut"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE
        range = 2*TILE_SIZE
        maxAngle = 360

        attackSpeed = 15

        damage = 40
        piercing = 3
        knockbackCoef = 1

        attackCooldown = 0.4*FPS

        durability = 160
        baseDurability = 160

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class HALBERD(MeleeWeapon):
    def __init__(self):
        name = "Halberd"
        shortDescription = "Melee weapon to deal with multiple enemies"
        handNumber = 2
        image = (224,224)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "onHitDamage":{"description":"Hitting an enemy causes the attack to increase in damage.", "extraDamage":10}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "cut"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE
        range = 3*TILE_SIZE
        maxAngle = 160

        attackSpeed = 5

        damage = 25
        piercing = 4
        knockbackCoef = 1

        attackCooldown = 0.8*FPS

        durability = 130
        baseDurability = 130

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class GAUNTLETS(MeleeWeapon):
    def __init__(self):
        name = "Gauntlets"
        shortDescription = "Fast melee weapon to combo enemies"
        handNumber = 2
        image = (240,224)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "combo":{"description":"Does not hitstun, but damage increases for every time you've hit an enemy.", "extraDamage":5}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "thrust"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE
        range = 1.75*TILE_SIZE
        maxAngle = 180

        attackSpeed = 10

        damage = 20
        piercing = 0
        knockbackCoef = 10

        attackCooldown = 0.3*FPS

        durability = 120
        baseDurability = 120

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class RUSTY_PISTOL(RangedWeapon):
    def __init__(self):
        name = "Rusty Pistol"
        shortDescription = "A basic gun"
        handNumber = 1
        image = (128,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "none":{"description":"No special effects"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "automatic"

        bulletImage = (224,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 15
        movingSpreadIncrease = 15
        bulletCount = 1

        bulletSpeed = 2.5

        range = 6*TILE_SIZE
        damage = 20
        piercing = 0
        knockbackCoef = 1
        fallOffCoef = 1 #Positive = damage decreases with distance / Negative = damage increases with distance
        noFallOffArea = 1-0.9 #This means that there won't be damage fallOff for the first 40% of the projectile's trajectory

        reloadTime = 3*FPS
        attackCooldown = 0.25*FPS

        magAmmo = 20
        maxAmmo = 20
        reserveAmmo = 120

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]
        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class SNIPER(RangedWeapon):
    def __init__(self):
        name = "Sniper"
        shortDescription = "Long-range precision weapon"
        handNumber = 2
        image = (208,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "standingStillEffect":{"description":"Stand still to increase damage.","initialCoef":0.3}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "manual"

        bulletImage = (224,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 5
        movingSpreadIncrease = 50
        bulletCount = 1

        bulletSpeed = 3

        range = 12*TILE_SIZE
        damage = 50
        piercing = 1
        knockbackCoef = 1
        fallOffCoef = -1 #Positive = damage decreases with distance / Negative = damage increases with distance
        noFallOffArea = 1-0.4 #This means that there won't be damage fallOff for the first 40% of the projectile's trajectory

        reloadTime = 5*FPS
        attackCooldown = 1*FPS

        magAmmo = 10
        maxAmmo = 10
        reserveAmmo = 50

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]
        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class SHOTGUN(RangedWeapon):
    def __init__(self):
        name = "Shotgun"
        shortDescription = "Multi-pellet weapon"
        handNumber = 2
        image = (160,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "selfKnockback":{"description":"Attacks deals knockback to you too.", "strength":40}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "manual"

        bulletImage = (224,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 40
        movingSpreadIncrease = 20
        bulletCount = 6

        bulletSpeed = 0.5

        range = 3.5*TILE_SIZE
        damage = 8
        piercing = 0
        knockbackCoef = 1
        fallOffCoef = 2
        noFallOffArea = 1-0.4

        reloadTime = 3*FPS
        attackCooldown = 0.25*FPS

        magAmmo = 6
        maxAmmo = 6
        reserveAmmo = 36

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]

        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class FLARE_GUN(RangedWeapon):
    def __init__(self):
        name = "Flare Gun"
        shortDescription = "Single-fires fire projectiles"
        handNumber = 1
        image = (192,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "onHitFire":{"description":"Deals fire on hit", "stacks":3}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "automatic"

        bulletImage = (230,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 0
        movingSpreadIncrease = 20
        bulletCount = 1

        bulletSpeed = 0.25

        range = 8*TILE_SIZE
        damage = 25
        piercing = 0
        knockbackCoef = 0
        fallOffCoef = 0
        noFallOffArea = 1-0

        reloadTime = 3*FPS
        attackCooldown = 0.25*FPS

        magAmmo = 8
        maxAmmo = 8
        reserveAmmo = 48

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]

        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class FLAMETHROWER(RangedWeapon):
    def __init__(self):
        name = "Flamethrower"
        shortDescription = "Rapidly fires flames"
        handNumber = 2
        image = (128,208)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "repeatedHitFire":{"description":"Deals fire on hit", "stacks":2, "hitNumber":20},
            "continuousFiringFire":{"description":"Firing too long puts you on fire", "stacks":2, "duration":3*FPS}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "automatic"

        bulletImage = (230,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 20
        movingSpreadIncrease = 0
        bulletCount = 1

        bulletSpeed = 0.50

        range = 2.5*TILE_SIZE
        damage = 1
        piercing = 1
        knockbackCoef = 0
        fallOffCoef = 0
        noFallOffArea = 1-0

        reloadTime = 5*FPS
        attackCooldown = 0.05*FPS

        magAmmo = 200
        maxAmmo = 200
        reserveAmmo = 800

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]

        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class GRENADES(RangedWeapon):
    def __init__(self):
        name = "Grenades"
        shortDescription = "Explosive projectiles"
        handNumber = 1
        image = (144,208)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "explosionHit":{"description":"Projectiles explode on hit.", "radius":1*TILE_SIZE}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "manual"

        bulletImage = (224,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 10
        movingSpreadIncrease = 50
        bulletCount = 1

        bulletSpeed = 1

        range = 10*TILE_SIZE
        damage = 40
        piercing = 0
        knockbackCoef = 1
        fallOffCoef = 0
        noFallOffArea = 1-0

        reloadTime = 0*FPS
        attackCooldown = 0.5*FPS

        magAmmo = 30
        maxAmmo = 30
        reserveAmmo = 0

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]

        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class TAZER(RangedWeapon):
    def __init__(self):
        name = "Tazer"
        shortDescription = "Fires electric projectiles"
        handNumber = 1
        image = (240,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "redirect":{"description":"Lightning redirects towards other enemies"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "manual"

        bulletImage = (224,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 5
        movingSpreadIncrease = 20
        bulletCount = 1

        bulletSpeed = 3

        range = 12*TILE_SIZE
        damage = 20
        piercing = 2
        knockbackCoef = 1
        fallOffCoef = 0.5
        noFallOffArea = 1-0.4

        reloadTime = 3*FPS
        attackCooldown = 0.5*FPS

        magAmmo = 12
        maxAmmo = 12
        reserveAmmo = 48

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]

        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class MINIGUN(RangedWeapon):
    def __init__(self):
        name = "Minigun"
        shortDescription = "Increasingly fast weapon"
        handNumber = 2
        image = (224,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "continuousFiringSpeed":{"description":"Holding fire increases firing speed", "coef":0.5, "duration":3*FPS},
            "firingSlowDown":{"description":"You move slower while firing", "slowDown":0.5}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "automatic"

        bulletImage = (224,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 10
        movingSpreadIncrease = 5
        bulletCount = 1

        bulletSpeed = 0.7

        range = 7*TILE_SIZE
        damage = 3
        piercing = 0
        knockbackCoef = 0.2
        fallOffCoef = 1
        noFallOffArea = 1-0.4

        reloadTime = 3*FPS
        attackCooldown = 0.3*FPS

        magAmmo = 100
        maxAmmo = 100
        reserveAmmo = 300

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]

        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class LANCE_PROJECTILE(RangedWeapon): #Creates the projectile for the "Lance of Hyperion" item
    def __init__(self, baseDamage):
        name = ""
        shortDescription = ""
        handNumber = 0
        image = (176,144)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "none":{"description":"No special effects"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = ""

        bulletImage = (176,144)
        bulletWidth = TILE_SIZE
        bulletHeight = TILE_SIZE

        spread = 0
        movingSpreadIncrease = 0
        bulletCount = 1

        bulletSpeed = 3

        range = 12*TILE_SIZE
        damage = baseDamage
        piercing = -1 #infinite piercing
        knockbackCoef = 0
        fallOffCoef = 0 #Positive = damage decreases with distance / Negative = damage increases with distance
        noFallOffArea = 1 #This means that there won't be damage fallOff for the first 40% of the projectile's trajectory

        reloadTime = 0
        attackCooldown = 0

        magAmmo = 0
        maxAmmo = 0
        reserveAmmo = 0

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]
        super().__init__(baseWeaponInfo, rangedWeaponInfo)

WEAPON_LIST = [x() for x in (MeleeWeapon.__subclasses__() + RangedWeapon.__subclasses__()) if (x!=NO_WEAPON and x!=LANCE_PROJECTILE)]

class CLAW_WEAPON(MeleeWeapon):
    def __init__(self):
        name = "Claw"
        shortDescription = "Enemy claw attack"
        handNumber = 1
        image = (0,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "none":{"description":"No special effects"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "cut"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE
        range = 1.75*TILE_SIZE
        maxAngle = 180

        attackSpeed = 20

        damage = 10
        piercing = 0
        knockbackCoef = 2

        attackCooldown = 0.2*FPS

        durability = 999
        baseDurability = 999

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class BITE(MeleeWeapon):
    def __init__(self):
        name = "Bite"
        shortDescription = "Enemy bite attack"
        handNumber = 1
        image = (0,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "none":{"description":"No special effects"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "thrust"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = 12
        range = 1.75*TILE_SIZE
        maxAngle = 180

        attackSpeed = 20

        damage = 20
        piercing = 0
        knockbackCoef = 2

        attackCooldown = 0.2*FPS

        durability = 999
        baseDurability = 999

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class HATCHLING_BITE(MeleeWeapon):
    def __init__(self):
        name = "Bite"
        shortDescription = "Hatchling bite attack"
        handNumber = 1
        image = (0,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "none":{"description":"No special effects"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "thrust"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = 8
        range = 1.6*TILE_SIZE
        maxAngle = 180

        attackSpeed = 20

        damage = 5
        piercing = 0
        knockbackCoef = 2

        attackCooldown = 0.2*FPS

        durability = 999
        baseDurability = 999

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)

class WEB(RangedWeapon):
    def __init__(self):
        name = "Web"
        shortDescription = "Web attack"
        handNumber = 1
        image = (236,64)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "extraHitstun":{"description":"Enemies are hitstun for longer", "coef":1.5}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "automatic"

        bulletImage = (236,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 0
        movingSpreadIncrease = 0
        bulletCount = 1

        bulletSpeed = 1.5

        range = 6*TILE_SIZE
        damage = 15
        piercing = 0
        knockbackCoef = 1
        fallOffCoef = 0 #Positive = damage decreases with distance / Negative = damage increases with distance
        noFallOffArea = 1

        reloadTime = 1*FPS
        attackCooldown = 0.25*FPS

        magAmmo = 999
        maxAmmo = 999
        reserveAmmo = 999

        

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]
        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class BURROWER_CLAW(MeleeWeapon):
    def __init__(self):
        name = "Claw"
        shortDescription = "Burrower claw attack"
        handNumber = 1
        image = (0,192)
        width = TILE_SIZE
        height = TILE_SIZE

        specialEffects = {
            "none":{"description":"No special effects"}
        }

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height, specialEffects]

        mode = "cut"

        attackImage = (0,0)
        attackWidth = TILE_SIZE
        attackHeight = TILE_SIZE

        hitBoxWidth = TILE_SIZE
        range = 1.75*TILE_SIZE
        maxAngle = 180

        attackSpeed = 10

        damage = 15
        piercing = 0
        knockbackCoef = 2

        attackCooldown = 0.2*FPS

        durability = 999
        baseDurability = 999

        meleeWeaponInfo = [mode, attackImage, attackWidth, attackHeight, hitBoxWidth, range, maxAngle, attackSpeed, damage, piercing, knockbackCoef, attackCooldown, durability, baseDurability]

        super().__init__(baseWeaponInfo, meleeWeaponInfo)