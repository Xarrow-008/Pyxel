import inspect
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

    WAR_FIGURINE = {"name":"War Figurine", 
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "effects":[
                    {"stat":"ignoreHitChance","scaling":"geometric", "initial_term":15, "reason":0.5}],
                "short_description":"Chance to ignore damage on hit",
                "long_description":"Every time you get hit, you have a 15% chance to ignore damage. Each stack grants half of the previous one."}

    LUNCHBOX = {"name":"Workman's Lunchbox", 
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "effects":[
                    {"stat":"healLeftCombat","scaling":"arithmetic", "initial_term":10, "reason":10}],
                "short_description":"Heal after leaving combat",
                "long_description":"After you haven't gotten hit or dealt damage for 10s, heal for 10HP (+10 per stack)"}    

    PILLOW = {"name":"Pillow", 
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "effects":[
                    {"stat":"flatDamageReduction","scaling":"arithmetic", "initial_term":1, "reason":1}],
                "short_description":"Flat physical damage reduction",
                "long_description":"Decreases all physical damage by 1 (+1 per stack). Cannot make attacks deal less than 1 damage."}

    MEDICATION = {"name":"Expired Medication",
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "effects":[
                    {"stat":"lowHealthDamageReduction","scaling":"geometric", "initial_term":10, "reason":0.8}],
                "short_description":"Take less damage at low health", 
                "long_description":"If you have less than 10% of your max health, take 10% less damage. Every stack gives 4/5th of the last ones effect."}

    TIN_CAN = {"name":"Tin Can", 
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "effects":[
                    {"stat":"flatMaxHealth","scaling":"arithmetic", "initial_term":15, "reason":15}],
                "short_description":"Max health increase",
                "long_description":"Increases max health by 15 (+15 per stack)"}

    LEATHER_JACKET = {"name":"Leather Jacket", 
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "effects":[
                    {"stat":"onKillTempHealth","scaling":"arithmetic", "initial_term":5, "reason":5}],
                "short_description":"Gain temporary health on kill", 
                "long_description":"Every time you kill an enemy, gain temporay health equal to 5% of that enemy's max health (+5% per stack). Temporary health cannot exceed max health."}

    CARD_DECK = {"name":"Mostly Full Deck of Cards", #Gambling
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "effects":[
                    {"stat":"healReloadCloseEnemies","scaling":"arithmetic", "initial_term":15, "reason":15}],
                "short_description":"Heal after reloading while close to enemies", #The idea is to reward players who take risks by reloading while they're still fighting instead of leaving
                "long_description":"If you finish reloading while you are close to an enemy, heal for 15HP (+15 per stack)"}

    KEY_CHAIN = {"name":"Key Chain",  
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "effects":[
                    {"stat":"interactableSpeed","scaling":"arithmetic", "initial_term":10, "reason":5},
                    {"stat":"interactableQualityChance", "scaling":"arithmetic", "initial_term":5, "reason":5}], #TODO : Implement this one when we make interactables spawn automatically
                "short_description":"Interactables are faster and of better quality",
                "long_description":"Interacting with interactables is 10% (+5% per stack) faster and interactables have an extra 5% (+5% per stack) chance of being of a higher quality"}

    WARNING_SIGN = {"name":"Warning Sign", #A "slippery when wet" sign for example
                "image":(0,192), 
                "rarity":"common", 
                "type":"support", 
                "effects":[
                    {"stat":"lowHealthMoveSpeed","scaling":"arithmetic", "initial_term":15, "reason":10},
                    {"stat":"explosionTimerMoveSpeed", "scaling":"constant", "value":25}], #TODO : Implement this one when we implement the timer
                "short_description":"Increased movement speed when in danger", 
                "long_description":"Movement speed increases by 15% (+10% per stack) when under 20% health. Movement speed increases by 25% once the explosion timer starts."}

    SQUEAKY_TOY = {"name":"Squeaky Toy", 
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "effects":[
                    {"stat":"rangedKnockback","scaling":"arithmetic", "initial_term":10, "reason":10},
                    {"stat":"meleeKnockback", "scaling":"arithmetic", "initial_term":15, "reason":15}], #TODO : Implement this one when we implement melee weapons
                "short_description":"Deal increased knockback",
                "long_description":"Increases knockback with ranged weapons by 10% (+10% per stack). Increases knockback with melee weapons by 15% (+15% per stack)"}

    WIRE_CUTTER = {"name":"Wire Cutter", 
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "effects":[
                    {"stat":"timerTime","scaling":"arithmetic", "initial_term":15, "reason":15}], #TODO : Implement this one when we implement the tiler
                "short_description":"Get more time to explore",
                "long_description":"Increases the time before the Horde spawns and the Explosion triggers by 15s (+15 per stack)"}

    SHOE_BOX = {"name":"Shoe Box", 
                "image":(0,192), 
                "rarity":"common",
                "type":"support",
                "effects":[
                    {"stat":"moveSpeedBoost","scaling":"arithmetic", "initial_term":10, "reason":10}],
                "short_description":"Increased movement speed",
                "long_description":"Increases movement speed by 10% (+10% per stack)"}

    BATTERIES = {"name":"Spare Batteries",
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "effects":[
                    {"stat":"dashCooldownReduction","scaling":"geometric", "initial_term":15, "reason":5/6}],
                "short_description":"Decreased dash cooldown",
                "long_description":"Decreases the dash cooldown by 15%. Every stack gives 5/6th of the last ones effect."}

    JERRYCAN = {"name":"All-Purposes Jerrycan",
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "effects":[
                    {"stat":"fuelKillChance","scaling":"arithmetic", "initial_term":5, "reason":5},
                    {"stat":"extraFuelKillChance", "scaling":"arithmetic", "initial_term":10, "reason":10}],
                "short_description":"Get more fuel",
                "long_description":"Increases chance to get fuel on kill by 5% (+5% per stack). Extra 10% (+10% per stack) chance to get extra fuel on kill."}

    PAMPHLET = {"name":"Pamphlet", #like a political pamphlet that tells you to go vote for a party
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "effects":[
                    {"stat":"ressourceKillChance","scaling":"geometric", "initial_term":5, "reason":0.6}],
                "short_description":"Chance to get ressources back on kill",
                "long_description":"You have a 10% chance to get 5% of your amunitions and durability back on kill. Every stack gives 3/5th of the last ones effect."}

    RED_BOOK = {"name":"Little Red Book", 
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "effects":[
                    {"stat":"strongEnemiesDamageBoost","scaling":"arithmetic", "initial_term":15, "reason":15}],
                "short_description":"Increases damage against strong enemies", 
                "long_description":"Increases damage by 15% (+15% per stack) against bosses and enemies with a higher level than your weapons"} #Considering the fact enemies will outscale the player's stats, I think this item is pretty much a must-have if we want the player to have the ability tp have long runs (but it won't have much of an effect in the early game)

    BOTTLE = {"name":"Broken Bottle", #Broken Glass Bottle
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "effects":[
                    {"stat":"critChanceIncrease","scaling":"arithmetic", "initial_term":5, "reason":5}],
                "short_description":"Increased critical hit chance", 
                "long_description":"Increases your chance of dealing critical hits by 5% (+5% per stack). You cannot increase critical hit chance over 50%"}

    BADGES = {"name":"Scout's Badges", #Like boyscout badges
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "effects":[
                    {"stat":"lowRessourcesDamageIncrease","scaling":"arithmetic", "initial_term":15, "reason":15}],
                "short_description":"Increases damage when low on ressources", 
                "long_description":"Melee weapons deal 15% (+15% per stack) more damage when under 10% durability. Ranged weapons deal 15% (+15% per stack) more damage on the last shot before reloading. Does not affect weapons who only have one shot before reloading."}

    PUZZLE_CUBE = {"name":"Puzzle Cube", #Its just a rubik's cube (I don't think the organisers will allow us to name actual brands)
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "effects":[
                    {"stat":"attackSpeedIncrease","scaling":"geometric", "initial_term":15, "reason":5/6}],
                "short_description":"Increases attack speed", #speedcubing
                "long_description":"Reduces the time between two attacks by 15%. Each stack gives 5/6th of the last ones effect."} #This makes it so that the reduction between attacks is at most 90% (so you can't just make every weapon fire their entire clip in less than 1s with many stacks of this item)

    METAL_SHEET = {"name":"Rusted Metal Sheet", #just a random sheet of metal
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "effects":[
                    {"stat":"fullHealthEnemyDamageBoost","scaling":"arithmetic", "initial_term":100, "reason":50}],
                "short_description":"Increases damage against full health enemies", #the logic behind why this is the effect is that you can't catch tetanos if you already have it
                "long_description":"Increases damage by 100%(+50% per stack) against enemies who have not taken damage"}

    BINOCULAR = {"name":"Dirty Binocular",
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "effects":[
                    {"stat":"rangeIncrease","scaling":"arithmetic", "initial_term":10, "reason":10}],
                "short_description":"Increased range", 
                "long_description":"Bullets can go 10% (+10% per stack) further. Melee attacks have 15% (+15% per stack) more range"}

    GLASSES = {"name":"Glasses", 
                    "image":(0,192),
                    "rarity":"common",
                    "type":"damage",
                    "effects":[
                        {"stat":"precisionIncrease","scaling":"arithmetic", "initial_term":5, "reason":5}],
                    "short_description":"Increased precision", 
                    "long_description":"Increases precision on ranged weapons by 5° (+5° per stack). Decreases by 10° the precision loss while moving."}

ITEM_LIST = []
for i in inspect.getmembers(Item):
    if not i[0].startswith('_'):
        ITEM_LIST.append(i[1])
    
    
 #Overall i mainly think we need to change the item names, but it shouldnt be a problem, and other than that we shouldnt get stuck with 1 idea (I can only think of 1 item in Hollow knight that works when low health)
 #Yeah but there are like 5 items that trigger when you heal
 #I think having a few items that trigger at the same time isn't really a problem, the important part is that they feel different

 #At the suggestion of Louis, it might be a good idea to move these into a csv file once we've finished (since its not really a program)
 #Actually, no, because some of these items will have effects too complex to be able to describe with just a csv file (or if we do, it'll be impossible to understand what's going on)