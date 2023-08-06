from UnitFactory import UnitFactory

class stress(UnitFactory):
    def __init__(self):
        self.unit_dict = {
            "kPa": 1,
            "Pa": 0.001,
            "psi": 6.89476,
        }

    def giveDict(self):
        return self.unit_dict
