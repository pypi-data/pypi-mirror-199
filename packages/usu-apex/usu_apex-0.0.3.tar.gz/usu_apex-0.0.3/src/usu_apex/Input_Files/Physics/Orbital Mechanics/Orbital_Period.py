from src.TopicFactory import TopicFactory
import numpy as np

class Orbital_Period(TopicFactory):
    def __init__(self):

        G = 6.6743 * np.power(10, -11)

        self.input_dict = {
            "orbitalradius": ["", 3, "length", "", ""],
            "massorbitant": ["", 4, "mass", "", ""],
            "time": ["", 5, "time", "", ""],
            "orbitalperiod": ["", 3, "time", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": f"orbitalperiod == np.sqrt((4 * np.pi**2 * np.power(orbitalradius, 3) / {G} * massorbitant)",
             "Note": """
                     This is the orbital period of an object around a celestial body as a function of radius and mass
                     """,
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info