from UnitFactory import UnitFactory

class mass(UnitFactory):
    def __init__(self):
        self.unit_dict = {
            "kg": 1,
            "g": .001,
            "Mg": 1000,
            "lb": 2.2046,
            "kip": 2.2046 * 1088-3,
            "oz": 0.0283495,
            "metric ton": 1000,
            "ozt": 0.0311035,
        }

    def giveDict(self):
        return self.unit_dict
