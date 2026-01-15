TILE_SIZE = 16
FPS = 120

#Damage : Anything that increases DPS
#Healing : Anything that increases survivability
#Support : Everything else

#A stack is an additionnal copy of an item (so if you have 3 copies of an item, then you have 2 stacks of that item)

#6+7+7=20 common items

#Common items : Pre-war Everyday items (the literal "scrap" the player is here to collect)
#Rare items : Post-war items (stuff made by the survivors, level of technology would depend on those who made it)
#Legendary items : Pre-war alien technology (cyberpunk/high tech)
#Boss items : either a part of the boss's body, or something they would carry on them (level of technology would depend on the boss)

class Item:
    def __init__(self):
        self.name = ""
        self.image = (0,192)
        self.rarity = ""
        self.type = ""
        self.effects = []
        self.short_description = ""
        self.long_description = ""

class WAR_FIGURINE(Item):
    def __init__(self):
        self.name = "War Figurine"
        self.image = (0,160)
        self.rarity = "common"
        self.type = "healing"
        self.effects = [
            {"stat":"ignoreHitChance","scaling":"geometric", "initial_term":15, "reason":0.5}]
        self.shortDescription = "Chance to ignore damage on hit"
        self.longDescription = "Every time you get hit, you have a 15% chance to ignore damage. Each stack grants half of the previous one."

class LUNCHBOX(Item):
    def __init__(self):
        self.name = "Workman's Lunchbox"
        self.image = (16,160)
        self.rarity = "common"
        self.type = "healing"
        self.effects = [
            {"stat":"healLeftCombat","scaling":"arithmetic", "initial_term":10, "reason":10}]
        self.shortDescription = "Heal after leaving combat"
        self.longDescription = "After you haven't gotten hit or dealt damage for 10s, heal for 10HP (+10 per stack)"

class PILLOW(Item):
    def __init__(self):
        self.name = "Pillow"
        self.image = (32,160)
        self.rarity = "common"
        self.type = "healing"
        self.effects = [
            {"stat":"flatDamageReduction","scaling":"arithmetic", "initial_term":1, "reason":1}]
        self.shortDescription = "Flat physical damage reduction"
        self.longDescription = "Decreases all physical damage by 1 (+1 per stack). Cannot make attacks deal less than 1 damage."

class MEDICATION(Item):
    def __init__(self):
        self.name = "Expired Medication"
        self.image = (48,160)
        self.rarity = "common"
        self.type = "healing"
        self.effects = [
            {"stat":"lowHealthDamageReduction","scaling":"geometric", "initial_term":10, "reason":0.8}]
        self.shortDescription = "Take less damage at low health"
        self.longDescription = "If you have less than 10% of your max health, take 10% less damage. Every stack gives 4/5th of the last ones effect."

class TIN_CAN(Item):
    def __init__(self):
        self.name = "Tin Can"
        self.image = (64,160)
        self.rarity = "common"
        self.type = "healing"
        self.effects = [
            {"stat":"flatMaxHealth","scaling":"arithmetic", "initial_term":15, "reason":15}]
        self.shortDescription = "Max health increase"
        self.longDescription = "Increases max health by 15 (+15 per stack)"

class LEATHER_JACKET(Item):
    def __init__(self):
        self.name = "Leather Jacket"
        self.image = (80,160)
        self.rarity = "common"
        self.type = "healing"
        self.effects = [
            {"stat":"onKillTempHealth","scaling":"arithmetic", "initial_term":5, "reason":5}]
        self.shortDescription = "Gain temporary health on kill"
        self.longDescription = "Every time you kill an enemy, gain temporay health equal to 5% of that enemy's max health (+5% per stack). Temporary health cannot exceed max health."

class CARD_DECK(Item):
    def __init__(self):
        self.name = "Mostly Full Deck of Cards"
        self.image = (96,160)
        self.rarity = "common"
        self.type = "healing"
        self.effects = [
            {"stat":"healReloadCloseEnemies","scaling":"arithmetic", "initial_term":15, "reason":15}]
        self.shortDescription = "Heal after reloading while close to enemies"
        self.longDescription = "If you finish reloading while you are close to an enemy, heal for 15HP (+15 per stack)"

class KEY_CHAIN(Item):
    def __init__(self):
        self.name = "Key Chain"
        self.image = (112,160)
        self.rarity = "common"
        self.type = "support"
        self.effects = [
            {"stat":"interactableSpeed","scaling":"arithmetic", "initial_term":10, "reason":5},
            {"stat":"interactableQualityChance", "scaling":"arithmetic", "initial_term":5, "reason":5}] #TODO : Implement this one when we make interactables spawn automatically
        self.shortDescription = "Interactables are faster and of better quality"
        self.longDescription = "Interacting with interactables is 10% (+5% per stack) faster and interactables have an extra 5% (+5% per stack) chance of being of a higher quality"

class WARNING_SIGN(Item):
    def __init__(self):
        self.name = "Warning Sign"
        self.image = (128,160)
        self.rarity = "common"
        self.type = "support"
        self.effects = [
            {"stat":"lowHealthMoveSpeed","scaling":"arithmetic", "initial_term":15, "reason":10},
            {"stat":"explosionTimerMoveSpeed", "scaling":"constant", "value":25}] #TODO : Implement this one when we implement the timer
        self.shortDescription = "Increased movement speed when in danger"
        self.longDescription = "Movement speed increases by 15% (+10% per stack) when under 20% health. Movement speed increases by 25% once the explosion timer starts."

class SQUEAKY_TOY(Item):
    def __init__(self):
        self.name = "Squeaky Toy"
        self.image = (144,160)
        self.rarity = "common"
        self.type = "support"
        self.effects = [
            {"stat":"rangedKnockback","scaling":"arithmetic", "initial_term":10, "reason":10},
            {"stat":"meleeKnockback", "scaling":"arithmetic", "initial_term":15, "reason":15}] #TODO : Implement this one when we implement melee weapons
        self.shortDescription = "Deal increased knockback"
        self.longDescription = "Increases knockback with ranged weapons by 10% (+10% per stack). Increases knockback with melee weapons by 15% (+15% per stack)"

class WIRE_CUTTER(Item):
    def __init__(self):
        self.name = "Wire Cutter"
        self.image = (160,160)
        self.rarity = "common"
        self.type = "support"
        self.effects = [
            {"stat":"timerTime","scaling":"arithmetic", "initial_term":15, "reason":15}] #TODO : Implement this one when we implement the timer
        self.shortDescription = "Get more time to explore"
        self.longDescription = "Increases the time before the Horde spawns and the Explosion triggers by 15s (+15 per stack)"

class SHOE_BOX(Item):
    def __init__(self):
        self.name = "Shoe Box"
        self.image = (0,176)
        self.rarity = "common"
        self.type = "support"
        self.effects = [
            {"stat":"moveSpeedBoost","scaling":"arithmetic", "initial_term":10, "reason":10}]
        self.shortDescription = "Increased movement speed"
        self.longDescription = "Increases movement speed by 10% (+10% per stack)"

class BATTERIES(Item):
    def __init__(self):
        self.name = "Spare Batteries"
        self.image = (16,176)
        self.rarity = "common"
        self.type = "support"
        self.effects = [
            {"stat":"dashCooldownReduction","scaling":"geometric", "initial_term":15, "reason":5/6}]
        self.shortDescription = "Decreased dash cooldown"
        self.longDescription = "Decreases the dash cooldown by 15%. Every stack gives 5/6th of the last ones effect."

class JERRYCAN(Item):
    def __init__(self):
        self.name = "All-Purposes Jerrycan"
        self.image = (32,176)
        self.rarity = "common"
        self.type = "support"
        self.effects = [
            {"stat":"fuelKillChance","scaling":"arithmetic", "initial_term":5, "reason":5},
            {"stat":"extraFuelKillChance", "scaling":"arithmetic", "initial_term":1, "reason":1}]
        self.shortDescription = "Get more fuel"
        self.longDescription = "Increases chance to get fuel on kill by 5% (+5% per stack). Increases chance to get more fuel."

class PAMPHLET(Item):
    def __init__(self):
        self.name = "Pamphlet"
        self.image = (48,176)
        self.rarity = "common"
        self.type = "support"
        self.effects = [
            {"stat":"ressourceKillEffect","scaling":"geometric", "initial_term":5, "reason":0.6}]
        self.shortDescription = "Chance to get ressources back on kill"
        self.longDescription = "You have a 10% chance to get 5% of your amunitions and durability back on kill. Every stack gives 3/5th of the last ones effect."

class RED_BOOK(Item):
    def __init__(self):
        self.name = "Little Red Book"
        self.image = (64,176)
        self.rarity = "common"
        self.type = "damage"
        self.effects = [
            {"stat":"strongEnemiesDamageBoost","scaling":"arithmetic", "initial_term":15, "reason":15}]
        self.shortDescription = "Increases damage against strong enemies"
        self.longDescription = "Increases damage by 15% (+15% per stack) against bosses and enemies with a higher level than your weapons"

class BOTTLE(Item):
    def __init__(self):
        self.name = "Broken Bottle"
        self.image = (80,176)
        self.rarity = "common"
        self.type = "damage"
        self.effects = [
            {"stat":"critChanceIncrease","scaling":"arithmetic", "initial_term":5, "reason":5}]
        self.shortDescription = "Increased critical hit chance"
        self.longDescription = "Increases your chance of dealing critical hits by 5% (+5% per stack). You cannot increase critical hit chance over 50%"

class BADGES(Item):
    def __init__(self):
        self.name = "Scout's Baddges"
        self.image = (96,176)
        self.rarity = "common"
        self.type = "damage"
        self.effects = [
            {"stat":"lowRessourcesDamageIncrease","scaling":"arithmetic", "initial_term":15, "reason":15}] #TODO : make this work for melee weapons
        self.shortDescription = "Increases damage when low on ressources"
        self.longDescription = "Melee weapons deal 15% (+15% per stack) more damage when under 10% durability. Ranged weapons deal 15% (+15% per stack) more damage on the last shot before reloading. Does not affect weapons who only have one shot before reloading."

class PUZZLE_CUBE(Item):
    def __init__(self):
        self.name = "Puzzle Cube"
        self.image = (112,176)
        self.rarity = "common"
        self.type = "damage"
        self.effects = [
            {"stat":"attackSpeedIncrease","scaling":"geometric", "initial_term":15, "reason":5/6}] #TODO : make this work for melee weapons
        self.shortDescription = "Increases attack speed"
        self.longDescription = "Reduces the time between two attacks by 15%. Each stack gives 5/6th of the last ones effect."

class METAL_SHEET(Item):
    def __init__(self):
        self.name = "Rusted Metal Sheet"
        self.image = (128,176)
        self.rarity = "common"
        self.type = "damage"
        self.effects = [
            {"stat":"fullHealthEnemyDamageBoost","scaling":"arithmetic", "initial_term":100, "reason":50}]
        self.shortDescription = "Increases damage against full health enemies"
        self.longDescription = "Increases damage by 100%(+50% per stack) against enemies who have not taken damage"

class BINOCULAR(Item):
    def __init__(self):
        self.name = "Dirty Binocular"
        self.image = (144,176)
        self.rarity = "common"
        self.type = "damage"
        self.effects = [
            {"stat":"rangeIncrease","scaling":"arithmetic", "initial_term":10, "reason":10}] #TODO : make this work for melee weapons
        self.shortDescription = "Increased range"
        self.longDescription = "Bullets can go 10% (+10% per stack) further. Melee attacks have 15% (+15% per stack) more range"

class GLASSES(Item):
    def __init__(self):
        self.name = "Glasses"
        self.image = (160,176)
        self.rarity = "common"
        self.type = "damage"
        self.effects = [
            {"stat":"precisionIncrease","scaling":"arithmetic", "initial_term":5, "reason":5},
            {"stat":"movingPrecisionIncrease", "scaling":"constant", "value":10}]
        self.shortDescription = "Increased precision"
        self.longDescription = "Increases precision on ranged weapons by 5° (+5° per stack). Decreases by 10° the precision loss while moving."



#Rare items are meant to be things that were made afted the bombs dropped.
#As such, their aesthetic depends a lot on which group made it, it could be :
# Biological (living beings who evolved to better survive the new environment / mutations) -> mainly the Hunter and Mutant enemy groups
# Artisanal (making stuff out of scrap metal based on their old technology) -> mainly the Basics and Legion enemy groups
# Primitive (stuff made by people who've lost their access to pre-war knowledge, and as such are using older techniques (medieval era technology basically)) -> mainly the Celestials enemy group

class GLAND(Item): #Meant to be some sort of organ that evolved to better digest stuff by using the ambiant radiation
    def __init__(self):
        self.name = "Glowing Gland"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "healing"
        self.effects = [
            {"stat":"healAfter10EnemiesKilled","scaling":"arithmetic", "initial_term":15, "reason":10}]
        self.shortDescription = "Heal after killing a few enemies"
        self.longDescription = "Heal for 15%(+10% per stack) of your max health every 10 enemy kills."

class CLAW(Item): #Meant to be hunters/aliens reinforcing their claws by using discarded steel scrap from inside the bunkers
    def __init__(self):
        self.name = "Steel Claw"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "healing"
        self.effects = [
            {"stat":"healCriticalHit","scaling":"arithmetic", "initial_term":10, "reason":10}]
        self.shortDescription = "Critical hits heal you"
        self.longDescription = "Dealing a critical hit heals you for 10%(+10% per stack) of its damage"

class BOOTS(Item): #Basically just heavily reinforced boots meant to be able to traverse the wasteland safely
    def __init__(self):
        self.name = "Wastelander's Boots"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "healing"
        self.effects = [
            {"stat":"ignoreStatusCooldown","scaling":"constant", "value":15*FPS},
            {"stat":"healInsteadOfStatus", "scaling":"geometric", "initial_term":10, "reason":0.6}]
        self.shortDescription = "Ignore status effects and heal instead"
        self.longDescription = "If you would be affected by a status effect, don't, and heal instead for 10% of your max health. Has a 15s cooldown. Every stack gives 3/5th of the last ones effect."


class LEECHES(Item): #Leeches were heavily used during the medieval era to cure the "imbalance in humors" causing diseases (it worked more often than one would expect even though they were completely wrong about why it worked)
    def __init__(self):
        self.name = "Jar of Leeches"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "healing"
        self.effects = [
            {"stat":"healOnHitChance","scaling":"constant", "value":5},
            {"stat":"healOnHitAmount","scaling":"arithmetic", "initial_term":5, "reason":5}]
        self.shortDescription = "Random chance to heal on hit"
        self.longDescription = "Every time you land a hit on an enemy, you have a 5% chance to heal for 5HP(+5 per stack)."

class CLOAK(Item): #This is just a cloak that regular members of the Celestials wear
    def __init__(self):
        self.name = "Acolyte's Cloak"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "support"
        self.effects = [
            {"stat":"extraDash","scaling":"arithmetic", "initial_term":1, "reason":1}]
        self.shortDescription = "Get an additional dash"
        self.longDescription = "You can dash 1(+1 per stack) additional time before having to wait for the cooldown."

class METAL_DETECTOR(Item): #Metal detector made out of magnets or something. Usually used to detect mines and other remnants of the war
    def __init__(self):
        self.name = "Metal Detector"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "support"
        self.effects = [
            {"stat":"increasedRarity","scaling":"incremental", "value":2}]
        self.shortDescription = "The next two items you find will be rare or rarer"
        self.longDescription = "The next two items you find will be either rare or legendary."

class SACK(Item): #Something that was evolved by prey animals to project hot air at predators in order to escape (kind of like squids do it)
    def __init__(self):
        self.name = "Air Sack"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "support"
        self.effects = [
            {"stat":"dashKnockbackStrength","scaling":"arithmetic", "initial_term":15, "reason":15}]
        self.shortDescription = "Pushback enemies while dashing"
        self.longDescription = "Enemies which you enter in contact with, or are near you when finish dashing are knockbacked. The strength of the knockback increases linearly with every stack."

class BANDOLIER(Item):
    def __init__(self):
        self.name = "Bandolier"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "support"
        self.effects = [
            {"stat":"dashKnockbackStrength","scaling":"arithmetic", "initial_term":15, "reason":15}]
        self.shortDescription = "Increased durability, ammo capacity and reload speed"
        self.longDescription = "Increases the ammount of ammo in clips and in the reserve by 15%(+15% per stack). Increases reload speed by 10(+5% per stack). Increases the durability of melee weapons by 35%(+35% per stack)"


class IDOL(Item): #A glass figurine used by the Celestials for prayer. #Because they're obsessed with light, they use mirrors to trap sunlight inside the idols
    def __init__(self):
        self.name = "Bright Idol"
        self.image = (0,192)
        self.rarity = "rare"
        self.type = "damage"
        self.effects = [
            {"stat":"onKillFireEnemyNumber","scaling":"arithmetic", "initial_term":2, "reason":1},
            {"stat":"onKillFireRadius", "scaling":"arithmetic", "initial_term":3*TILE_SIZE, "reason":1.5*TILE_SIZE}]
        self.shortDescription = "Set enemies on fire on kill"
        self.longDescription = "Every time you kill an enemy, 2(+1 per stack) enemies in a 3T(+1.5 per stack) gets set on fire."





ITEM_LIST = [x() for x in Item.__subclasses__()]
    

