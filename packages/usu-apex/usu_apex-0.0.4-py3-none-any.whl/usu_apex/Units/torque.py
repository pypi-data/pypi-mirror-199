from UnitFactory import UnitFactory

class torque(UnitFactory):
    def __init__(self):
        self.unit_dict = {
            "Nm": 1,
            "ftlb": 0.7376,
            "inlb": 8.851,
            "mNm": 1000,
            "gf cm": 10197,
        }

    def giveDict(self):
        return self.unit_dict
