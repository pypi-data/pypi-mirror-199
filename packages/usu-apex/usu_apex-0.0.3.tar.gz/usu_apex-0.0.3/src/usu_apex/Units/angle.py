from UnitFactory import UnitFactory

class angle(UnitFactory):
    def __init__(self):
        self.unit_dict = {
            "radians": 1,
            "degrees": 0.0174533,
        }

    def giveDict(self):
        return self.unit_dict
