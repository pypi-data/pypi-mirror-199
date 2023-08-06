from UnitFactory import UnitFactory

class length(UnitFactory):
    def __init__(self):
        self.unit_dict = {
            "m": 1,
            "km": 1000,
            "mm": .001,
            "ft": 0.3048,
            "in": 0.0254,
            "yard": 0.9144,
        }

    def giveDict(self):
        return self.unit_dict
