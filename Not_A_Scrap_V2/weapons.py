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

class RangedWeapon(Weapon):
    def __init__(self, baseWeaponInfo, rangedWeaponInfo):
        super().__init__(*baseWeaponInfo)
        self.mode = rangedWeaponInfo[0]

        self.bulletImage = rangedWeaponInfo[1]
        self.bulletWidth = rangedWeaponInfo[2]
        self.bulletHeight = rangedWeaponInfo[3]

        self.spread = rangedWeaponInfo[4]
        self.bulletCount = rangedWeaponInfo[5]

        self.bulletSpeed = rangedWeaponInfo[6]

        self.range = rangedWeaponInfo[7]
        self.damage = rangedWeaponInfo[8]
        self.piercing = rangedWeaponInfo[9]
        self.knockbackCoef = rangedWeaponInfo[10]

        self.reloadTime = rangedWeaponInfo[11]
        self.attackCooldown = rangedWeaponInfo[12]

        self.magAmmo = rangedWeaponInfo[13]
        self.maxAmmo = rangedWeaponInfo[14]
        self.reserveAmmo = rangedWeaponInfo[15]

        self.baseWeaponInfo = baseWeaponInfo
        self.rangedWeaponInfo = rangedWeaponInfo

    def copy(self):
        return RangedWeapon(self.baseWeaponInfo, self.rangedWeaponInfo)

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

        spread = 0
        bulletCount = 1

        bulletSpeed = 0.5

        range = 6*TILE_SIZE
        damage = 15
        piercing = 0
        knockbackCoef = 1

        reloadTime = 3*FPS
        attackCooldown = 0.25*FPS

        magAmmo = 20
        maxAmmo = 20
        reserveAmmo = 120

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]
        print(len(rangedWeaponInfo))
        super().__init__(baseWeaponInfo, rangedWeaponInfo)

class TEST_2_HANDS(RangedWeapon):
    def __init__(self):
        name = "2HANDS"
        shortDescription = "A basic weapon"
        handNumber = 2
        image = (0,112)
        width = TILE_SIZE
        height = TILE_SIZE

        baseWeaponInfo = [name, shortDescription, handNumber, image, width, height]

        mode = "automatic"

        bulletImage = (32,64)
        bulletWidth = 4
        bulletHeight = 4

        spread = 0
        bulletCount = 1

        bulletSpeed = 0.5

        range = 6*TILE_SIZE
        damage = 15
        piercing = 0
        knockbackCoef = 1

        reloadTime = 3*FPS
        attackCooldown = 0.25*FPS

        magAmmo = 20
        maxAmmo = 20
        reserveAmmo = 120

        rangedWeaponInfo = [mode, bulletImage, bulletWidth, bulletHeight, spread, bulletCount, bulletSpeed, range, damage, piercing, knockbackCoef, reloadTime, attackCooldown, magAmmo, maxAmmo, reserveAmmo]

        super().__init__(baseWeaponInfo, rangedWeaponInfo)

WEAPON_LIST = [x() for x in (MeleeWeapon.__subclasses__() + RangedWeapon.__subclasses__()) if x!=NO_WEAPON]