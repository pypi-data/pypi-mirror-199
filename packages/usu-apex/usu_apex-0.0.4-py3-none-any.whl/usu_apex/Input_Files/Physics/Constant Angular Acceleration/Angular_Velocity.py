from src.TopicFactory import TopicFactory


class Angular_Velocity(TopicFactory):
    def __init__(self):

        g = 9.81

        self.input_dict = {
            "omega": ["", 3, "velocity", "", ""],
            "omegai": ["", 4, "velocity", "", ""],
            "time": ["", 5, "time", "", ""],
            "omegadot" : ["", 3, "acceleration", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": f"omega == omegai * omegadot * time",
             "Note": """
                     This is the angular velocity of an object as a function of the initial angular velocity
                     and the angular acceleration
                     """,
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info