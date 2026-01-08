class Fuel:
    def __init__(self):
        self.name = ""
        self.shortDescription = ""
        self.image = (0,192)
        self.value = 0

class SMALL_FUEL(Fuel):
    def __init__(self):
        self.name = "Small Fuel Canister"
        self.shortDescription = "Increases fuel by 1"
        self.image = (0,192)
        self.value = 1

class MEDIUM_FUEL(Fuel):
    def __init__(self):
        self.name = "Oil Tank"
        self.shortDescription = "Increases fuel by 3"
        self.image = (0,192)
        self.value = 3

class BIG_FUEL(Fuel):
    def __init__(self):
        self.name = "Rocket Fuel"
        self.shortDescription = "Increases fuel by 5"
        self.image = (0,192)
        self.value = 5