import inspect
TILE_SIZE = 16
FPS = 120

class Weapon:
    def __init__(self, name, description, handNumber, image, width, height):
        self.name = name
        self.shortDescription = description
        self.handNumber = handNumber
        self.image = image
        self.width = width
        self.height = height

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
        return RangedWeapon(self.baseWeaponInfo, [self.mode, self.bulletImage, self.bulletWidth, self.bulletHeight, self.spread, self.movingSpreadIncrease, self.bulletCount, self.bulletSpeed, self.range, self.damage, self.piercing, self.knockbackCoef, self.fallOffCoef, self.noFallOffArea, self.reloadTime, self.attackCooldown, self.magAmmo, self.maxAmmo, self.reserveAmmo])

class MeleeWeapon(Weapon):
    def __init__(self, baseWeaponInfo):
        super().__init__(*baseWeaponInfo)

        self.baseWeaponInfo = baseWeaponInfo
        #TODO, complete this when we implement melee weapons

    def copy(self):
        return MeleeWeapon(self.baseWeaponInfo)



class NO_WEAPON(MeleeWeapon):
    def __init__(self):
        name = "None"
        shortDescription = "No weapon"
        handNumber = 1
        image = (0,192)
        width = TILE_SIZE
        height = TILE_SIZE

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height]
        super().__init__(baseWeaponInfo)
    
class RUSTY_PISTOL(RangedWeapon):
    def __init__(self):
        name = "Rusty Pistol"
        shortDescription = "A basic weapon"
        handNumber = 1
        image = (0,112)
        width = TILE_SIZE
        height = TILE_SIZE

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height]

        mode = "automatic"

        bulletImage = (32,64)
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


class SNIPER(RangedWeapon): #just a test, you can erase it if you want
    def __init__(self):
        name = "Sniper"
        shortDescription = "Long-range precision weapon"
        handNumber = 2
        image = (80,112)
        width = TILE_SIZE
        height = TILE_SIZE

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height]

        mode = "manual"

        bulletImage = (32,64)
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


class TEST_2_HANDS(RangedWeapon):
    def __init__(self):
        name = "2HANDS"
        shortDescription = "A basic weapon"
        handNumber = 2
        image = (64,112)
        width = TILE_SIZE
        height = TILE_SIZE

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height]

        mode = "automatic"

        bulletImage = (32,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 0
        movingSpreadIncrease = 0
        bulletCount = 1

        bulletSpeed = 0.5

        range = 6*TILE_SIZE
        damage = 40
        piercing = 0
        knockbackCoef = 1
        fallOffCoef = 1
        noFallOffArea = 1-0.4

        reloadTime = 3*FPS
        attackCooldown = 0.25*FPS

        magAmmo = 20
        maxAmmo = 20
        reserveAmmo = 120

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, movingSpreadIncrease, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, fallOffCoef, noFallOffArea, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]

        super().__init__(baseWeaponInfo, rangedWeaponInfo)

WEAPON_LIST = [x() for x in (MeleeWeapon.__subclasses__() + RangedWeapon.__subclasses__()) if x!=NO_WEAPON]