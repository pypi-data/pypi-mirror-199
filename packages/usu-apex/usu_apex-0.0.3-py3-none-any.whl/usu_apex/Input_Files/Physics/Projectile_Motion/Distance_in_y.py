from src.TopicFactory import TopicFactory


class Distnace_in_y(TopicFactory):
    def __init__(self):

        g = 9.81

        self.input_dict = {
            "y": ["", 3, "length", "", ""],
            "yi": ["", 4, "length", "", ""],
            "time": ["", 5, "time", "", ""],
            "vyi" : ["", 3, "velocity", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": f"y == yi + vyi * time - .5 * {g} * time**2",
             "Note": "This is the velocity of the projectile at any time",
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info