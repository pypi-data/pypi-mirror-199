from src.TopicFactory import TopicFactory


class Angular_Position(TopicFactory):
    def __init__(self):

        g = 9.81

        self.input_dict = {
            "radialposition": ["", 3, "angle", "", ""],
            "omegai": ["", 4, "velocity", "", ""],
            "time": ["", 5, "time", "", ""],
            "omegadot" : ["", 3, "acceleration", "", ""],
            "radialpositioni": ["", 2, "angle", "", ""]
                      }

        self.info = {
             "input": self.input_dict,
             "formula": f"radialposition == radialpositioni +  omegai * time + .5 * omegadot * time ** 2",
             "Note": """
                     This is the angular position as a function of initial position, angular velocity, 
                     and angular acceleration.
                     """,
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info