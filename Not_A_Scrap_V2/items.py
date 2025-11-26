
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

    RED_BOOK : {"name":"Little Red Book",
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "short_description":"Increases damage against strong enemies", #seems OP
                "long_description":"Increases damage by 15%(+15% per stack) against bosses and enemies with a higher level than your weapons"}
    
