from UnitFactory import UnitFactory

class force(UnitFactory):
    def __init__(self):
        self.unit_dict = {
            "kN": 1,
            "MN": 1000,
            "N": .001,
            "lb": 224.8089431,
            "kip": .2248089431,
        }

    def giveDict(self):
        return self.unit_dict
