import random
from weapons import*
from items import*
from fuel import*

class LootTable:
    def __init__(self, table):
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

COMMON_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="common"])
RARE_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="rare"])
LEGENDARY_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="legendary"])
RARITY_TABLE = LootTable([[COMMON_TABLE,80,1], [RARE_TABLE,15,2], [LEGENDARY_TABLE,5,3]])
FUEL_TABLE = LootTable([[Fuel.SMALL_FUEL,80, 1], [Fuel.MEDIUM_FUEL,15,2], [Fuel.BIG_FUEL,5,3]])
WEAPON_TABLE = LootTable([[x, 1, 1] for x in WEAPON_LIST])
GENERAL_TABLE = LootTable([[RARITY_TABLE,1,1], [FUEL_TABLE,1,1], [WEAPON_TABLE,1,1]])

COMMON_HEAL_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="common" and x["type"]=="healing"])
RARE_HEAL_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="rare" and x["type"]=="healing"])
LEGENDARY_HEAL_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="legendary" and x["type"]=="healing"])
HEAL_TABLE = LootTable([[COMMON_HEAL_TABLE, 80, 1], [RARE_HEAL_TABLE, 15, 1], [LEGENDARY_HEAL_TABLE, 5, 1]])

COMMON_SUPPORT_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="common" and x["type"]=="support"])
RARE_SUPPORT_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="rare" and x["type"]=="support"])
LEGENDARY_SUPPORT_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="legendary" and x["type"]=="support"])
SUPPORT_TABLE = LootTable([[COMMON_SUPPORT_TABLE, 80, 1], [RARE_SUPPORT_TABLE, 15, 1], [LEGENDARY_SUPPORT_TABLE, 5, 1]])

COMMON_DAMAGE_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="common" and x["type"]=="damage"])
RARE_DAMAGE_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="rare" and x["type"]=="damage"])
LEGENDARY_DAMAGE_TABLE = LootTable([[x,1,1] for x in ITEM_LIST if x["rarity"]=="legendary" and x["type"]=="damage"])
DAMAGE_TABLE = LootTable([[COMMON_DAMAGE_TABLE, 80, 1], [RARE_DAMAGE_TABLE, 15, 1], [LEGENDARY_DAMAGE_TABLE, 5, 1]])