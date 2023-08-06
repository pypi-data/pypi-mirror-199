from src.TopicFactory import TopicFactory

from math import cos

class Projectile_Distance_in_x(TopicFactory):
    def __init__(self):



        self.input_dict = {
            "xtot": ["", 3, "length", "", ""],
            "vi": ["", 4, "velocity", "", ""],
            "time": ["", 5, "time", "", ""],
            "theta": ["", 3, "angle", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": "xtot == vi * cos(theta) * time",
             "Note": """
                    This is the total distance travelled by the projectile in 
                    the x direction as a function of velocity, angle, and time
                    """,
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info