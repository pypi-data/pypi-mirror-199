from src.TopicFactory import TopicFactory


class Displacement_in_x(TopicFactory):
    def __init__(self):


        self.input_dict = {
            "x": ["", 3, "length", "", ""],
            "xi": ["", 4, "length", "", ""],
            "time": ["", 5, "time", "", ""],
            "vxi": ["", 2, "velocity", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": "x = xi + vxi * time",
             "Note": """
                     This is the distance that a projectile travels in the x direction as a function of initial
                     velocity, time and the initial position in x. 
                     """,
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info