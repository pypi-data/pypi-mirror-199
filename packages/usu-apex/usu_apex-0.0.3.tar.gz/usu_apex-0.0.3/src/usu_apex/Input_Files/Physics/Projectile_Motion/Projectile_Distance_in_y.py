from src.TopicFactory import TopicFactory

from math import sin

class Projectile_Distance_in_x(TopicFactory):
    def __init__(self):

        g = 9.81

        self.input_dict = {
            "ytot": ["", 3, "length", "", ""],
            "vi": ["", 4, "velocity", "", ""],
            "time": ["", 5, "time", "", ""],
            "theta": ["", 3, "angle", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": f"ytot == vi * sin(theta) * time -.5 * {g} * time ** 2",
             "Note": """
                    This is the total distance travelled by the projectile in the y direction as a function 
                    of velocity, angle, and time
                    """,
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info