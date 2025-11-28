
#Damage : Anything that increases DPS
#Healing : Anything that increases survivability
#Support : Everything else

#A stack is an additionnal copy of an item (so if you have 3 copies of an item, then you have 2 stacks of that item)

#6+7+7=20 common items

#I tried to lean into the hyper-capitalistic aspect of cyberpunk

class Item:

    DEFECTIVE_SHIELD : {"name":"Defective Shield", #idk abt the name but hard to get a better one #changed it to give more of the "cyberpunk" aesthetic
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Chance to ignore damage on hit",
                "long_description":"Every time you get hit, you have a 15% chance to ignore damage. Each stack grants half of the previous one."}

    LUNCHBOX : {"name":"Workman's Lunchbox", #The idea is that it only opens when the worker is on break ("Can't eat on the job"). Mirrors the item's effect
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Heal after leaving combat",
                "long_description":"After you haven't gotten hit for 5s, heal for 10HP (+10 per stack)"}    

    PILLOW : {"name":"Pillow", #I mean they still would have pillows in a cyberpunk world right ? #Can't really find a cyberpunk thing that's not just "armor"
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Flat physical damage reduction",
                "long_description":"Decreases all physical damage by 1 (+1 per stack). Cannot make attacks deal less than 1 damage."}

    ADRENALINE_MANUFACTURER : {"name":"Adrenaline Manufacturer",
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Take less damage at low health", #meh kinda just insta fix to problem of low health #I remade the whole item, so that instead of making it so that you just leave low health, it allows you to survive longer while in low health
                "long_description":"If you have less than 10% of your max health, take 10% (+5% per stack) less damage. Cannot make attacks deal less than 50% damage."}

    TIN_CAN : {"name":"Tin Can", #This can work within the cyberpunk aesthetic as like, food from before the cyberpunk era that was preserved
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Max health increase",
                "long_description":"Increases max health by 15 (+15 per stack)"}

    BIOTHERMAL_GENERATOR : {"name":"Biothermal Generator", #It burns the organic material of the enemies to generate the temp health
                "image":(0,192),
                "rarity":"common",
                "type":"healing",
                "short_description":"Gain temporary health on kill", #I like the temp health, i would probably put big cap on it like if taken damage recently, cant get temp health, we can balance later
                "long_description":"Every time you kill an enemy, gain temporay health equal to 5% of that enemy's max health (+5% per stack). Temporary health cannot exceed max health."}

    SUPERVISOR_KEY : {"name":"Supervisor's Keycard", #Would basically be a key card held by the guy that supervises the bunker
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Interactables are faster and of better quality",
                "long_description":"Interacting with interactables is 10% (+5% per stack) faster and interactables have an extra 5% (+5% per stack) chance of being of a higher quality"}

    NOREPINEPHRINE_CATALYST : {"name":"Norepinephrine Catalyst", #Norepinephrine is a molecule that's released when you're in stress to give you a lot of energy (and makes you ignore pain), but has a lot of negative side effects if its produced too much. The idea is that the item boosts your body's norepinephrine production by a lot
                "image":(0,192), #I feel more like naming it clenching stress or something like it (I'm thinking of a little machine that would press on muscles when in danger) 
                "rarity":"common", #(it would be cool to base our items on some kind of cyberpunk style, like realisticly its obviously long-term bad but on the moment it makes you much stronger)
                "type":"support", 
                "short_description":"Increased movement speed when in danger", #but maybe we shouldn't base too many items on being low on health (might have to discuss this point)
                "long_description":"Movement speed increases by 15% (+10% per stack) when under 20% health. Movement speed increases by 25% once the explosion timer starts."}

    PRIVATE_SPHERE : {"name":"Private Sphere Enforcer", #The idea is that its an item that would physically push people out of your private sphere (with like compressed air or something)
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Deal increased knockback",
                "long_description":"Increases knockback with ranged weapons by 10% (+10% per stack). Increases knockback with melee weapons by 15% (+15% per stack)"}

    ALARM_OVERRIDE : {"name":"Alarm Override", #The idea is that its a small bot/drone a hacker would plant on an alarm system to get remote control of it
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Get more time to explore",
                "long_description":"Increases the time before the Horde spawns and the Explosion triggers by 15s (+15 per stack)"}

    SPEED_IMPLANT : {"name":"Neuronal Speed Implant", #also i just thought that most players wont even look at the name, which means we can invent some things #The idea is that it doesn't necesseraly make you physically faster, but increases the speed at which your brain operates, which in turns makes you faster
                "image":(0,192), #for example, do you know the name of the anchor item in Haste? Me, no but I think it increases speed when at full health
                "rarity":"common",
                "type":"support",
                "short_description":"Increased movement speed",
                "long_description":"Increases movement speed by 10% (+10% per stack)"}

    BATTERIES : {"name":"Spare Batteries", #This works fine as cyberpunk
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Decreased dash cooldown",
                "long_description":"Decreases the dash cooldown by 15% (+5% per stack)"}

    COMPATIBLE_JERRYCAN : {"name":"Compatible Jerrycan", #we can do like compatible jerrycan, and like pouring in is more efficient #yeah good idea
                "image":(0,192),
                "rarity":"common",
                "type":"support",
                "short_description":"Get more fuel",
                "long_description":"Increases chance to get fuel on kill by 5% (+5% per stack). Extra 10% (+10% per stack) chance to get extra fuel on kill."}

    RED_BOOK : {"name":"Little Red Book", #Its named after a real life communist book. That way it shows that there still was disagreement with the hypercapitalistic society #Having it be a regular paper book instead of digital/numeric thing also shows disagreement with the state of society
                "image":(0,192),
                "rarity":"common",
                "type":"damage",
                "short_description":"Increases damage against strong enemies", #seems OP #Considering the bosses will be much tougher than regular enemies, I don't think it'll be as OP (though it will still be very useful). Also, we can modify the percentage if its too strong
                "long_description":"Increases damage by 15%(+15% per stack) against bosses and enemies with a higher level than your weapons"} #Also we could make it so that the percentage for bosses and strong enemies is separate if its balanced for bosses but too high for strong enemies
    
 #Overall i mainly think we need to change the item names, but it shouldnt be a problem, and other than that we shouldnt get stuck with 1 idea (I can only think of 1 item in Hollow knight that works when low health)
 #Yeah but there are like 5 items that trigger when you heal
 #I think having a few items that trigger at the same time isn't really a problem, the important part is that they feel different

 #At the suggestion of Louis, it might be a good idea to move these into a csv file once we've finished (since its not really a program)