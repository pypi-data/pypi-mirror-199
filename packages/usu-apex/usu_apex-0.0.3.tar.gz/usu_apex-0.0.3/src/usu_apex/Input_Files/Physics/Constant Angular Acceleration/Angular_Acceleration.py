from src.TopicFactory import TopicFactory


class Angular_Acceleration(TopicFactory):
    def __init__(self):

        g = 9.81

        self.input_dict = {
            "radialposition": ["", 3, "angle", "", ""],
            "omegai": ["", 4, "velocity", "", ""],
            "time": ["", 5, "time", "", ""],
            "omegadot" : ["", 3, "acceleration", "", ""],
            "radialpositioni": ["", 2, "angle", "", ""],
            "omegadoti" : ["", 3, "acceleration", "", ""]
                      }

        self.info = {
             "input": self.input_dict,
             "formula": f"omegadot ** 2 == omegadoti ** 2 + 2 * omegadot * (radialposition - radialpositioni)",
             "Note": """
                     This is the angular acceleration of an object as a function of angular acceleration and 
                     angular velocity.
                     """,
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info