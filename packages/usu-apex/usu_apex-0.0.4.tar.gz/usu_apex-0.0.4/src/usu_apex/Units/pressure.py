from usu_apex.UnitFactory import UnitFactory

class pressure(UnitFactory):
    def __init__(self):
        self.unit_dict = {
            "kPa": 1,
            "Pa": 0.001,
            "psi": 6.89476,
            "bar": 100,
            "atm": 101.325,
            "mmHg": 0.133322,
        }

    def giveDict(self):
        return self.unit_dict
