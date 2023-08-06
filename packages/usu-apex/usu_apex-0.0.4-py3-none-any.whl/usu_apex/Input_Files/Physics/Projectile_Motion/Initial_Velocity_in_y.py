from src.TopicFactory import TopicFactory

from math import sin

class Initial_Velocity_in_y(TopicFactory):
    def __init__(self):

        g = 9.81

        self.input_dict = {
            "vyi": ["", 3, "velocity", "", ""],
            "vi": ["", 4, "velocity", "", ""],
            "time": ["", 5, "time", "", ""],
            "theta": ["", 3, "angle", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": f"yxi == vi * sin(theta)",
             "Note": """
                    This is the initial velocity in y as a function of the initial velocity and the angle of 
                    projection
                    """,
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info