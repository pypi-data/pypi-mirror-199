from usu_apex.UnitFactory import UnitFactory

class acceleration(UnitFactory):
    def __init__(self):
        self.unit_dict = {
            "m/(s)^2": 1,
            "cm/(s)^2": 100,
            "in/(s)^2": 39.37,
            "ft/(s)^2": 3.28084,
            "g": 9.80665
        }

    def giveDict(self):
        return self.unit_dict
