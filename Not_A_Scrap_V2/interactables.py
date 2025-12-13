from lootTables import*

FPS = 120

class InteractableTemplate :

    CHEST = {"name":"Basic Chest",
             "image":(0,192),
             "duration":2*FPS,
             "function":["drop", GENERAL_TABLE],
             "description":"Contains either fuel, an item, or a weapon"}