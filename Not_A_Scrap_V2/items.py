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

ITEM_LIST = [x() for x in Item.__subclasses__()]
    
    
 #Overall i mainly think we need to change the item names, but it shouldnt be a problem, and other than that we shouldnt get stuck with 1 idea (I can only think of 1 item in Hollow knight that works when low health)
 #Yeah but there are like 5 items that trigger when you heal
 #I think having a few items that trigger at the same time isn't really a problem, the important part is that they feel different

 #At the suggestion of Louis, it might be a good idea to move these into a csv file once we've finished (since its not really a program)
 #Actually, no, because some of these items will have effects too complex to be able to describe with just a csv file (or if we do, it'll be impossible to understand what's going on)