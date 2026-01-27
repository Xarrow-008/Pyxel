import random
from weapons import*
from items import*
from fuel import*

class LootTable:
    def __init__(self, name, table):
        self.name = name
        self.table = table

        self.percent_sum = 0

        last_percent = 0
        for i in range(len(self.table)):
            self.percent_sum += self.table[i][1]
            self.table[i][1] = [x for x in range(last_percent+1, last_percent+self.table[i][1]+1)]
            last_percent = self.table[i][1][-1]

        if self.percent_sum <= 0 :
            self.percent_sum = 1

        

    def pickRandom(self, rerolls=0):
        result = None
        value = 0
        for i in range(1+rerolls):
            percent = random.randint(1,self.percent_sum)
            pick = (None, 0, 0)
            random.shuffle(self.table)
            for item in self.table:
                if percent in item[1] and item[2] >= pick[2]:
                    pick = item
            if pick[2] >= value:
                result = pick[0]
                value = pick[2]

        if type(result)==LootTable:
            result = result.pickRandom(rerolls)

        return result

COMMON_TABLE = LootTable("commonTable", [[x,1,1] for x in ITEM_LIST if x.rarity=="common"])
RARE_TABLE = LootTable("rareTable", [[x,1,1] for x in ITEM_LIST if x.rarity=="rare"])
LEGENDARY_TABLE = LootTable("legendaryTable", [[x,1,1] for x in ITEM_LIST if x.rarity=="legendary"])
ITEM_TABLE = LootTable("itemTable",[[COMMON_TABLE,75,1], [RARE_TABLE,20,2], [LEGENDARY_TABLE,5,3]])
FUEL_TABLE = LootTable("fuelTable",[[SMALL_FUEL(),75, 1], [MEDIUM_FUEL(),20,2], [BIG_FUEL(),5,3]])
WEAPON_TABLE = LootTable("weaponTable",[[x, 1, 1] for x in WEAPON_LIST])
GENERAL_TABLE = LootTable("generalTable",[[ITEM_TABLE,1,1], [FUEL_TABLE,1,1], [WEAPON_TABLE,1,1]])
INCREASED_ITEM_TABLE = LootTable("increasedItemTable",[[RARE_TABLE,20,2], [LEGENDARY_TABLE,5,3]])
INCREASED_GENERAL_TABLE = LootTable("increasedGeneralTable",[[INCREASED_ITEM_TABLE,1,1], [FUEL_TABLE,1,1], [WEAPON_TABLE,1,1]])

COMMON_HEAL_TABLE = LootTable("commonHealTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="common" and x.type=="healing"])
RARE_HEAL_TABLE = LootTable("rareHealTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="rare" and x.type=="healing"])
LEGENDARY_HEAL_TABLE = LootTable("legendaryHealTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="legendary" and x.type=="healing"])
HEAL_TABLE = LootTable("healTable",[[COMMON_HEAL_TABLE, 75, 1], [RARE_HEAL_TABLE, 20, 2], [LEGENDARY_HEAL_TABLE, 5, 3]])
INCREASED_HEAL_TABLE = LootTable("increasedHealTable",[[RARE_HEAL_TABLE, 20, 2], [LEGENDARY_HEAL_TABLE, 5, 3]])

COMMON_SUPPORT_TABLE = LootTable("commonHealTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="common" and x.type=="support"])
RARE_SUPPORT_TABLE = LootTable("rareSupportTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="rare" and x.type=="support"])
LEGENDARY_SUPPORT_TABLE = LootTable("legendarySupportTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="legendary" and x.type=="support"])
SUPPORT_TABLE = LootTable("supportTable",[[COMMON_SUPPORT_TABLE, 75, 1], [RARE_SUPPORT_TABLE, 20, 2], [LEGENDARY_SUPPORT_TABLE, 5, 3]])
INCREASED_SUPPORT_TABLE = LootTable("increasedSupportTable",[[RARE_SUPPORT_TABLE, 20, 2], [LEGENDARY_SUPPORT_TABLE, 5, 3]])

COMMON_DAMAGE_TABLE = LootTable("commonDamageTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="common" and x.type=="damage"])
RARE_DAMAGE_TABLE = LootTable("rareDamageTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="rare" and x.type=="damage"])
LEGENDARY_DAMAGE_TABLE = LootTable("legendaryDamageTable",[[x,1,1] for x in ITEM_LIST if x.rarity=="legendary" and x.type=="damage"])
DAMAGE_TABLE = LootTable("damageTable",[[COMMON_DAMAGE_TABLE, 75, 1], [RARE_DAMAGE_TABLE, 20, 2], [LEGENDARY_DAMAGE_TABLE, 5, 3]])
INCREASED_DAMAGE_TABLE = LootTable("increasedDamageTable",[[RARE_DAMAGE_TABLE, 20, 2], [LEGENDARY_DAMAGE_TABLE, 5, 3]])

def increaseRarity(lootTable):
    print(lootTable.name)
    print(GENERAL_TABLE.name)
    if lootTable.name == "generalTable":
        return INCREASED_GENERAL_TABLE
    elif lootTable.name == "itemTable":
        return INCREASED_ITEM_TABLE
    elif lootTable.name == "healTable" :
        return INCREASED_HEAL_TABLE
    elif lootTable.name == "supportTable":
        return INCREASED_SUPPORT_TABLE
    elif lootTable.name == "damageTable":
        return INCREASED_DAMAGE_TABLE