
#Damage : Anything that increases DPS
#Healing : Anything that increases survivability
#Support : Everything else

#A stack is an additionnal copy of an item (so if you have 3 copies of an item, then you have 2 stacks of that item)

#6+7+7=20 common items

class Item:

    WAR_FIG : {"name":"War Figurine", #idk abt the name but hard to get a better one
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Chance to ignore damage on hit",
                "long_description":"Every time you get hit, you have a 15% chance to ignore damage. Each stack grants half of the previous one."}

    LUNCHBOX : {"name":"Lunchbox",
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Heal after leaving combat",
                "long_description":"After you haven't gotten hit for 5s, heal for 10HP (+10 per stack)"}    

    PILLOW : {"name":"Pillow",
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Flat physical damage reduction",
                "long_description":"Decreases all physical damage by 1 (+1 per stack). Cannot make attacks deal less than 1 damage."}

    DEFIBRILATOR : {"name":"Defibrilator",
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Killing enemies at low health heals you", #meh kinda just insta fix to problem of low health 
                "long_description":"If you have less than 10% of your max health, heal for 10% of your max health (+5% per stack) when you kill an enemy"}

    TIN_CAN : {"name":"Tin Can",
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Max health increase",
                "long_description":"Increases max health by 15 (+15 per stack)"}

    JACKET : {"name":"Leather Jacket",
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Gain temporary health on kill", #I like the temp health, i would probably put big cap on it like if taken damage recently, cant get temp health, we can balance later
                "long_description":"Every time you kill an enemy, gain temporay health equal to 5% of that enemy's max health (+5% per stack)"}



    KEY_CHAIN : {"name":"Key Chain",
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Interactables are faster and of better quality",
                "long_description":"Interacting with interactables is 10% (+5% per stack) faster and interactables have an extra 5% (+5% per stack) chance of being of a higher quality"}

    SIGN : {"name":"Warning Sign", #Like, a "Slippery when wet" sign
                "image":(0,192), #I feel more like naming it clenching stress or something like it (I'm thinking of a little machine that would press on muscles when in danger) 
                "rarity":"common", #(it would be cool to base our items on some kind of cyberpunk style, like realisticly its obviously long-term bad but on the moment it makes you much stronger)
                "type":"support", 
                "short_description":"Increased movement speed when in danger", #but maybe we shouldn't base too many items on being low on health (might have to discuss this point)
                "long_description":"Movement speed increases by 15% (+10% per stack) when under 20% health. Movement speed increases by 25% once the explosion timer starts."}

    SQUEAKY_TOY : {"name":"Squeaky Toy",
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Deal increased knockback",
                "long_description":"Increases knockback with ranged weapons by 10% (+10% per stack). Increases knockback with melee weapons by 15% (+15% per stack)"}

    WIRE_CUTTER : {"name":"Wire Cutter", #sneak break-in maybe, but a lot of names i think we can change later, its just about me when i'll draw them, thats why i kinda want a theme (cyberpunk)
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Get more time to explore",
                "long_description":"Increases the time before the Horde spawns and the Explosion triggers by 15s (+15 per stack)"}

    SHOE_BOX : {"name":"Shoe Box", #also i just thought that most players wont even look at the name, which means we can invent some things
                "image":(0,192), #for example, do you know the name of the anchor item in Haste? Me, no but I think it increases speed when at full health
                "rarity":"common",
                "type":"support",
                "short_description":"Increased movement speed",
                "long_description":"Increases movement speed by 10% (+10% per stack)"}

    BATTERIES : {"name":"Spare Batteries",
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Decreased dash cooldown",
                "long_description":"Decreases the dash cooldown by 15% (+5% per stack)"}

    GAS_LAMP : {"name":"Gas Lamp", #we can do like compatible jerrycan, and like pouring in is more efficient
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Get more fuel",
                "long_description":"Increases chance to get fuel on kill by 5% (+5% per stack). Extra 10% (+10% per stack) chance to get extra fuel on kill."}

    RED_BOOK : {"name":"Little Red Book",
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "short_description":"Increases damage against strong enemies", #seems OP
                "long_description":"Increases damage by 15%(+15% per stack) against bosses and enemies with a higher level than your weapons"}
    
 #Overall i mainly think we need to change the item names, but it shouldnt be a problem, and other than that we shouldnt get stuck with 1 idea (I can only think of 1 item in Hollow knight that works when low health)